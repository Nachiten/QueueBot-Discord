from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from utils.utils import cantidadDeParametrosEs
from clases.colas import Colas

comandoAdd = Configs.comandoAdd
prefijoBot = Configs.prefijoBot


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd(mensaje, autorMensaje, tagAlAutor, voiceState):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoAdd} nombreCola`."
        )
        return False

    nombreCola = parametrosMensaje[2]

    if not Colas.existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
        return False
    else:
        if Colas.existeUsuarioEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(
                f"{tagAlAutor} ya estas en la cola **{nombreCola}**!")
            return False
        else:
            if voiceState is None:
                await canalSpamComandos.send(f"{tagAlAutor} para unirte a la cola necesitas estar conectado "
                                             f"en algun canal de soporte!")
                return False
            else:
                Colas.agregarUsuarioACola(autorMensaje, nombreCola, voiceState.channel)
                await canalSpamComandos.send(
                    f"{tagAlAutor} ha sido agregado a la cola **{nombreCola}**.")
                await Colas.actualizarMensajeExistenteEnCola(nombreCola)
                return True
