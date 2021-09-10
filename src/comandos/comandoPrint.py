from configs.globalVariables import GlobalVariables

from clases.colas import Colas
from utils.utils import esMod
from utils.utils import printearErrorSinPermisos

comandoPrint = "print"

# Nota: Este comando no aparece en help (sirve para debug)
# Description: Printear todas las colas en el canal de logs
# Access: Only Mods
async def manejarComandoPrint(autorMensaje, channel):
    canalSpamComandos = GlobalVariables.canalOutputComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoPrint, channel)
        return False

    await Colas.printeameLasColas(canalSpamComandos)

    return True
