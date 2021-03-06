from configs.configs import Configs

from utils.utils import esMod
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoAll = Configs.comandoAll
prefijoBot = Configs.prefijoBot
imagenThumbnail = Configs.imagenThumbnail


# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll(autorMensaje, channel):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoAll, channel)
        return False

    mensajeEmbed = Colas.generarMensajeListandoColas()

    await channel.send(embed=mensajeEmbed)

    return True
