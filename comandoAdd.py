from configs import Configs
from globalVariables import GlobalVariables

from utils import existeMiembroEnCola
from utils import existeCola
from utils import actualizarMensajeCola
from utils import cantidadDeParametrosEs
from utils import colas
from utils import indexDeCola

comandoAdd = Configs.comandoAdd
prefijoBot = Configs.prefijoBot


# Agrega nuevo miembro a una cola
def agregarACola(nombreCola, autorMensaje):
    colas[indexDeCola(nombreCola)][1].append(autorMensaje)


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoAdd} nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        if existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(
                f"{tagAlAutor} ya estas en la cola **{nombreCola}**!")
        else:
            agregarACola(nombreCola, autorMensaje)
            await canalSpamComandos.send(
                f"{tagAlAutor} ha sido agregado a la cola **{nombreCola}**.")
            await actualizarMensajeCola(nombreCola)
