from configs.globalVariables import GlobalVariables
from configs.configs import Configs

# Configs
rangosMOD = Configs.RANGOS_MOD
emojis = Configs.emojis
imagenThumbnail = Configs.imagenThumbnail


# Verifica la cantidad de parametros de un comando
def cantidadDeParametrosEs(numero, parametros):
    return len(parametros) == numero and stringEsValido(parametros[numero - 1])


# Saber si un parametro solo son espacios y no es valido
def stringEsValido(string):
    return not (string == "" or string == " ")


# Verifica si un usuario tiene al menos un rango mod
def esMod(unUsuario):
    return any(map(lambda unRol: unRol.id in rangosMOD, unUsuario.roles))


# Printea error cuando un usuario no tiene permisos para un comando
async def printearErrorSinPermisos(autorMensaje, nombreComando):
    canalSpamComandos = GlobalVariables.canalSpamComandos
    print("[PermissionError] El usuario " + autorMensaje.name +
          " intento usar el comando " + nombreComando + ".")
    await canalSpamComandos.send("No tenes permiso para usar este comando.")
