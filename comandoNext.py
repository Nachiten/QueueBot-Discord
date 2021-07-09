from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import existeCola
from utils import colas
from utils import cantidadDeParametrosEs
from utils import indexDeCola
from utils import actualizarMensajeCola
from utils import printearErrorSinPermisos

comandoNext = Configs.comandoNext
prefijoBot = Configs.prefijoBot


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext(mensaje, autorMensaje, tagAlAutor):
    # Verificacion de mod
    if not esMod(autorMensaje):
        printearErrorSinPermisos(autorMensaje, comandoNext)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos
    canalOutputBot = GlobalVariables.canalOutputBot

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(f"Sintaxis incorrecta, uso: `{prefijoBot} {comandoNext} nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send(f"No existe la cola **{nombreCola}**!")
    else:
        if len(colas[indexDeCola(nombreCola)][1]) == 0:
            await canalOutputBot.send(f"No quedan miembros en la cola **{nombreCola}**.")
            return
        else:
            # Calculo los siguientes para printearlos
            siguienteEnLaLista = "<@" + str(
                colas[indexDeCola(nombreCola)][1].pop(0).id) + ">"
            siguienteAlSiguienteEnLaLista = " No hay nadie mas adelante en la cola."

            if len(colas[indexDeCola(nombreCola)][1]) >= 1:
                siguienteAlSiguienteEnLaLista = " El siguiente en la lista es: <@" + str(
                    colas[indexDeCola(nombreCola)][1][0].id) + ">."

            await canalOutputBot.send(siguienteEnLaLista +
                                      " es tu turno en la cola **" +
                                      nombreCola + "**." +
                                      siguienteAlSiguienteEnLaLista)
            await actualizarMensajeCola(nombreCola)
