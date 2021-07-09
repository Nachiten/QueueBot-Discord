from configs import Configs
from globalVariables import GlobalVariables

from utils import cantidadDeParametrosEs
from colas import Colas

comandoRemove = Configs.comandoRemove
prefijoBot = Configs.prefijoBot


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoRemove} nombreCola`."
        )
        return

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        if not Colas.existeUsuarioEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(
                f"{tagAlAutor} no estas en la cola **{nombreCola}**!")
        else:
            Colas.quitarUsuarioDeCola(autorMensaje, nombreCola)
            await canalSpamComandos.send(
                f"{tagAlAutor} ha sido quitado de la cola **{nombreCola}**.")
            await Colas.actualizarMensajeExistenteEnCola(nombreCola)
