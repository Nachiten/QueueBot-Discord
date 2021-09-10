from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from clases.colas import Colas
from utils.utils import cantidadDeParametrosEs

from utils.utils import esMod
from utils.utils import printearErrorSinPermisos

comandoRemove = Configs.comandoRemove
prefijoBot = Configs.prefijoBot


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove(mensaje, autorMensaje, tagAlAutor, channel):
    canalSpamComandos = GlobalVariables.canalOutputComandos

    parametrosMensaje = mensaje.split(" ", 5)

    tieneNombreEscrito = False
    nombreEscrito = ""

    # Si hay 4 parametros quiere agregar una persona con nombre como string
    if cantidadDeParametrosEs(4, parametrosMensaje):
        # Debo checkear que sea mod antes de ejecutar este path
        if not esMod(autorMensaje):
            await printearErrorSinPermisos(autorMensaje, comandoRemove, channel)
            return False
        tieneNombreEscrito = True
        nombreEscrito = parametrosMensaje[3]

    # Solo debe haber tres parametros (si no pasa lo anterior)
    elif not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoRemove} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    # No existe la cola
    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    # Estoy agregando a quien mando el mensaje y no esta en la cola
    if not Colas.existeUsuarioEnCola(autorMensaje, nombreCola) and not tieneNombreEscrito:
        await channel.send(
            f"{tagAlAutor} no estas en la cola **{nombreCola}**!")
        return False

    # El nombre viene como string
    if not tieneNombreEscrito:
        Colas.quitarUsuarioDeCola(autorMensaje, nombreCola)
        await canalSpamComandos.send(
            f"{tagAlAutor} ha sido quitado de la cola **{nombreCola}**.")
    # Se agrega a la persona que envio el mensaje
    else:
        quitadoSatisfactorio = Colas.quitarUsuarioPorStringDeCola(nombreEscrito, nombreCola)

        # Pude quitar el usuario porque existia
        if quitadoSatisfactorio:
            await canalSpamComandos.send(
                f"{nombreEscrito} ha sido quitado de la cola **{nombreCola}**.")
            await Colas.actualizarMensajeExistenteEnCola(nombreCola)
            return True
        # No existia el usuario
        else:
            await channel.send(
                f"{nombreEscrito} no existe en la cola **{nombreCola}**.")
            await Colas.actualizarMensajeExistenteEnCola(nombreCola)
            return False
