from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import esMod
from utils.utils import cantidadDeParametrosEs
from utils.utils import printearErrorSinPermisos
from clases.colas import Colas

comandoCreate = Configs.comandoCreate
prefijoBot = Configs.prefijoBot


# Description: Crea un nueva cola y la agrega a la lista
# Access: Only Mods
async def manejarComandoCreate(mensaje, autorMensaje, tagAlAutor, channel):
    # Verificacion de mod
    if not esMod(autorMensaje):
        await printearErrorSinPermisos(autorMensaje, comandoCreate, channel)
        return False

    canalSpamComandos = GlobalVariables.canalOutputComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await channel.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoCreate} nombreCola`"
        )
        return False

    nombreCola = parametrosMensaje[2]

    if Colas.existeCola(nombreCola):
        await channel.send(
            f"Ya existe la cola **{nombreCola}**!")
        return False

    Colas.agregarCola(nombreCola, channel)
    await canalSpamComandos.send(
        f"{tagAlAutor} ha creado la cola **{str(nombreCola)}**."
    )
    await Colas.enviarMensajeNuevoEnCola(nombreCola)

    return True
