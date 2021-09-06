from configs.configs import Configs

from utils.utils import esMod
from utils.utils import cantidadDeParametrosEs
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoList = Configs.comandoList
prefijoBot = Configs.prefijoBot


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList(mensaje, autorMensaje, channel):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoList, channel)
        return False

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoList} nombreCola`"
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    await Colas.enviarMensajeNuevoEnCola(nombreCola, channel)

    return True
