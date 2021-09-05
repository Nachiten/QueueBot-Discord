from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import esMod
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoAll = Configs.comandoAll
prefijoBot = Configs.prefijoBot
imagenThumbnail = Configs.imagenThumbnail


# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll(autorMensaje):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoAll)
        return False

    canalSpamComandos = GlobalVariables.canalSpamComandos

    mensajeEmbed = Colas.generarMensajeListandoColas()

    await canalSpamComandos.send(embed=mensajeEmbed)

    return True
