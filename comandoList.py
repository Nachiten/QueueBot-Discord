from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import cantidadDeParametrosEs
from utils import printearErrorSinPermisos
from colas import Colas

comandoList = Configs.comandoList
prefijoBot = Configs.prefijoBot


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList(mensaje, autorMensaje):

    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoList)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoList} nombreCola`"
        )
        return

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        await Colas.enviarMensajeNuevoEnCola(nombreCola)
