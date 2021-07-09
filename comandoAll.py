from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import printearErrorSinPermisos
from colas import Colas

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
