from colas import Colas
from globalVariables import GlobalVariables
from utils import esMod
from utils import printearErrorSinPermisos

comandoPrint = "print"


async def manejarComandoPrint(autorMensaje):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoPrint)
        return

    await Colas.printeameLasColas(canalSpamComandos)
