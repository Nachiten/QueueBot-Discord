from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import cantidadDeParametrosEs
from utils import eliminarMensajeCola
from utils import eliminarCola

comandoDelete = Configs.comandoDelete
prefijoBot = Configs.prefijoBot

# Description: Eliminar una cola
# Access: Only Mods
async def manejarComandoDelete(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoDelete + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando."
                                     )
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoDelete +
                                     " nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola +
                                     "**!")
    else:
        await eliminarMensajeCola(nombreCola)
        eliminarCola(nombreCola)
        await canalSpamComandos.send(tagAlAutor + " ha eliminado la cola **" +
                                     nombreCola + "**.")