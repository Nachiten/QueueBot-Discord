import os

import discord

from configs import Config

# Configs
rangosMOD = Config.rangosMOD
emojis = Config.emojis
canalSpamComandosID = Config.canalSpamComandosID
canalOutputBotID = Config.canalOutputBotID
prefijoBot = Config.prefijoBot
comandoCreate = Config.comandoCreate
comandoList = Config.comandoList
comandoNext = Config.comandoNext
comandoDelete = Config.comandoDelete
comandoAdd = Config.comandoAdd
comandoRemove = Config.comandoRemove
comandoHelp = Config.comandoHelp
comandoAll = Config.comandoAll

# Datos administrativos del bot
cliente = discord.Client()
token = os.environ['TOKEN']

# Lista de todas las colas
# Una cola es de la forma ("nombre", [usuario1, usuario2, usuarioN], mensajeEnviado)
colas = []

# Variables globales necesarias
mensaje = None
autorMensaje = None
tagAlAutor = None


# Obtiene el index de una cola dentro del array de estas
def indexDeCola(nombreCola):
    index = 0

    for unaCola in colas:
        if unaCola[0] == nombreCola:
            return index
        index += 1
    print("[ERROR] No se encontro una cola que si deberia.")


# Elimina una cola de la lista
def eliminarCola(nombreCola):
    for unaCola in colas:
        if unaCola[0] == nombreCola:
            colas.remove(unaCola)
            return
    print("[ERROR] No fue encontrada la cola que deberia existir")


# Agrega nuevo miembro a una cola
def agregarACola(nombreCola, autorMensaje):
    colas[indexDeCola(nombreCola)][1].append(autorMensaje)


# Quita un miembro de una cola
def quitarDeCola(nombreCola, autorMensaje):
    colas[indexDeCola(nombreCola)][1].remove(autorMensaje)


# Verifica la cantidad de parametros de un comando
def cantidadDeParametrosEs(numero, parametros):
    return len(parametros) == numero and stringEsValido(parametros[numero - 1])


# Saber si un parametro solo son espacios y no es valido
def stringEsValido(string):
    return not (string == "" or string == " ")


# Verifica existencia de una cola
def existeCola(nombreCola):
    return nombreCola in map(lambda unaCola: unaCola[0], colas)


# Saber si un miembro esta en una cola dado el nombre
def existeMiembroEnCola(miembro, nombreCola):
    return miembro in colas[indexDeCola(nombreCola)][1]


# Verifica si un usuario tiene al menos un rango mod
def esMod(unUsuario):
    return any(map(lambda unRol: unRol.id in rangosMOD, unUsuario.roles))


# Genera el mensaje embed a enviar
def generarEmbedDeCola(nombreCola):
    # Lista de miembros de la cola actual (posible que sea vacia)
    miembrosCola = colas[indexDeCola(nombreCola)][1]

    # Valores default de siguientes personas
    siguienteMiembro = "No quedan mas personas de la cola."
    miembrosAContinuacion = "No hay mas miembros a continuacion."

    # Si hay al menos un miembro, fijo el primero de la cola
    if len(miembrosCola) > 0:
        siguienteMiembro = "1) " + "<@" + str(miembrosCola[0].id) + ">"

    # Si hay mas de un miembro, fijo los a continuacion
    if len(miembrosCola) > 1:
        miembrosAContinuacion = ""

        for index in range(1, len(miembrosCola)):
            miembrosAContinuacion += str(index) + ") <@" + str(miembrosCola[index].id) + ">\n"

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Cola " + nombreCola + ":",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(name="Siguiente turno:",
                           value=siguienteMiembro,
                           inline=False)
    mensajeEmbed.add_field(name="A continuacion:",
                           value=miembrosAContinuacion,
                           inline=False)
    mensajeEmbed.set_footer(
        text="Usá los emojis para reaccionar y agregarte o quitarte de la cola."
    )

    return mensajeEmbed


# Agrega un mensaje en una cola
def agregarMensajeEnCola(mensaje, nombreCola):
    colaActual = colas[indexDeCola(nombreCola)]
    colas[indexDeCola(nombreCola)] = (colaActual[0], colaActual[1], mensaje)


# Obtiene el mensaje de una cola
def obtenerMensajeDeCola(nombreCola):
    return colas[indexDeCola(nombreCola)][2]


# Description: Crea un nueva cola
# Access: Only Mods
async def manejarComandoCreate():
    global canalSpamComandos

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


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList():
    global canalSpamComandos

    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoList + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoList +
                                     " nombreCola`")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola + "**!")
    else:
        await enviarMensajeCola(nombreCola)


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoNext + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoNext +
                                     " nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola +
                                     "**!")
    else:
        if len(colas[indexDeCola(nombreCola)][1]) == 0:
            await canalOutputBot.send("No quedan miembros en la cola **" +
                                      nombreCola + "**.")
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


# Description: Eliminar una cola
# Access: Only Mods
async def manejarComandoDelete():
    global canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoDelete + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando."
                                     )
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoDelete +
                                     " nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola +
                                     "**!")
    else:
        await eliminarMensajeCola(nombreCola)
        eliminarCola(nombreCola)
        await canalSpamComandos.send(tagAlAutor + " ha eliminado la cola **" +
                                     nombreCola + "**.")


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoAdd +
                                     " nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        if existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(tagAlAutor +
                                         " Ya estas en la cola **" +
                                         nombreCola + "**!")
        else:
            agregarACola(nombreCola, autorMensaje)
            await canalSpamComandos.send(tagAlAutor +
                                         " ha sido agregado a la cola **" +
                                         nombreCola + "**.")
            await actualizarMensajeCola(nombreCola)


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: `" +
                                     prefijoBot + " " + comandoRemove +
                                     " + nombreCola`.")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola **" + nombreCola +
                                     "**!")
    else:
        if not existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(tagAlAutor +
                                         " No estas en la cola **" +
                                         nombreCola + "**!")
        else:
            quitarDeCola(nombreCola, autorMensaje)
            await canalSpamComandos.send(tagAlAutor +
                                         " ha sido quitado de la cola **" +
                                         nombreCola + "**.")
            await actualizarMensajeCola(nombreCola)


# Description: Mostrar mensaje de ayuda
# Access: Everyone
async def manejarComandoHelp():
    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Lista de comandos:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(
        name="Comandos para todos:",
        value=
        "!queue add unaCola | Agregarse a una cola\n!queue remove unaCola | Quitarse de una cola",
        inline=False)
    mensajeEmbed.add_field(
        name="Comandos para Ayudantes:",
        value="!queue create unaCola | Crear una nueva cola\n"
        "!queue delete unaCola | Eliminar una cola\n"
        "!queue next unaCola | Atender el siguiente en una cola\n"
        "!queue list unaCola | Mostrar estado de la cola\n"
        "!queue all | Mostrar todas las colas existentes",
        inline=False)
    mensajeEmbed.add_field(
        name="Emojis:",
        value="[👍] add | [👎] remove | [➡️] next | [❌] delete",
        inline=False)
    mensajeEmbed.set_footer(
        text=
        "Tener en cuenta que los mensajes de las colas se actualizan automaticamente una vez enviados."
    )

    await canalSpamComandos.send(embed=mensajeEmbed)


# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll():

    # Verificacion de mod
    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoAll + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando."
                                     )
        return

    mensaje = "No Hay ninguna cola."

    if len(colas) > 0:
        mensaje = ""

    for unaCola in colas:
        mensaje += str(unaCola[0]) + " | " + str(len(unaCola[1])) + "\n"

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Todas las colas:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(name="Nombre de Cola | Cantidad de Miembros",
                           value=mensaje,
                           inline=False)

    await canalSpamComandos.send(embed=mensajeEmbed)


# Envia un nuevo embed de una cola
async def enviarMensajeCola(nombreCola):
    global canalOutputBot

    # Genero embed a enviar
    embedCompleto = generarEmbedDeCola(nombreCola)

    # Obtengo el mensaje anterior que habia (potencialmente nulo)
    mensajeDeCola = obtenerMensajeDeCola(nombreCola)
    # Si existe, lo borro antes de enviar el nuevo
    if not mensajeDeCola == None:
        await mensajeDeCola.delete()

    # Envio el nuevo mensaje
    mensajeEnviado = await canalOutputBot.send(embed=embedCompleto)
    # Registro el mensaje enviado
    agregarMensajeEnCola(mensajeEnviado, nombreCola)

    # Reacciono con emojis para que el resto pueda hacerlo
    for emoji in emojis:
        await mensajeEnviado.add_reaction(emoji)


# Actualiza el embed de una cola
async def actualizarMensajeCola(nombreCola):
    # Genero embed a enviar
    embedCompleto = generarEmbedDeCola(nombreCola)

    # Obtengo mensaje anterior a enviar
    mensajeDeCola = obtenerMensajeDeCola(nombreCola)

    # Checkeo que no sea null para evitar excepciones
    if not mensajeDeCola == None:
        # Edito el mensaje
        await mensajeDeCola.edit(embed=embedCompleto)


# Elimina el embed de una cola
async def eliminarMensajeCola(nombreCola):
    # Obtengo el mensaje anterior
    mensajeDeCola = obtenerMensajeDeCola(nombreCola)

    # Checkeo que no sea null para evitar excepciones
    if not mensajeDeCola == None:
        # Borro el mensaje
        await mensajeDeCola.delete()


# Evento de inicializacion
@cliente.event
async def on_ready():
    global canalOutputBot
    global canalSpamComandos

    # Cargo los canales donde el bot hablara
    canalOutputBot = cliente.get_channel(canalOutputBotID)
    canalSpamComandos = cliente.get_channel(canalSpamComandosID)

    if canalSpamComandos == None:
        print("[ERROR] No se pudo encontrar el canal 'canalSpamComandos'")
    if canalOutputBot == None:
        print("[ERROR] No se pudo encontrar el canal 'canalOutputBot'")

    print('[Info] El bot ha sido cargado como el usurio: {0.user}'.format(
        cliente))
    await canalOutputBot.send(
        "El bot ha sido inicializado correctamente como el usuario **{0.user}**"
        .format(cliente))


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
        await manejarComandoCreate()

    # Comando para listar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoList):
        await manejarComandoList()

    # Comando para obtener siguiente de la cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoNext):
        await manejarComandoNext()

    # Comando para eliminar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoDelete):
        await manejarComandoDelete()

    # Comando para agregarse a una cola
    elif mensaje.startswith(prefijoBot + " " + comandoAdd):
        await manejarComandoAdd()

    # Comando para quitarse a uno mismo de una cola
    elif mensaje.startswith(prefijoBot + " " + comandoRemove):
        await manejarComandoRemove()

    elif mensaje.startswith(prefijoBot + " " + comandoHelp):
        await manejarComandoHelp()

    elif mensaje.startswith(prefijoBot + " " + comandoAll):
        await manejarComandoAll()

    elif mensaje.startswith(prefijoBot):
        await message.channel.send("Comando no existente. Usa `" + prefijoBot +
                                   " " + comandoHelp +
                                   "` para una lista de comandos.")

async def chequearIntegridadDeMensaje(mensaje):
    if len(mensaje.split(" ", 7)) > 3:
        await canalSpamComandos.send("**[Error]** Ha ocurrido un error al procesar la solicitud de " 
        + str(autorMensaje) + ". Por favor intente nuevamente.")


# Averigua si un mensaje pertenece a alguna cola de mensajes
def esAlgunaReaccionDeCola(mensaje):
    mensajesDeColas = map(lambda unaCola : unaCola[2], colas)
    return any(map(lambda unMensaje : unMensaje.id == mensaje.id, mensajesDeColas))

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

        await manejarComandoAdd()
    elif emoji == '👎':
        mensaje += comandoRemove + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Remove] " + mensaje)

        await manejarComandoRemove()
    elif emoji == '➡️':
        mensaje += comandoNext + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Next] " + mensaje)

        await manejarComandoNext()
    elif emoji == '❌':
        mensaje += comandoDelete + " " + nombreCola

        await chequearIntegridadDeMensaje(mensaje)
        print("[Delete] " + mensaje)

        await manejarComandoDelete()
    else:
        return


# Corre el bot
cliente.run(token)
