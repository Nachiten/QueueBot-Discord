from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import colas
from utils import enviarMensajeCola
from utils import cantidadDeParametrosEs

comandoCreate = Configs.comandoCreate
prefijoBot = Configs.prefijoBot

# Description: Crea un nueva cola y la agrega a la lista
# Access: Only Mods
async def manejarComandoCreate(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoCreate + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando."
                                     )
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoCreate +
                                     " nombreCola`")
        return

    nombreCola = parametrosMensaje[2]

    if (existeCola(nombreCola)):
        await canalSpamComandos.send("Ya existe una cola con el nombre **" +
                                     nombreCola + "**!")
    else:
        colas.append((nombreCola, [], None))
        await canalSpamComandos.send(tagAlAutor +
                                     " ha creado una nueva cola llamada: **" +
                                     str(nombreCola) + "**.")
        await enviarMensajeCola(nombreCola)