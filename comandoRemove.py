from configs import Configs
from globalVariables import GlobalVariables

from utils import existeMiembroEnCola
from utils import existeCola
from utils import cantidadDeParametrosEs
from utils import actualizarMensajeCola
from utils import indexDeCola
from utils import colas

comandoRemove = Configs.comandoRemove
prefijoBot = Configs.prefijoBot


# Quita un miembro de una cola
def quitarDeCola(nombreCola, autorMensaje):
    colas[indexDeCola(nombreCola)][1].remove(autorMensaje)


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoRemove} nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        if not existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(f"{tagAlAutor} no estas en la cola **{nombreCola}**!")
        else:
            quitarDeCola(nombreCola, autorMensaje)
            await canalSpamComandos.send(f"{tagAlAutor} ha sido quitado de la cola **{nombreCola}**.")
            await actualizarMensajeCola(nombreCola)
