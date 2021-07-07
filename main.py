import os
import discord

from configs import Config

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


# Elimina una cola de la lista
def eliminarCola(nombreCola):
    for unaCola in colas:
        if unaCola[0] == nombreCola:
            colas.remove(unaCola)
            return
    print("[ERROR] No fue encontrada la cola que deberia existir")


# Agrega nuevo miembro a una cola
def agregarACola(nombreCola, autorMensaje):
    indexCola = indexDeCola(nombreCola)
    colas[indexCola][1].append(autorMensaje)


# Quita un mibmro de una cola
def quitarDeCola(nombreCola, autorMensaje):
    indexCola = indexDeCola(nombreCola)
    colas[indexCola][1].remove(autorMensaje)


# Verifica la cantidad de parametros de un comando
def cantidadDeParametrosEs(numero, parametros):
    return len(parametros) == numero and stringEsValido(parametros[numero - 1])


# Saber si un parametro solo son espacios y no es valido
def stringEsValido(string):
    return not (string == "" or string == " ")


# Verifica existencia de una cola
def existeCola(nombreCola):
    nombresColas = map(lambda unaCola : unaCola[0], colas)
    return nombreCola in nombresColas


# Saber si un miembro esta en una cola dado elnombre
def existeMiembroEnCola(miembro, nombreCola):
    return miembro in colas[indexDeCola(nombreCola)][1]


# Verifica si un usuario tiene el rango de ayudante
def esMod(unUsuario):
    for unRol in unUsuario.roles:
        if unRol.id in rangosMOD:
            return True
    return False

# Genera el mensaje embed a enviar
def generarEmbedDeCola(nombreCola):
    # Lista de miembros de la cola actual (posible que sea vacia)
    miembrosCola = colas[indexDeCola(nombreCola)][1]

    # Valores default de siguientes personas
    siguienteMiembro = "No quedan mas personas de la cola."
    mensajeCompleto = "No hay mas miembros a continuacion."

    # Si hay al menos un miembro, fijo el primero de la cola
    if len(miembrosCola) > 0:
        siguienteMiembro = "1) " + "<@" + str(miembrosCola[0].id) + ">"

    # Si hay mas de un miembro, fijo los a continuacion
    if len(miembrosCola) > 1:
        mensajeCompleto = ""
        index = 1

        for persona in miembrosCola:
            if index == 1:
                index += 1
                continue

            mensajeCompleto = mensajeCompleto + str(index) + ") <@" + str(
                persona.id) + ">\n"
            index += 1

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Cola Actual: " + nombreCola,
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(name="Siguiente turno:",
                           value=siguienteMiembro,
                           inline=False)
    mensajeEmbed.add_field(name="A continuacion:",
                           value=mensajeCompleto,
                           inline=False)
    mensajeEmbed.set_footer(
        text="Usá los emojis para reaccionar y agregarte a la cola.")

    return mensajeEmbed

# Agrega un mensaje en una cola
def agregarMensajeEnCola(mensaje, nombreCola):
    colaActual = colas[indexDeCola(nombreCola)]
    colas[indexDeCola(nombreCola)] = (colaActual[0], colaActual[1], mensaje)

# Obtiene el mensaje de una cola
def obtenerMensajeDeCola(nombreCola):
    return colas[indexDeCola(nombreCola)][2]


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
    
    print('El bot ha sido cargado como el usurio: {0.user}'.format(cliente))


# Description: Crea un nueva cola
# Access: Only Mods
async def manejarComandoCreate():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send("Sintaxis incorrecta, uso: !queue " +
                                comandoCreate + " nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if (existeCola(nombreCola)):
        await canalSpamComandos.send("Ya existe una cola con el nombre " +
                                nombreCola + "!")
    else:
        colas.append((nombreCola, [], None))
        await canalSpamComandos.send(tagAlAutor +
                                " ha creado una nueva cola llamada: " +
                                str(nombreCola) + ".")
        await enviarMensajeCola(nombreCola)


# Description: Muestra una cola por output-bot
# Access: Only Mods
async def manejarComandoList():
    global canalSpamComandos

    if not esMod(autorMensaje):
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            "Sintaxis incorrecta, uso: !queue list nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        await enviarMensajeCola(nombreCola)


# Description: Atender siguiente persona en una cola
# Access: Only Mods
async def manejarComandoNext():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            "Sintaxis incorrecta, uso: !queue next nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        if len(colas[indexDeCola(nombreCola)][1]) == 0:
            await canalSpamComandos.send("No quedan miembros en la cola " +
                                    nombreCola + ".")
            return
        else:
            # Calculo los siguientes para printearlos
            siguienteEnLaLista = "<@" + str(
                colas[indexDeCola(nombreCola)][1].pop(0).id) + ">"
            siguienteAlSiguienteEnLaLista = "{Nadie}"

            if len(colas[indexDeCola(nombreCola)][1]) >= 1:
                siguienteAlSiguienteEnLaLista = "<@" + str(
                    colas[indexDeCola(nombreCola)][1][0].id) + ">"

            await canalOutputBot.send(
                siguienteEnLaLista +
                " es tu turno. El siguiente en la cola es " +
                siguienteAlSiguienteEnLaLista + ".")
            await actualizarMensajeCola(nombreCola)


# Description: Eliminar una cola
# Access: Only Mods
async def manejarComandoDelete():
    global canalSpamComandos

    if not esMod(autorMensaje):
        await canalSpamComandos.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            "Sintaxis incorrecta, uso: !queue delete nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        eliminarCola(nombreCola)
        await canalSpamComandos.send(tagAlAutor + " ha eliminado la cola " +
                                nombreCola + ".")
        await eliminarMensajeCola(nombreCola)


# Description: Agregar una persona a una cola
# Access: Everyone
async def manejarComandoAdd():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            "Sintaxis incorrecta, uso: !queue add nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        if existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(tagAlAutor + " Ya estas en la cola " +
                                    nombreCola + "!")
        else:
            agregarACola(nombreCola, autorMensaje)
            await canalSpamComandos.send(tagAlAutor +
                                    " ha sido agregado a la cola " +
                                    nombreCola + ".")
            await actualizarMensajeCola(nombreCola)


# Description: Eliminar una persona de una cola
# Access: Everyone
async def manejarComandoRemove():
    global canalSpamComandos

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalSpamComandos.send(
            "Sintaxis incorrecta, uso: !queue remove nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalSpamComandos.send("No existe la cola " + nombreCola + "!")
    else:
        if not existeMiembroEnCola(autorMensaje, nombreCola):
            await canalSpamComandos.send(tagAlAutor + " No estas en la cola " +
                                    nombreCola + "!")
        else:
            quitarDeCola(nombreCola, autorMensaje)
            await canalSpamComandos.send(tagAlAutor +
                                    " ha sido quitado de la cola " +
                                    nombreCola + ".")
            await actualizarMensajeCola(nombreCola)

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


# Evento de mensaje recibido
@cliente.event
async def on_message(message):
    # Cancelo la operacion si el mensaje es enviado por el mismo bot
    if message.author == cliente.user:
        return

    # Utilizando variables globales
    global mensaje
    global autorMensaje
    global tagAlAutor
    
    # Variables utiles
    mensaje = message.content
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


# Evento de reaccion recibida
@cliente.event
async def on_reaction_add(reaction, user):

    # No hago nada con cualquier reaccion hecha por el bot
    if user == cliente.user:
        return

    # TODO | Falta checkear que se haya reaccionado al mensaje de lista enviado por el bot
    # Se entra aca para TODA reaccion del sistema

    global mensaje
    global autorMensaje
    global tagAlAutor

    mensaje = prefijoBot + " "
    autorMensaje = user
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    # Variables necesarias
    nombreCola = reaction.message.embeds[0].title.split(" ", 3)[2]
    emoji = reaction.emoji

    # Remuevo la reaccion generada por el usuario
    await reaction.remove(user)

    if emoji == '👍':
        mensaje += comandoAdd + " " + nombreCola
        await manejarComandoAdd()
    elif emoji == '👎':
        mensaje += comandoRemove + " " + nombreCola
        await manejarComandoRemove()
    elif emoji == '➡️':
        mensaje += comandoNext + " " + nombreCola
        await manejarComandoNext()
    elif emoji == '❌':
        mensaje += comandoDelete + " " + nombreCola
        await manejarComandoDelete()
    else:
        return

# Corre el bot
cliente.run(token)
