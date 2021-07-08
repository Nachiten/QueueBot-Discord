import discord

from globalVariables import GlobalVariables

# Description: Mostrar mensaje de ayuda
# Access: Everyone
async def manejarComandoHelp(mensaje, autorMensaje, tagAlAutor):
    
    canalSpamComandos = GlobalVariables.canalSpamComandos
    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Lista de comandos:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url="https://i.imgur.com/FU1z6dq.png")
    mensajeEmbed.add_field(
        name="Comandos para todos:",
        value=
        "!queue add unaCola | Agregarse a una cola\n!queue remove unaCola | Quitarse de una cola",
        inline=False)
    mensajeEmbed.add_field(
        name="Comandos para Ayudantes:",
        value="!queue create unaCola | Crear una nueva cola\n"
        "!queue delete unaCola | Eliminar una cola\n"
        "!queue next unaCola | Atender el siguiente en una cola\n"
        "!queue list unaCola | Mostrar estado de la cola\n"
        "!queue all | Mostrar todas las colas existentes",
        inline=False)
    mensajeEmbed.add_field(
        name="Emojis:",
        value="[👍] add | [👎] remove | [➡️] next | [❌] delete",
        inline=False)
    mensajeEmbed.set_footer(
        text=
        "Tener en cuenta que los mensajes de las colas se actualizan automaticamente una vez enviados."
    )

    await canalSpamComandos.send(embed=mensajeEmbed)