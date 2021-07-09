import discord

from configs import Configs
from globalVariables import GlobalVariables

# Configs
rangosMOD = Configs.rangosMOD
emojis = Configs.emojis
imagenThumbnail = Configs.imagenThumbnail

# Lista de todas las colas
# Una cola es de la forma ("nombre", [usuario1, usuario2, usuarioN], mensajeEnviado)
colas = []


# Obtiene el index de una cola dentro del array de estas
def indexDeCola(nombreCola):
    index = 0

    for unaCola in colas:
        if unaCola[0] == nombreCola:
            return index
        index += 1
    print("[ERROR] No se encontro una cola que si deberia.")


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

async def printearErrorSinPermisos(autorMensaje, nombreComando):
    canalSpamComandos = GlobalVariables.canalSpamComandos
    print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoAll + ".")
    await canalSpamComandos.send("No tenes permiso para usar este comando.")

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
            miembrosAContinuacion += str(index) + ") <@" + str(
                miembrosCola[index].id) + ">\n"

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Cola " + nombreCola + ":",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url=imagenThumbnail)
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


# Envia un nuevo embed de una cola
async def enviarMensajeCola(nombreCola):
    canalOutputBot = GlobalVariables.canalOutputBot

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
