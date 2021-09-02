import os

class Configs:

    # ############################################################### #

    # ### Campos que deben estar seteados como Envarioment (.env) ### #
    # Ubicacion de .env, esta misma carpeta

    # Discord Token | String | Token unico del bot de dicord
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    # Canal Spam Comandos | Int | Canal donde se le enviaran comandos al bot
    canalSpamComandosID = int(os.environ["canalSpamComandosID"])
    # Canal Output Bot | Int | Canal donde el bot enviara sus mensajes sobre la cola
    canalOutputBotID = int(os.environ["canalOutputBotID"])
    # Rangos Mod | [Int] | Ids de los rangos de moderacion que tendran permisos totales
    rangosMOD = list(map(int, os.environ["rangosMOD"].split("_")))

    # ############################################################### #

    # Emojis utilizados
    emojis = ['👍', '👎', '➡️', '❌']
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
