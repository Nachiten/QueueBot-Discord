from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import enviarMensajeCola
from utils import cantidadDeParametrosEs

comandoList = Configs.comandoList
prefijoBot = Configs.prefijoBot


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoList + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoList +
                                     " nombreCola`")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola + "**!")
    else:
        await enviarMensajeCola(nombreCola)
