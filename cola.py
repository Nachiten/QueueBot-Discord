import discord

from usuario import Usuario
from globalVariables import GlobalVariables
from configs import Configs

emojis = Configs.emojis
imagenThumbnail = Configs.imagenThumbnail


# Estructura sobre una cola del sistema
class Cola:
    # Nombre de la cola
    nombre = "DefaultName"
    # Lista de usuarios en la cola
    usuarios = []
    # Mensaje enviado de la cola
    mensajeEnviado = None

    def __init__(self, nombreCola):
        self.nombre = nombreCola

    # Agregar un usuario a la cola
    def agregarUsuario(self, usuario):
        self.usuarios.append(Usuario(
            usuario,
            "--"))  # TODO | Implementar el manejar en que canal se encuentra

    def obtenerUsuario(self, usuario):
        for unUsuario in self.usuarios:
            if unUsuario.objetoUsuario == usuario:
                return unUsuario
        print("[ERROR] No deberia no poder encontrar un usuario")

    # Quitar un usuario de la cola
    def quitarUsuario(self, usuario):
        usuarioBuscado = self.obtenerUsuario(usuario)

        self.usuarios.remove(usuarioBuscado)

    # Actualizar el mensaje enviado de la cola
    async def enviarMensajeNuevo(self):
        canalOutputBot = GlobalVariables.canalOutputBot

        # Genero embed a enviar
        embedCompleto = self.generarMensajeEmbed()

        # Obtengo mensaje anterior a enviar
        mensajeDeCola = self.mensajeEnviado

        # Checkeo si existe un mensaje anterior
        if not mensajeDeCola == None:
            # Lo borro
            await mensajeDeCola.delete()

        # Envio y registro el mensaje enviado
        self.mensajeEnviado = await canalOutputBot.send(embed=embedCompleto)

        # Reacciono con emojis para que el resto pueda hacerlo
        for emoji in emojis:
            await self.mensajeEnviado.add_reaction(emoji)

    # Actualiza el embed de una cola
    async def actualizarMensajeExistente(self):
        # Genero embed a enviar
        embedCompleto = self.generarMensajeEmbed()

        # Obtengo mensaje anterior a enviar
        mensajeDeCola = self.mensajeEnviado

        # Checkeo que no sea null para evitar excepciones
        if not mensajeDeCola == None:
            # Edito el mensaje
            await mensajeDeCola.edit(embed=embedCompleto)

    # Eliminar el mensaje embed de la cola
    async def eliminarMensaje(self):
        # Checkeo que no sea null para evitar excepciones
        if not self.mensajeEnviado == None:
            # Borro el mensaje
            await self.mensajeEnviado.delete()

    # Genera el mensaje embed a enviar
    def generarMensajeEmbed(self):
        # Lista de miembros de la cola actual (posible que sea vacia)
        miembrosCola = self.usuarios

        # Valores default de siguientes personas
        siguienteMiembro = "No quedan mas personas de la cola."
        miembrosAContinuacion = "No hay mas miembros a continuacion."

        # Si hay al menos un miembro, fijo el primero de la cola
        if len(miembrosCola) > 0:
            siguienteMiembro = "1) " + "<@" + str(miembrosCola[0].objetoUsuario.id) + ">"

        # Si hay mas de un miembro, fijo los a continuacion
        if len(miembrosCola) > 1:
            miembrosAContinuacion = ""

            for index in range(1, len(miembrosCola)):
                miembrosAContinuacion += str(index) + ") <@" + str(
                    miembrosCola[index].objetoUsuario.id) + ">\n"

        # Creacion de mensaje embed
        mensajeEmbed = discord.Embed(title="Cola " + self.nombre + ":",
                                     color=discord.Color.purple())
        mensajeEmbed.set_thumbnail(url=imagenThumbnail)
        mensajeEmbed.add_field(name="Siguiente turno:",
                               value=siguienteMiembro,
                               inline=False)
        mensajeEmbed.add_field(name="A continuacion:",
                               value=miembrosAContinuacion,
                               inline=False)
        mensajeEmbed.set_footer(
            text=
            "Usá los emojis para reaccionar y agregarte o quitarte de la cola."
        )

        return mensajeEmbed

    def existeUsuario(self, usuario):
        return usuario in map(lambda unUsuario : unUsuario.objetoUsuario, self.usuarios)

    def cantidadDeUsuarios(self):
        return len(self.usuarios)

    # Obtener y quitar de la lista de usuarios el siguiente
    def obtenerYQuitarIdDeSiguiente(self):
        return self.usuarios.pop(0).objetoUsuario.id

    # Solo leer sin tocar el siguiente de la cola
    def obtenerIdDeSiguiente(self):
        return self.usuarios[0].objetoUsuario.id

    def perteneceElMensaje(self, mensaje):
        return mensaje.id == self.mensajeEnviado.id
