from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import colas
from utils import enviarMensajeCola
from utils import cantidadDeParametrosEs
from utils import printearErrorSinPermisos

comandoCreate = Configs.comandoCreate
prefijoBot = Configs.prefijoBot


# Description: Crea un nueva cola y la agrega a la lista
# Access: Only Mods
async def manejarComandoCreate(mensaje, autorMensaje, tagAlAutor):

    # Verificacion de mod
    if not esMod(autorMensaje):
        printearErrorSinPermisos(autorMensaje, comandoCreate)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoCreate} nombreCola`")
        return

    nombreCola = parametrosMensaje[2]

    if (existeCola(nombreCola)):
        await canalSpamComandos.send(f"Ya existe una cola con el nombre **{nombreCola}**!")
    else:
        colas.append((nombreCola, [], None))
        await canalSpamComandos.send(f"{tagAlAutor} ha creado una nueva cola llamada: **{str(nombreCola)}**.")
        await enviarMensajeCola(nombreCola)
