from src.configs.globalVariables import GlobalVariables
from src.configs.configs import Configs

from src.utils.utils import esMod
from src.utils.utils import printearErrorSinPermisos
from src.clases.colas import Colas

comandoAll = Configs.comandoAll
prefijoBot = Configs.prefijoBot
imagenThumbnail = Configs.imagenThumbnail


# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll(autorMensaje):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoAll)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    mensajeEmbed = Colas.generarMensajeListandoColas()

    await canalSpamComandos.send(embed=mensajeEmbed)
