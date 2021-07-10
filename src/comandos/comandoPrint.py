from src.configs.globalVariables import GlobalVariables

from src.clases.colas import Colas
from src.utils.utils import esMod
from src.utils.utils import printearErrorSinPermisos

comandoPrint = "print"


async def manejarComandoPrint(autorMensaje):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoPrint)
        return

    await Colas.printeameLasColas(canalSpamComandos)
