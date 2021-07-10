import discord

from cola import Cola
from configs import Configs

imagenThumbnail = Configs.imagenThumbnail


# Clase estatica
# Mantiene una lista de todas las colas del sistema
class Colas:
    # Las colas existentes del sitema
    colasActuales = []

    # Agregar una nueva cola
    @classmethod
    def agregarCola(self, nombreCola):
        self.colasActuales.append(Cola(nombreCola))

    # Quitar una cola existente
    @classmethod
    def quitarCola(self, nombreCola):
        self.colasActuales.remove(self.getColaPorNombre(nombreCola))

    # Obtener una cola dado el nombre
    @classmethod
    def getColaPorNombre(self, nombreCola):
        return self.colasActuales[self.indexDeCola(nombreCola)]

    # Obtener el index de una cola dado el nombre
    @classmethod
    def indexDeCola(self, nombreCola):
        index = 0

        for unaCola in self.colasActuales:
            if unaCola.nombre == nombreCola:
                return index
            index += 1
        print("[ERROR] No se encontro una cola que si deberia.")

    @classmethod
    def generarMensajeListandoColas(self):
        mensaje = "No Hay ninguna cola."

        if len(self.colasActuales) > 0:
            mensaje = ""
            for unaCola in self.colasActuales:
                mensaje += str(unaCola[0]) + " | " + str(len(
                    unaCola[1])) + "\n"

        # Creacion de mensaje embed
        mensajeEmbed = discord.Embed(title="Todas las colas:",
                                     color=discord.Color.purple())
        mensajeEmbed.set_thumbnail(url=imagenThumbnail)
        mensajeEmbed.add_field(name="Nombre de Cola | Cantidad de Miembros",
                               value=mensaje,
                               inline=False)

        return mensajeEmbed

    @classmethod
    def existeCola(self, nombreCola):
        return nombreCola in map(lambda unaCola: unaCola.nombre,
                                 self.colasActuales)

    @classmethod
    def agregarUsuarioACola(self, usuario, nombreCola):
        self.getColaPorNombre(nombreCola).agregarUsuario(usuario)

    @classmethod
    def quitarUsuarioDeCola(self, usuario, nombreCola):
        self.getColaPorNombre(nombreCola).quitarUsuario(usuario)

    @classmethod
    def existeUsuarioEnCola(self, nombreUsuario, nombreCola):
        return self.getColaPorNombre(nombreCola).existeUsuario(nombreUsuario)

    @classmethod
    # Averigua si un mensaje pertenece a alguna cola de mensajes
    def esAlgunaReaccionDeCola(self, mensaje):
        return any(
            map(lambda unaCola: unaCola.perteneceElMensaje(mensaje),
                self.colasActuales))

    # --- Son awaited porque envian mensajes ---

    @classmethod
    async def enviarMensajeNuevoEnCola(self, nombreCola):
        await self.getColaPorNombre(nombreCola).enviarMensajeNuevo()

    @classmethod
    async def actualizarMensajeExistenteEnCola(self, nombreCola):
        await self.getColaPorNombre(nombreCola).actualizarMensajeExistente()

    @classmethod
    async def eliminarMensajeEnCola(self, nombreCola):
        await self.getColaPorNombre(nombreCola).eliminarMensaje()

    @classmethod
    async def enviarMensajeNextEnCola(self, nombreCola, canalOutputBot):
        await self.getColaPorNombre(nombreCola).enviarMensajeNext(
            canalOutputBot)

    # --- Son awaited porque envian mensajes ---
