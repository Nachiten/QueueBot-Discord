from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import esMod
from utils.utils import cantidadDeParametrosEs
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoNext = Configs.comandoNext
prefijoBot = Configs.prefijoBot


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext(mensaje, autorMensaje):
    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoNext)
        return False

    canalSpamComandos = GlobalVariables.canalSpamComandos
    canalOutputBot = GlobalVariables.canalOutputBot

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoNext} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
        return False

    await Colas.enviarMensajeNextEnCola(nombreCola, canalOutputBot)
    return True
