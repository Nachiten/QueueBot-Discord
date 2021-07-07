import os
import discord

# String que tageua al usuario "usuario"
# "<@" + str(usuario.id) + ">"

# Como se debe invocar al bot
prefijoBot = "!queue"

# Aliases de comandos
comandoCreate = "create"
comandoList = "list"
comandoNext = "next"
comandoDelete = "delete"
comandoAdd = "add"
comandoRemove = "remove"

# Lista de todas las colas
# Una cola es de la forma ("nombre", [usuario1, usuario2, usuarioN], mensajeEnviado)
colas = []

# Ids de los rangos de moderacion que tendran permisos totales
ayudanteID = 862332264830074891
# Canal donde enviará mensajes el bot
canalGeneralID = 597165801346301982
emojis = ['👍', '👎', '➡️', '❌']

# Datos administrativos del bot
cliente = discord.Client()
token = os.environ['TOKEN']

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


def quitarDeCola(nombreCola, autorMensaje):
    indexCola = indexDeCola(nombreCola)
    colas[indexCola][1].remove(autorMensaje)


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


# Saber si un miembro esta en una cola dado elnombre
def existeMiembroEnCola(miembro, nombreCola):
    return miembro in colas[indexDeCola(nombreCola)][1]


# Verifica si un usuario tiene el rango de ayudante
def esMod(unUsuario):
    for unRol in unUsuario.roles:
        if unRol.id == ayudanteID:
            return True
    return False


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

def agregarMensajeEnCola(mensaje, nombreCola):
    colaActual = colas[indexDeCola(nombreCola)]
    colas[indexDeCola(nombreCola)] = (colaActual[0], colaActual[1], mensaje)

def obtenerMensajeDeCola(nombreCola):
    return colas[indexDeCola(nombreCola)][2]


# Evento de inicializacion
@cliente.event
async def on_ready():
    print('El bot ha sido cargado como el usurio: {0.user}'.format(cliente))


# [Solo Mods]
async def manejarComandoCreate(canalAEnviar):
    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        await canalAEnviar.send("No tenes permiso para usar este comando.")
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue "+ comandoCreate +" nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if (existeCola(nombreCola)):
        await canalAEnviar.send("Ya existe una cola con el nombre " +
                                nombreCola + "!")
    else:
        colas.append((nombreCola, [], None))
        await canalAEnviar.send(tagAlAutor +
                                " ha creado una nueva cola llamada: " +
                                str(nombreCola) + ".")

        embedCompleto = generarEmbedDeCola(nombreCola)

        mensajeEnviado = await canalAEnviar.send(embed=embedCompleto)

        agregarMensajeEnCola(mensajeEnviado, nombreCola)

        for emoji in emojis:
            await mensajeEnviado.add_reaction(emoji)


# [Solo Mods]
async def manejarComandoList(canalAEnviar):
    if not esMod(autorMensaje):
        await canalAEnviar.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue list nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalAEnviar.send("No existe la cola " + nombreCola + "!")
    else:
        embedCompleto = generarEmbedDeCola(nombreCola)

        mensajeEnviado = await canalAEnviar.send(embed=embedCompleto)

        agregarMensajeEnCola(mensajeEnviado, nombreCola)

        for emoji in emojis:
            await mensajeBot.add_reaction(emoji)


# [Solo Mods]
async def manejarComandoNext(canalAEnviar):
    parametrosMensaje = mensaje.split(" ", 5)

    if not esMod(autorMensaje):
        await canalAEnviar.send("No tenes permiso para usar este comando.")
        return

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue next nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalAEnviar.send("No existe la cola " + nombreCola + "!")
    else:
        if len(colas[indexDeCola(nombreCola)][1]) == 0:
            await canalAEnviar.send("No quedan miembros en la cola " + nombreCola +
                                    ".")
            return
        else:
            # Calculo los siguientes para printearlos
            siguienteEnLaLista = "<@" + str(
                colas[indexDeCola(nombreCola)][1].pop(0).id) + ">"
            siguienteAlSiguienteEnLaLista = "{Nadie}"

            if len(colas[indexDeCola(nombreCola)][1]) >= 1:
                siguienteAlSiguienteEnLaLista = "<@" + str(
                    colas[indexDeCola(nombreCola)][1][0].id) + ">"
            
            await canalAEnviar.send(siguienteEnLaLista +
                                    " es tu turno. El siguiente en la cola es " +
                                    siguienteAlSiguienteEnLaLista + ".")
            await actualizarQueue(nombreCola)


# [Solo Mods]
async def manejarComandoDelete(canalAEnviar):
    if not esMod(autorMensaje):
        await canalAEnviar.send("No tenes permiso para usar este comando.")
        return

    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue delete nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalAEnviar.send("No existe la cola " + nombreCola + "!")
    else:
        eliminarCola(nombreCola)
        await canalAEnviar.send(tagAlAutor + " ha eliminado la cola " +
                                nombreCola + ".")
        if not mensajeBot == None:
            await mensajeBot.delete()


async def manejarComandoAdd(canalAEnviar):
    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue add nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalAEnviar.send("No existe la cola " + nombreCola + "!")
    else:
        if existeMiembroEnCola(autorMensaje, nombreCola):
            await canalAEnviar.send(tagAlAutor + " Ya estas en la cola " +
                                    nombreCola + "!")
        else:
            agregarACola(nombreCola, autorMensaje)
            await canalAEnviar.send(tagAlAutor +
                                    " ha sido agregado a la cola " +
                                    nombreCola + ".")
            await actualizarQueue(nombreCola)
            

async def manejarComandoRemove(canalAEnviar):
    parametrosMensaje = mensaje.split(" ", 5)

    # Solo debe haber tres parametros {!queue}, {create}, {elNombre}
    if not cantidadDeParametrosEs(3, parametrosMensaje):
        await canalAEnviar.send(
            "Sintaxis incorrecta, uso: !queue remove nombreCola")
        return

    nombreCola = parametrosMensaje[2]

    if not existeCola(nombreCola):
        await canalAEnviar.send("No existe la cola " + nombreCola + "!")
    else:
        if not existeMiembroEnCola(autorMensaje, nombreCola):
            await canalAEnviar.send(tagAlAutor + " No estas en la cola " +
                                    nombreCola + "!")
        else:
            quitarDeCola(nombreCola, autorMensaje)
            await canalAEnviar.send(tagAlAutor +
                                    " ha sido quitado de la cola " +
                                    nombreCola + ".")
            await actualizarQueue(nombreCola)


async def actualizarQueue(nombreCola):
    embedCompleto = generarEmbedDeCola(nombreCola)

    mensajeDeCola = obtenerMensajeDeCola(nombreCola)

    if not mensajeDeCola == None:
        await mensajeDeCola.edit(embed = embedCompleto)

# Evento de mensaje recibido
@cliente.event
async def on_message(message):

    global autorMensaje
    autorMensaje = message.author

    # Cancelo la operacion si el mensaje es enviado por el mismo bot
    if autorMensaje == cliente.user:
        return

    # Utilizando variables globales
    global mensaje
    global tagAlAutor

    # Variables utiles
    mensaje = message.content
    tagAlAutor = "<@" + str(autorMensaje.id) + ">"

    canalGeneral = cliente.get_channel(canalGeneralID)

    # Comando para crear nueva cola [ONLY MODS]
    if mensaje.startswith(prefijoBot + " " + comandoCreate):
        await manejarComandoCreate(canalGeneral)

    # Comando para listar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoList):
        await manejarComandoList(canalGeneral)

    # Comando para obtener siguiente de la cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoNext):
        await manejarComandoNext(canalGeneral)

    # Comando para eliminar una cola [ONLY MODS]
    elif mensaje.startswith(prefijoBot + " " + comandoDelete):
        await manejarComandoDelete(canalGeneral)

    # Comando para agregarse a una cola
    elif mensaje.startswith(prefijoBot + " " + comandoAdd):
        await manejarComandoAdd(canalGeneral)

    # Comando para quitarse a uno mismo de una cola
    elif mensaje.startswith(prefijoBot + " " + comandoRemove):
        await manejarComandoRemove(canalGeneral)


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
    tagAlAutor = "<@" + str(user.id) + ">"

    # Variables necesarias
    nombreCola = reaction.message.embeds[0].title.split(" ", 3)[2]
    canalGeneral = cliente.get_channel(canalGeneralID)
    emoji = reaction.emoji

    # Remuevo la reaccion generada por el usuario
    await reaction.remove(user)

    if emoji == '👍':
        mensaje += comandoAdd + " " + nombreCola
        await manejarComandoAdd(canalGeneral)
    elif emoji == '👎':
        mensaje += comandoRemove + " " + nombreCola
        await manejarComandoRemove(canalGeneral)
    elif emoji == '➡️':
        mensaje += comandoNext + " " + nombreCola
        await manejarComandoNext(canalGeneral)
    elif emoji == '❌':
        mensaje += comandoDelete + " " + nombreCola
        await manejarComandoDelete(canalGeneral)
    else:
        return


cliente.run(token)
