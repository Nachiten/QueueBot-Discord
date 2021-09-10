from configs.configs import Configs

from utils.utils import esMod
from utils.utils import cantidadDeParametrosEs
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoNext = Configs.comandoNext
prefijoBot = Configs.prefijoBot


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext(mensaje, autorMensaje, channel):
    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoNext, channel)
        return False

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoNext} nombreCola`.")
        return False

    nombreCola = parametrosMensaje[2]

    # No existe la cola
    if not Colas.existeCola(nombreCola):
        await channel.send(f"No existe la cola **{nombreCola}**!")
        return False

    await Colas.enviarMensajeNextEnCola(nombreCola)
    return True
