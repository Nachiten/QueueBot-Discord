import os


def obtenerCanal(envVar):
    return int(os.environ[envVar])


def obtenerRangos(envVar):
    return list(map(int, os.environ[envVar].split("_")))


class Configs:
    # ############################################################### #

    # ### Campos que deben estar seteados como Environment (bot.env) ### #

    # Discord Token | String | Token unico del bot de dicord
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    # Canal Spam Comandos | Int | Canal donde el bot hace output de los comandos recibidos
    CANAL_OUTPUT_COMANDOS_ID = obtenerCanal("CANAL_OUTPUT_COMANDOS_ID")
    # Canal Output Bot | Int | Canal donde el bot envia la informacion sobre las colas
    CANAL_OUTPUT_COLAS_ID = obtenerCanal("CANAL_OUTPUT_COLAS_ID")
    # Rangos Mod | [Int] | IDs de los rangos de moderacion que tendran permisos totales
    RANGOS_MOD = obtenerRangos("RANGOS_MOD")

    # ############################################################### #

    # Emojis utilizados | Los primeros 4 son para las colas, los otros dos para los mensajes enviados
    emojis = ['👍', '👎', '➡️', '❌', '✅', '❎', '💥']
    # Como se debe invocar al bot
    prefijoBot = "!queue"
    # Aliases de comandos
    comandoCreate = "create"
    comandoList = "list"
    comandoNext = "next"
    comandoDelete = "delete"
    comandoAdd = "add"
    comandoRemove = "remove"
    comandoHelp = "help"
    comandoAll = "all"
    # Comando de debug (por eso no aparece en help)
    comandoPrint = "print"
    imagenThumbnail = "https://i.imgur.com/LXStHiQ.png"
