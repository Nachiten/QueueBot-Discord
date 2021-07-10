import discord

from cola import Cola
from configs import Configs

imagenThumbnail = Configs.imagenThumbnail


# Clase estatica
# Mantiene una lista de todas las colas del sistema
class Colas:
    # Las colas existentes del sitema
    colasActuales = []

    @classmethod
    async def printeameLasColas(self, canalSpamComandos):
        if len(self.colasActuales) == 0:
            await canalSpamComandos.send("No hay colas.")
            return

        for unaCola in self.colasActuales:
            await canalSpamComandos.send(f"Nombre Cola: {unaCola.nombre}\n")
            await canalSpamComandos.send(f"Lista de usuarios:\n")
            await unaCola.printearListaDeUsuarios(canalSpamComandos)

    # Obtener una cola dado el nombre
    @classmethod
    def getColaPorNombre(self, nombreCola):
        for unaCola in self.colasActuales:
            if unaCola.nombre == nombreCola:
                return unaCola
        print("[ERROR] No deberia no poder encontrarse una cola existente.")

    @classmethod
    def agregarCola(self, nombreCola):
        self.colasActuales.append(Cola(nombreCola))

    # Quitar una cola existente
    @classmethod
    def quitarCola(self, nombreCola):
        self.colasActuales.remove(self.getColaPorNombre(nombreCola))

    @classmethod
    def agregarUsuarioACola(self, usuario, nombreCola, canalActual):
        colaObtenida = self.getColaPorNombre(nombreCola)
        print("Cola a la que le agrego usuario: " + colaObtenida.nombre)
        colaObtenida.agregarUsuario(usuario, canalActual)

    @classmethod
    def quitarUsuarioDeCola(self, usuario, nombreCola):
        self.getColaPorNombre(nombreCola).quitarUsuario(usuario)

    @classmethod
    def existeCola(self, nombreCola):
        return nombreCola in map(lambda unaCola: unaCola.nombre,
                                 self.colasActuales)

    @classmethod
    def existeUsuarioEnCola(self, nombreUsuario, nombreCola):
        colaAUsar = self.getColaPorNombre(nombreCola)

        print(colaAUsar.nombre)

        return colaAUsar.existeUsuario(nombreUsuario)

    @classmethod
    # Averigua si un mensaje pertenece a alguna cola de mensajes
    def esAlgunaReaccionDeCola(self, mensaje):
        return any(
            map(lambda unaCola: unaCola.perteneceElMensaje(mensaje),
                self.colasActuales))

    @classmethod
    def generarMensajeListandoColas(self):
        nombresColas = "No Hay ninguna cola."
        cantidadUsuariosColas = "No Hay ninguna cola."

        if len(self.colasActuales) > 0:
            nombresColas = ""
            cantidadUsuariosColas = ""
            for unaCola in self.colasActuales:
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
