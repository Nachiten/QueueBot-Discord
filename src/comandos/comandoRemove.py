from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from clases.colas import Colas
from utils.utils import cantidadDeParametrosEs

comandoRemove = Configs.comandoRemove
prefijoBot = Configs.prefijoBot


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove(mensaje, autorMensaje, tagAlAutor, channel):
    canalSpamComandos = GlobalVariables.canalOutputComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoRemove} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    if not Colas.existeUsuarioEnCola(autorMensaje, nombreCola):
        await channel.send(
            f"{tagAlAutor} no estas en la cola **{nombreCola}**!")
        return False

    Colas.quitarUsuarioDeCola(autorMensaje, nombreCola)
    await canalSpamComandos.send(
        f"{tagAlAutor} ha sido quitado de la cola **{nombreCola}**.")
    await Colas.actualizarMensajeExistenteEnCola(nombreCola)

    return True
