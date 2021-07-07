import os
import discord

# Tageua al autor del mensaje
# "<@" + str(message.author.id) + ">"

# Como se debe invocar al bot
prefijoBot = "!queue"

# Lista de todas las colas
# Una cola es de la forma ("nombre", [usuario1, usuario2, usuarioN])
colas = []


# Obtiene el index de una cola dentro del array de estas
def indexDeCola(nombreCola):
    index = 0

    for unaCola in colas:
        if unaCola[0] == nombreCola:
            return index
        index += 1


# Agrega nuevo miembro a una cola
def agregarACola(nombreCola, autorMensaje):
    indexCola = indexDeCola(nombreCola)
    colas[indexCola][1].append(autorMensaje)


# Verifica la cantidad de parametros de un comando
def cantidadDeParametrosEs(numero, parametros):
    return len(parametros) == numero and stringEsValido(parametros[numero - 1])


# Saber si un parametro solo son espacios y no es valido
def stringEsValido(string):
    return not (string == "" or string == " ")


#Obtiene el nombre de una cola
def nombreDe(unaCola):
    return unaCola[0]


# Verifica existencia de una cola
def existeCola(nombreCola):
    nombresColas = map(nombreDe, colas)

    return nombreCola in nombresColas


def existeMiembroEnCola(miembro, nombreCola):
    return miembro in colas[indexDeCola(nombreCola)][1]


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
        text="Usa los emojis para reaccionar y agregarte a la cola.")

    return mensajeEmbed


# Datos administrativos del bot
cliente = discord.Client()
token = os.environ['TOKEN']


# Evento de inicializacion
@cliente.event
async def on_ready():
    print('El bot ha sido cargado como el usurio: {0.user}'.format(cliente))


# Evento de mensaje recibido
@cliente.event
async def on_message(message):
    global nombreCola

    # Variables utiles
    mensaje = message.content
    autorMensaje = message.author
    tagAlAutor = "<@" + str(message.author.id) + ">"

    # Cancelo la operacion si el mensaje es enviado por el mismo bot
    if autorMensaje == cliente.user:
        return

    # Comando para testear
    if mensaje.startswith(prefijoBot + ' test'):
        await message.channel.send(tagAlAutor +
                                   " La prueba fue satisfactoria!")

    # Comando para crear nueva cola
    if mensaje.startswith(prefijoBot + ' create'):
        parametrosMensaje = mensaje.split(" ", 5)

        # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
        if not cantidadDeParametrosEs(3, parametrosMensaje):
            await message.channel.send(
                "Sintaxis incorrecta, uso: !queue create nombreCola")
            return

        nombreCola = parametrosMensaje[2]

        if (existeCola(nombreCola)):
            await message.channel.send("Ya existe una cola con el nombre " +
                                       nombreCola + "!")
        else:
            colas.append((nombreCola, []))
            await message.channel.send(tagAlAutor +
                                       " ha creado una nueva cola llamada: " +
                                       str(nombreCola) + ".")

    # Comando para agregarse a una cola
    if mensaje.startswith(prefijoBot + ' add'):

        parametrosMensaje = mensaje.split(" ", 5)

        # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
        if not cantidadDeParametrosEs(3, parametrosMensaje):
            await message.channel.send(
                "Sintaxis incorrecta, uso: !queue add nombreCola")
            return

        nombreCola = parametrosMensaje[2]

        if not existeCola(nombreCola):
            await message.channel.send("No existe la cola " + nombreCola + "!")
        else:
            if existeMiembroEnCola(autorMensaje, nombreCola):
                await message.channel.send(tagAlAutor +
                                           " Ya estas en la cola " +
                                           nombreCola + "!")
            else:
                agregarACola(nombreCola, autorMensaje)
                await message.channel.send(tagAlAutor +
                                           " ha sido agregado a la cola " +
                                           nombreCola + ".")

    # Comando para listar una cola
    if mensaje.startswith(prefijoBot + ' list'):

        parametrosMensaje = mensaje.split(" ", 5)

        # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
        if not cantidadDeParametrosEs(3, parametrosMensaje):
            await message.channel.send(
                "Sintaxis incorrecta, uso: !queue list nombreCola")
            return

        nombreCola = parametrosMensaje[2]

        if not existeCola(nombreCola):
            await message.channel.send("No existe la cola " + nombreCola + "!")
        else:
            embedCompleto = generarEmbedDeCola(nombreCola)
            await message.channel.send(embed=embedCompleto)

    # Comando para obtener siguiente de la cola
    if mensaje.startswith(prefijoBot + ' next'):
        pass

    # Comando para quitarse a uno mismo de una cola
    if mensaje.startswith(prefijoBot + ' remove'):
        pass

    # Comando para eliminar una cola
    if mensaje.startswith(prefijoBot + ' delete'):
        pass


cliente.run(token)
