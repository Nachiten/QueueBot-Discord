from configs import Configs
from globalVariables import GlobalVariables

from utils import cantidadDeParametrosEs
from colas import Colas

comandoAdd = Configs.comandoAdd
prefijoBot = Configs.prefijoBot


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoAdd} nombreCola`."
        )
        return

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        if Colas.existeUsuarioEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(
                f"{tagAlAutor} ya estas en la cola **{nombreCola}**!")
        else:
            Colas.agregarUsuarioACola(autorMensaje, nombreCola)
            await canalSpamComandos.send(
                f"{tagAlAutor} ha sido agregado a la cola **{nombreCola}**.")
            await Colas.actualizarMensajeExistenteEnCola(nombreCola)
