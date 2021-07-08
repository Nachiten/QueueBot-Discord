import discord

from configs import Configs
from globalVariables import GlobalVariables

from utils import esMod
from utils import colas

comandoAll = Configs.comandoAll
prefijoBot = Configs.prefijoBot

# Description: Mostrar todas las colas existentes
# Access: Only Mods
async def manejarComandoAll(mensaje, autorMensaje, tagAlAutor):
    canalSpamComandos = GlobalVariables.canalSpamComandos

    # Verificacion de mod
    if not esMod(autorMensaje):
        print("[PermissionError] El usuario " + autorMensaje.name +
              " intento usar el comando " + comandoAll + ".")
        await canalSpamComandos.send("No tenes permiso para usar este comando."
                                     )
        return

    mensaje = "No Hay ninguna cola."

    if len(colas) > 0:
        mensaje = ""

    for unaCola in colas:
        mensaje += str(unaCola[0]) + " | " + str(len(unaCola[1])) + "\n"

    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Todas las colas:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(name="Nombre de Cola | Cantidad de Miembros",
                           value=mensaje,
                           inline=False)

    await canalSpamComandos.send(embed=mensajeEmbed)