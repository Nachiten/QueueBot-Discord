from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import enviarMensajeCola
from utils import cantidadDeParametrosEs
from utils import printearErrorSinPermisos

comandoList = Configs.comandoList
prefijoBot = Configs.prefijoBot


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList(mensaje, autorMensaje, tagAlAutor):
    # Verificacion de mod
    if not esMod(autorMensaje):
        printearErrorSinPermisos(autorMensaje, comandoList)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoList} nombreCola`")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        await enviarMensajeCola(nombreCola)
