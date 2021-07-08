import os
import discord

from configs import Configs
from globalVariables import GlobalVariables
from comandoCreate import manejarComandoCreate
from comandoAll import manejarComandoAll
from comandoAdd import manejarComandoAdd
from comandoDelete import manejarComandoDelete
from comandoList import manejarComandoList
from comandoNext import manejarComandoNext
from comandoRemove import manejarComandoRemove
from comandoHelp import manejarComandoHelp
from utils import colas

# Datos administrativos del bot
cliente = discord.Client()
token = os.environ['TOKEN']

# Configs
rangosMOD = Configs.rangosMOD
emojis = Configs.emojis
canalSpamComandosID = Configs.canalSpamComandosID
canalOutputBotID = Configs.canalOutputBotID
prefijoBot = Configs.prefijoBot

comandoCreate = Configs.comandoCreate
comandoList = Configs.comandoList
comandoNext = Configs.comandoNext
comandoDelete = Configs.comandoDelete
comandoAdd = Configs.comandoAdd
comandoRemove = Configs.comandoRemove
comandoHelp = Configs.comandoHelp
comandoAll = Configs.comandoAll

canalSpamComandos = None

async def chequearIntegridadDeMensaje(mensaje):
    if len(mensaje.split(" ", 7)) > 3:
        await canalSpamComandos.send("**[Error]** Ha ocurrido un error al procesar la solicitud de "
                                     + str(autorMensaje) + ". Por favor intente nuevamente.")


# Averigua si un mensaje pertenece a alguna cola de mensajes
def esAlgunaReaccionDeCola(mensaje):
    mensajesDeColas = map(lambda unaCola: unaCola[2], colas)
    return any(map(lambda unMensaje: unMensaje.id == mensaje.id, mensajesDeColas))


# Evento de inicializacion
@cliente.event
async def on_ready():
    global canalSpamComandos

    # Cargo los canales donde el bot hablara
    canalOutputBot = cliente.get_channel(canalOutputBotID)
    canalSpamComandos = cliente.get_channel(canalSpamComandosID)

    GlobalVariables.canalOutputBot = canalOutputBot
    GlobalVariables.canalSpamComandos = canalSpamComandos

    if canalSpamComandos is None:
        print("[ERROR] No se pudo encontrar el canal 'canalSpamComandos'")
    if canalOutputBot is None:
        print("[ERROR] No se pudo encontrar el canal 'canalOutputBot'")

    print('[Info] El bot ha sido cargado como el usurio: {0.user}'.format(
        cliente))
    await canalOutputBot.send("El bot ha sido inicializado correctamente como el usuario **{0.user}**".format(cliente))


# Evento de mensaje recibido
@cliente.event
async def on_message(message):
    # Cancelo la operacion si el mensaje es enviado por el mismo bot
    if message.author == cliente.user:
        return

    # Si no me invocaron ignoro el mensaje
    if not message.content.split(" ", 5)[0] == prefijoBot:
        return

    # Utilizando variables globales
    global mensaje
    global autorMensaje
    global tagAlAutor

    # Variables utiles
    mensaje = message.content
    print("[Mensaje recibido] " + mensaje)
    autorMensaje = message.author
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    # Comando para crear nueva cola [ONLY MODS]
    if mensaje.startswith(prefijoBot + " " + comandoCreate):
        await manejarComandoCreate(mensaje, autorMensaje, tagAlAutor)

    # Comando para listar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoList):
        await manejarComandoList(mensaje, autorMensaje, tagAlAutor)

    # Comando para obtener siguiente de la cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoNext):
        await manejarComandoNext(mensaje, autorMensaje, tagAlAutor)

    # Comando para eliminar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoDelete):
        await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor)

    # Comando para agregarse a una cola
    elif mensaje.startswith(prefijoBot + " " + comandoAdd):
        await manejarComandoAdd(mensaje, autorMensaje, tagAlAutor)

    # Comando para quitarse a uno mismo de una cola
    elif mensaje.startswith(prefijoBot + " " + comandoRemove):
        await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor)

    elif mensaje.startswith(prefijoBot + " " + comandoHelp):
        await manejarComandoHelp(mensaje, autorMensaje, tagAlAutor)

    elif mensaje.startswith(prefijoBot + " " + comandoAll):
        await manejarComandoAll(mensaje, autorMensaje, tagAlAutor)

    elif mensaje.startswith(prefijoBot):
        await message.channel.send("Comando no existente. Usa `" + prefijoBot +
                                   " " + comandoHelp +
                                   "` para una lista de comandos.")


# Evento de reaccion recibida
@cliente.event
async def on_reaction_add(reaction, user):
    # No hago nada con cualquier reaccion hecha por el bot
    if user == cliente.user:
        return

    # Chequeo si la reaccion es a un mensaje enviado por el bot
    if not esAlgunaReaccionDeCola(reaction.message):
        print("Reaccion no perteneciente al sistema.")
        return

    global mensaje
    global autorMensaje
    global tagAlAutor

    mensaje = prefijoBot + " "
    autorMensaje = user
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    # Variables necesarias
    nombreCola = reaction.message.embeds[0].title.split(" ",
                                                        2)[1].split(":", 1)[0]
    emoji = reaction.emoji

    # Remuevo la reaccion generada por el usuario
    await reaction.remove(user)

    if emoji == '👍':
        mensaje += comandoAdd + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Add] " + mensaje)

        await manejarComandoAdd(mensaje, autorMensaje, tagAlAutor)
    elif emoji == '👎':
        mensaje += comandoRemove + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Remove] " + mensaje)

        await manejarComandoRemove(mensaje, autorMensaje, tagAlAutor)
    elif emoji == '➡️':
        mensaje += comandoNext + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Next] " + mensaje)

        await manejarComandoNext(mensaje, autorMensaje, tagAlAutor)
    elif emoji == '❌':
        mensaje += comandoDelete + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Delete] " + mensaje)

        await manejarComandoDelete(mensaje, autorMensaje, tagAlAutor)
    else:
        return


# Corre el bot
cliente.run(token)
