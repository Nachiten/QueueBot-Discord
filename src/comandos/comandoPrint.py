from configs.globalVariables import GlobalVariables

from clases.colas import Colas
from utils.utils import esMod
from utils.utils import printearErrorSinPermisos

comandoPrint = "print"


async def manejarComandoPrint(autorMensaje):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoPrint)
        return

    await Colas.printeameLasColas(canalSpamComandos)
