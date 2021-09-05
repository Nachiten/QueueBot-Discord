import discord

from configs.globalVariables import GlobalVariables
from configs.configs import Configs

PREFIX = Configs.prefijoBot
COMANDO_ADD = Configs.comandoAdd
COMANDO_REMOVE = Configs.comandoRemove
COMANDO_NEXT = Configs.comandoNext
COMANDO_DELETE = Configs.comandoDelete
COMANDO_LIST = Configs.comandoList
COMANDO_ALL = Configs.comandoAll
COMANDO_CREATE = Configs.comandoCreate
imagenThumbnail = Configs.imagenThumbnail
emojis = Configs.emojis


def generarMensajeEmbed():
    # Creacion de mensaje embed
    mensajeEmbed = discord.Embed(title="Lista de comandos:",
                                 color=discord.Color.purple())
    mensajeEmbed.set_thumbnail(url=imagenThumbnail)
    mensajeEmbed.add_field(name="Comandos para Alumnos:",
                           value=f'''
                           {PREFIX} {COMANDO_ADD} unaCola | Agregarse a una cola
                           {PREFIX} {COMANDO_REMOVE} unaCola | Quitarse de una cola
                           ''',
                           inline=False)
    mensajeEmbed.add_field(name="Comandos para Ayudantes:",
                           value=f'''
                           {PREFIX} {COMANDO_CREATE} unaCola | Crear una nueva cola
                           {PREFIX} {COMANDO_DELETE} unaCola | Eliminar una cola
                           {PREFIX} {COMANDO_NEXT} unaCola | Atender el siguiente en una cola
                           {PREFIX} {COMANDO_LIST} unaCola | Mostrar estado de la cola
                           {PREFIX} {COMANDO_ALL} | Mostrar todas las colas existentes
                           ''',
                           inline=False)
    mensajeEmbed.add_field(
        name="Emojis:",
        value=f"[{emojis[0]}] add | [{emojis[1]}] remove | [{emojis[2]}] next | [{emojis[3]}] delete",
        inline=False)
    mensajeEmbed.set_footer(
        text=
        "Tener en cuenta que los mensajes de las colas se actualizan automaticamente una vez enviados."
    )

    return mensajeEmbed


# Description: Mostrar mensaje de ayuda
# Access: Everyone
async def manejarComandoHelp():
    canalSpamComandos = GlobalVariables.canalSpamComandos

    mensajeEmbed = generarMensajeEmbed()

    await canalSpamComandos.send(embed=mensajeEmbed)

    return True
