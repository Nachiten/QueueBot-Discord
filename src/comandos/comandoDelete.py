from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import esMod
from utils.utils import cantidadDeParametrosEs
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoDelete = Configs.comandoDelete
prefijoBot = Configs.prefijoBot


# Description: Eliminar una cola
# Access: Only Mods
async def manejarComandoDelete(mensaje, autorMensaje, tagAlAutor, channel):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoDelete, channel)
        return False

    canalSpamComandos = GlobalVariables.canalOutputComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: {prefijoBot} {comandoDelete} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    await Colas.eliminarMensajeEnCola(nombreCola)
    Colas.quitarCola(nombreCola)
    await canalSpamComandos.send(
        f"{tagAlAutor} ha eliminado la cola **{nombreCola}**.")
    return True
