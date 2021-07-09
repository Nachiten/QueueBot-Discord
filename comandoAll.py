import discord

from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import colas
from utils import printearErrorSinPermisos

comandoAll = Configs.comandoAll
prefijoBot = Configs.prefijoBot
imagenThumbnail = Configs.imagenThumbnail


# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll(mensaje, autorMensaje, tagAlAutor):

    # Verificacion de mod
    if not esMod(autorMensaje):
        printearErrorSinPermisos(autorMensaje, comandoAll)
        return

    canalSpamComandos = GlobalVariables.canalSpamComandos

    mensaje = "No Hay ninguna cola."

    if len(colas) > 0:
        mensaje = ""

    for unaCola in colas:
        mensaje += str(unaCola[0]) + " | " + str(len(unaCola[1])) + "\n"

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Todas las colas:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url=imagenThumbnail)
    mensajeEmbed.add_field(name="Nombre de Cola | Cantidad de Miembros",
                           value=mensaje,
                           inline=False)

    await canalSpamComandos.send(embed=mensajeEmbed)
