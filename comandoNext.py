from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import cantidadDeParametrosEs
from utils import printearErrorSinPermisos
from colas import Colas

comandoNext = Configs.comandoNext
prefijoBot = Configs.prefijoBot


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext(mensaje, autorMensaje, tagAlAutor):
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
        if Colas.cantidadDeUsuariosEnCola(nombreCola) == 0:
            await canalOutputBot.send(
                f"No quedan miembros en la cola **{nombreCola}**.")
            return
        else:
            # Calculo los siguientes para printearlos
            siguienteEnLaLista = "<@" + str(
                Colas.obtenerYQuitarIdDeSiguienteEnCola(nombreCola)) + ">"
            siguienteAlSiguienteEnLaLista = " No hay nadie mas adelante en la cola."

            if Colas.cantidadDeUsuariosEnCola(nombreCola) >= 1:
                siguienteAlSiguienteEnLaLista = " El siguiente en la lista es: <@" + str(
                    Colas.obtenerIdDeSiguienteEnCola(nombreCola)) + ">."

            await canalOutputBot.send(siguienteEnLaLista +
                                      " es tu turno en la cola **" +
                                      nombreCola + "**." +
                                      siguienteAlSiguienteEnLaLista)
            await Colas.actualizarMensajeExistenteEnCola(nombreCola)
