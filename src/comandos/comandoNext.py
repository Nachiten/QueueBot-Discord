from src.configs.globalVariables import GlobalVariables
from src.configs.configs import Configs

from src.utils.utils import esMod
from src.utils.utils import cantidadDeParametrosEs
from src.utils.utils import printearErrorSinPermisos
from src.clases.colas import Colas

comandoNext = Configs.comandoNext
prefijoBot = Configs.prefijoBot


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext(mensaje, autorMensaje):
    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoNext)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos
    canalOutputBot = GlobalVariables.canalOutputBot

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoNext} nombreCola`."
        )
        return

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        await Colas.enviarMensajeNextEnCola(nombreCola, canalOutputBot)
