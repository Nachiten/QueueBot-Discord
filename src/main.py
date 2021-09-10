import discord
import traceback

from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from clases.colas import Colas

from comandos.comandoCreate import manejarComandoCreate
from comandos.comandoAll import manejarComandoAll
from comandos.comandoAdd import manejarComandoAdd
from comandos.comandoDelete import manejarComandoDelete
from comandos.comandoList import manejarComandoList
from comandos.comandoNext import manejarComandoNext
from comandos.comandoRemove import manejarComandoRemove
from comandos.comandoHelp import manejarComandoHelp
from comandos.comandoPrint import manejarComandoPrint

# Datos administrativos del bot
cliente = discord.Client()

# Configs
canalOutputComandosID = Configs.CANAL_OUTPUT_COMANDOS_ID

prefijoBot = Configs.prefijoBot

comandoCreate = Configs.comandoCreate
comandoList = Configs.comandoList
comandoNext = Configs.comandoNext
comandoDelete = Configs.comandoDelete
comandoAdd = Configs.comandoAdd
comandoRemove = Configs.comandoRemove
comandoHelp = Configs.comandoHelp
comandoAll = Configs.comandoAll

emojis = Configs.emojis

canalSpamComandos = None


# Evento de inicializacion
@cliente.event
async def on_ready():
    global canalSpamComandos

    canalSpamComandos = cliente.get_channel(canalOutputComandosID)

    # Seteo variables globales
    GlobalVariables.canalOutputComandos = canalSpamComandos

    if canalSpamComandos is None:
        print("[ERROR] No se pudo encontrar el canal 'canalSpamComandos'")

    print('[Info] El bot ha sido cargado como el usurio: {0.user}'.format(
        cliente))
    await canalSpamComandos.send(
        "El bot ha sido inicializado correctamente como el usuario **{0.user}**".format(cliente))


# Evento de mensaje recibido
@cliente.event
async def on_message(message):
    mensajeSeparado = message.content.split(" ", 5)

    # Si el mensaje es enviado por el bot, o no esta presente el prefijo
    # Es importantisimo que este checkeo este antes de entrar al try, porque si llega a fallar aca,
    # genera un bucle infinito (cada mensaje que manda vuelve a entrar en el catch infinitamente)
    if message.author == cliente.user or not mensajeSeparado[0] == prefijoBot:
        return

    # Variables necesarias
    mensaje = message.content
    autorMensaje = message.author
    canal = message.channel
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    print("[Mensaje recibido] " + mensaje)

    try:
        # Si no inserto ningun segundo parametro
        if len(mensajeSeparado) == 1:
            await message.channel.send(
                f"Debes insertar algun comando. Usa `{prefijoBot} {comandoHelp}` para una lista de comandos."
            )
            return

        mensajeProcesadoConExito = False

        if mensajeSeparado[1] == comandoCreate:
            mensajeProcesadoConExito = await manejarComandoCreate(mensaje, autorMensaje, tagAlAutor, canal)
        elif mensajeSeparado[1] == comandoList:
            mensajeProcesadoConExito = await manejarComandoList(mensaje, autorMensaje, canal)
        elif mensajeSeparado[1] == comandoNext:
            mensajeProcesadoConExito = await manejarComandoNext(mensaje, autorMensaje, canal)
        elif mensajeSeparado[1] == comandoDelete:
            mensajeProcesadoConExito = await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor, canal)
        elif mensajeSeparado[1] == comandoAdd:
            mensajeProcesadoConExito = await manejarComandoAdd(
                mensaje, autorMensaje, tagAlAutor, message.author.voice, canal)
        elif mensajeSeparado[1] == comandoRemove:
            mensajeProcesadoConExito = await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor, canal)
        elif mensajeSeparado[1] == comandoHelp:
            mensajeProcesadoConExito = await manejarComandoHelp(canal)
        elif mensajeSeparado[1] == comandoAll:
            mensajeProcesadoConExito = await manejarComandoAll(autorMensaje, canal)
        elif mensajeSeparado[1] == "print":
            mensajeProcesadoConExito = await manejarComandoPrint(autorMensaje, canal)
        else:
            await message.channel.send(
                f"Comando no existente. Usa `{prefijoBot} {comandoHelp}` para una lista de comandos."
            )

        if mensajeProcesadoConExito:
            await message.add_reaction(emojis[4])
        else:
            await message.add_reaction(emojis[5])
    except Exception as e:
        await message.add_reaction(emojis[6])
        await message.channel.send(
            f"{tagAlAutor} Ha ocurrido un error inesperado procesando tu mensaje. Por favor vuelve a intentarlo."
        )
        print(f"Exception: {str(e)}")
        tb = traceback.format_exc()
        print(tb)


# Evento de reaccion recibida
@cliente.event
async def on_reaction_add(reaction, user):
    # No hago nada con cualquier reaccion hecha por el bot
    # Y Chequeo si la reaccion es a un mensaje enviado por el bot
    if user == cliente.user or not Colas.esAlgunaReaccionDeCola(reaction.message):
        return

    mensaje = prefijoBot + " "
    autorMensaje = user
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    # Variables necesarias
    nombreCola = reaction.message.embeds[0].title.split(" ",
                                                        2)[1].split(":", 1)[0]
    emoji = reaction.emoji

    canal = Colas.getColaPorNombre(nombreCola).canalMensaje
    # noinspection PyBroadException
    try:
        # Remuevo la reaccion generada por el usuario
        await reaction.remove(user)

        # Pulgar arriba
        if emoji == emojis[0]:
            mensaje += comandoAdd + " " + nombreCola

            print("[Add] " + mensaje)

            await manejarComandoAdd(
                mensaje, autorMensaje, tagAlAutor, user.voice, canal)
        # Pulgar abajo
        elif emoji == emojis[1]:
            mensaje += comandoRemove + " " + nombreCola

            print("[Remove] " + mensaje)

            await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor, canal)
        # Flecha hacia derecha
        elif emoji == emojis[2]:
            mensaje += comandoNext + " " + nombreCola

            print("[Next] " + mensaje)

            await manejarComandoNext(mensaje, autorMensaje, canal)
        # Cruz roja
        elif emoji == emojis[3]:
            mensaje += comandoDelete + " " + nombreCola

            print("[Delete] " + mensaje)

            await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor, canal)
    except Exception as e:
        await canal.send(
            f"{tagAlAutor} Ha ocurrido un error inesperado procesando tu mensaje. Por favor vuelve a intentarlo."
        )
        print(f"Exception: {str(e)}")
        tb = traceback.format_exc()
        print(tb)

# Corre el bot
cliente.run(Configs.DISCORD_TOKEN)
