from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import cantidadDeParametrosEs
from clases.colas import Colas
from utils.utils import esMod
from utils.utils import printearErrorSinPermisos

comandoAdd = Configs.comandoAdd
prefijoBot = Configs.prefijoBot


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd(mensaje, autorMensaje, tagAlAutor, voiceState, channel):
    canalSpamComandos = GlobalVariables.canalOutputComandos

    parametrosMensaje = mensaje.split(" ", 5)

    tieneNombreEscrito = False
    nombreEscrito = ""

    # Si hay 4 parametros quiere agregar una persona con nombre como string
    if cantidadDeParametrosEs(4, parametrosMensaje):
        # Debo checkear que sea mod antes de ejecutar este path
        if not esMod(autorMensaje):
            await printearErrorSinPermisos(autorMensaje, comandoAdd, channel)
            return False
        tieneNombreEscrito = True
        nombreEscrito = parametrosMensaje[3]

    # Solo debe haber tres parametros (si no pasa lo anterior)
    elif not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoAdd} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    # Si ya esta en la cola y el nombre no viene escrito
    if Colas.existeUsuarioEnCola(autorMensaje, nombreCola) and not tieneNombreEscrito:
        await channel.send(
            f"{tagAlAutor} ya estas en la cola **{nombreCola}**!")
        return False

    # No esta en ningun canal de voz y el nombre no viene escrito
    if voiceState is None and not tieneNombreEscrito:
        await channel.send(
            f"{tagAlAutor} para unirte a la cola necesitas estar conectado en algun canal de soporte!")
        return False

    # El nombre viene dado en el mensaje
    if tieneNombreEscrito:
        Colas.agregarUsuarioACola(nombreEscrito, nombreCola, "n/a")
        await canalSpamComandos.send(
            f"{nombreEscrito} ha sido agregado a la cola **{nombreCola}**.")
    # Se agrega a la persona que envio el mensaje
    else:
        Colas.agregarUsuarioACola(autorMensaje, nombreCola, voiceState.channel)
        await canalSpamComandos.send(
            f"{tagAlAutor} ha sido agregado a la cola **{nombreCola}**.")
    await Colas.actualizarMensajeExistenteEnCola(nombreCola)
    return True
