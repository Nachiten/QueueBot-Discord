import discord

from src.configs.configs import Configs

from src.clases.cola import Cola

imagenThumbnail = Configs.imagenThumbnail


# Clase estatica
# Mantiene una lista de todas las colas del sistema
class Colas:
    # Las colas existentes del sitema
    colasActuales = []

    # Agregar una nueva cola
    @classmethod
    def agregarCola(cls, nombreCola):
        cls.colasActuales.append(Cola(nombreCola))

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
    def agregarUsuarioACola(cls, usuario, nombreCola, canalActual):
        cls.getColaPorNombre(nombreCola).agregarUsuario(usuario, canalActual)

    @classmethod
    def quitarUsuarioDeCola(cls, usuario, nombreCola):
        cls.getColaPorNombre(nombreCola).quitarUsuario(usuario)

    @classmethod
    def existeUsuarioEnCola(cls, nombreUsuario, nombreCola):
        return cls.getColaPorNombre(nombreCola).existeUsuario(nombreUsuario)

    @classmethod
    # Averigua si un mensaje pertenece a alguna cola de mensajes
    def esAlgunaReaccionDeCola(cls, mensaje):
        return any(
            map(lambda unaCola: unaCola.perteneceElMensaje(mensaje),
                cls.colasActuales))

    @classmethod
    def cantidadDeColas(cls):
        return len(cls.colasActuales)

    @classmethod
    def eliminarTodasLasColas(cls):
        cls.colasActuales = []

    @classmethod
    def generarMensajeListandoColas(cls):
        nombresColas = "No Hay ninguna cola."
        cantidadUsuariosColas = "No Hay ninguna cola."

        if len(cls.colasActuales) > 0:
            nombresColas = ""
            cantidadUsuariosColas = ""
            for unaCola in cls.colasActuales:
                nombresColas += f"{str(unaCola.nombre)}\n"
                cantidadUsuariosColas += f"{str(unaCola.cantidadDeUsuarios())}\n"

        # Creacion de mensaje embed
        mensajeEmbed = discord.Embed(title="Todas las colas:",
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
    async def printearColas(cls, canalSpamComandos):
        mensaje = "```\nNo hay colas."

        if len(cls.colasActuales) > 0:
            mensaje = "```\n"

        for unaCola in cls.colasActuales:
            mensaje += f"Nombre Cola: {unaCola.nombre}\n"
            mensaje += f"Lista de usuarios:\n"
            mensaje += unaCola.obtenerListaDeUsuarios()
        mensaje += "\n```"

        await canalSpamComandos.send(mensaje)

    # --- Son awaited porque envian mensajes ---

    @classmethod
    async def enviarMensajeNuevoEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).enviarMensajeNuevo()

    @classmethod
    async def actualizarMensajeExistenteEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).actualizarMensajeExistente()

    @classmethod
    async def eliminarMensajeEnCola(cls, nombreCola):
        await cls.getColaPorNombre(nombreCola).eliminarMensaje()

    @classmethod
    async def enviarMensajeNextEnCola(cls, nombreCola, canalOutputBot):
        await cls.getColaPorNombre(nombreCola).enviarMensajeNext(
            canalOutputBot)
