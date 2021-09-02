import discord

from configs.globalVariables import GlobalVariables
from configs.configs import Configs

from clases.usuario import Usuario

emojis = Configs.emojis
imagenThumbnail = Configs.imagenThumbnail


# Estructura sobre una cola del sistema
class Cola:

    # Constructor
    def __init__(self, nombreCola):
        # Nombre de la cola
        self.nombre = nombreCola
        # Lista de usuarios en la cola
        self.usuarios = []
        # Mensaje enviado de la cola
        self.mensajeEnviado = None

    # Agregar un usuario a la cola
    def agregarUsuario(self, usuario, canalActual):
        canalDeUsuario = canalActual

        if canalActual is None:
            canalDeUsuario = "CanalNoValido"
            print("[ERROR] No deberia llegar un canal no valido a esta instancia")

        self.usuarios.append(Usuario(usuario, str(canalDeUsuario)))

    # Quitar un usuario de la cola
    def quitarUsuario(self, usuario):
        self.usuarios.remove(self.obtenerUsuario(usuario))

    # Saber si existre un usuario dado
    def existeUsuario(self, usuario):
        return usuario in map(lambda unUsuario: unUsuario.objetoUsuario,
                              self.usuarios)

    # Obtener un usuario por nombre
    def obtenerUsuario(self, usuario):
        return list(
            filter(lambda unUsuario: unUsuario.objetoUsuario == usuario,
                   self.usuarios))[0]

    def obtenerListaDeUsuarios(self):
        mensaje = ""
        for unUsuario in self.usuarios:
            mensaje += f"Nombre: {unUsuario.objetoUsuario.name}\n"
        return mensaje

    # Cantidad total de usuarios
    def cantidadDeUsuarios(self):
        return len(self.usuarios)

    # Obtener y quitar de la lista de usuarios el siguiente
    def obtenerYQuitarSiguienteUsuario(self):
        return self.usuarios.pop(0)

    # Solo leer sin tocar el siguiente de la cola
    def obtenerSiguienteUsuario(self):
        return self.usuarios[0].objetoUsuario

    # Saber si un mensaje pertenece a esta cola
    def perteneceElMensaje(self, mensaje):
        return mensaje.id == self.mensajeEnviado.id

    # Generar el mensaje embed a enviar
    def generarMensajeEmbed(self):
        # Lista de miembros de la cola actual (posible que sea vacia)
        miembrosCola = self.usuarios

        # Valores default de siguientes personas
        siguienteMiembro = "No quedan mas personas de la cola."
        miembrosAContinuacion = "No hay mas miembros a continuacion."

        # Si hay al menos un miembro, fijo el primero de la cola
        if len(miembrosCola) > 0:
            siguienteMiembro = f"1) <@{str(miembrosCola[0].objetoUsuario.id)}> | Canal: {miembrosCola[0].canalActual}"

        # Si hay mas de un miembro, fijo los a continuacion
        if len(miembrosCola) > 1:
            miembrosAContinuacion = ""

            for index in range(1, len(miembrosCola)):
                miembrosAContinuacion += f"{str(index + 1)}) <@{str(miembrosCola[index].objetoUsuario.id)}> |" \
                                         f" Canal: {miembrosCola[index].canalActual}\n"

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

    # --- Son async porque envian mensajes ---

    # Enviar el mensaje sobre el siguiente turno
    async def enviarMensajeNext(self, canalOutputBot):
        if self.cantidadDeUsuarios() == 0:
            await canalOutputBot.send(
                f" No quedan miembros en la cola **{self.nombre}**.")
            return
        else:
            # Calculo los siguientes para printearlos
            siguienteUsuario = self.obtenerYQuitarSiguienteUsuario()

            siguienteEnLaLista = f"<@{str(siguienteUsuario.objetoUsuario.id)}>"
            siguienteAlSiguienteEnLaLista = "No hay nadie mas adelante en la cola."

            if self.cantidadDeUsuarios() >= 1:
                siguienteAlSiguienteEnLaLista = f" El siguiente en la cola es: " \
                                                f"<@{str(self.obtenerSiguienteUsuario().id)}>."

            await canalOutputBot.send(
                f"{siguienteEnLaLista} es tu turno en canal **{siguienteUsuario.canalActual}** en la cola"
                f" **{self.nombre}**.{siguienteAlSiguienteEnLaLista}"
            )
            await self.actualizarMensajeExistente()

    # Enviar un mensaje nuevo sobre la cola
    async def enviarMensajeNuevo(self):
        canalOutputBot = GlobalVariables.canalOutputBot

        # Genero embed a enviar
        embedCompleto = self.generarMensajeEmbed()

        # Obtengo mensaje anterior a enviar
        mensajeDeCola = self.mensajeEnviado

        # Checkeo si existe un mensaje anterior
        if mensajeDeCola is not None:
            # Lo borro
            await mensajeDeCola.delete()

        # Envio y registro el mensaje enviado
        self.mensajeEnviado = await canalOutputBot.send(embed=embedCompleto)

        # Reacciono con emojis para que el resto pueda hacerlo
        for emoji in emojis:
            await self.mensajeEnviado.add_reaction(emoji)

    # Actualizar el mensaje existente sobre la cola
    async def actualizarMensajeExistente(self):
        # Genero embed a enviar
        embedCompleto = self.generarMensajeEmbed()

        # Obtengo mensaje anterior a enviar
        mensajeDeCola = self.mensajeEnviado

        # Checkeo que no sea null para evitar excepciones
        if mensajeDeCola is not None:
            # Edito el mensaje
            await mensajeDeCola.edit(embed=embedCompleto)

    # Eliminar el mensaje existente sobre la cola
    async def eliminarMensaje(self):
        # Checkeo que no sea null para evitar excepciones
        if self.mensajeEnviado is not None:
            # Borro el mensaje
            await self.mensajeEnviado.delete()
