import discord

from configs.configs import Configs

from clases.cola import Cola

imagenThumbnail = Configs.imagenThumbnail


# Clase estatica
# Mantiene una lista de todas las colas del sistema
class Colas:
    # Las colas existentes del sitema
    colasActuales = []

    @classmethod
    async def printeameLasColas(cls, canalSpamComandos):
        mensaje = "```\nNo hay colas."

        if len(cls.colasActuales) > 0:
            mensaje = "```\n"

        index = 0

        for unaCola in cls.colasActuales:
            mensaje += f"Cola {index}: {unaCola.nombre} | "
            mensaje += f"Usuarios: "
            mensaje += unaCola.obtenerListaDeUsuarios()
            index += 1
        mensaje += "\n```"

        await canalSpamComandos.send(mensaje)

    # Agregar una nueva cola
    @classmethod
    def agregarCola(cls, nombreCola, canalEnviado):
        cls.colasActuales.append(Cola(nombreCola, canalEnviado))

    # Quitar una cola existente
    @classmethod
    def quitarCola(cls, nombreCola):
        cls.colasActuales.remove(cls.getColaPorNombre(nombreCola))

    # Obtener una cola dado el nombre
    @classmethod
    def getColaPorNombre(cls, nombreCola):
        return list(filter(lambda unaCola: unaCola.nombre == nombreCola, cls.colasActuales))[0]

    @classmethod
    def existeCola(cls, nombreCola):
        return nombreCola in map(lambda unaCola: unaCola.nombre, cls.colasActuales)

    @classmethod
    def generarMensajeListandoColas(cls):
        nombresColas = "No hay ninguna cola."
        cantidadUsuariosColas = "n/a"

        if len(cls.colasActuales) > 0:
            nombresColas = ""
            cantidadUsuariosColas = ""
            for unaCola in cls.colasActuales:
                nombresColas += f"{str(unaCola.nombre)}\n"
                cantidadUsuariosColas += f"{str(unaCola.cantidadDeUsuarios())}\n"

        # Creacion de mensaje embed
        mensajeEmbed = discord.Embed(title="Colas existentes:",
                                     color=discord.Color.purple())
        mensajeEmbed.set_thumbnail(url=imagenThumbnail)
        mensajeEmbed.add_field(name="Nombre de Cola",
                               value=nombresColas,
                               inline=True)
        mensajeEmbed.add_field(name="Cantidad de Miembros",
                               value=cantidadUsuariosColas,
                               inline=True)

        return mensajeEmbed

    @classmethod
    def agregarUsuarioACola(cls, usuario, nombreCola, canalActual):
        cls.getColaPorNombre(nombreCola).agregarUsuario(usuario, canalActual)

    @classmethod
    def quitarUsuarioDeCola(cls, usuario, nombreCola):
        cls.getColaPorNombre(nombreCola).quitarUsuario(usuario)

    @classmethod
    def quitarUsuarioPorStringDeCola(cls, usuario, nombreCola):
        return cls.getColaPorNombre(nombreCola).quitarUsuarioPorString(usuario)

    @classmethod
    def existeUsuarioEnCola(cls, nombreUsuario, nombreCola):
        return cls.getColaPorNombre(nombreCola).existeUsuario(nombreUsuario)

    @classmethod
    # Averigua si un mensaje pertenece a alguna cola de mensajes
    def esAlgunaReaccionDeCola(cls, mensaje):
        return any(
            map(lambda unaCola: unaCola.perteneceElMensaje(mensaje),
                cls.colasActuales))

    # --- Son awaited porque envian mensajes ---

    @classmethod
    async def enviarMensajeNuevoEnCola(cls, nombreCola, channel):
        await cls.getColaPorNombre(nombreCola).enviarMensajeNuevo(channel)

    @classmethod
    async def actualizarMensajeExistenteEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).actualizarMensajeExistente()

    @classmethod
    async def eliminarMensajeEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).eliminarMensaje()

    @classmethod
    async def enviarMensajeNextEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).enviarMensajeNext()


