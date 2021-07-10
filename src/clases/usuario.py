# Mantiene todos los datos sobre un usuario en una cola
class Usuario:
    def __init__(self, objetoUsuario, canalActual):
        # Objeto de discord con los datos del usuario
        self.objetoUsuario = objetoUsuario
        # Canal donde se encuentra
        self.canalActual = canalActual
