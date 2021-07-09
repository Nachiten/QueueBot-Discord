class Usuario:
    # Objeto de discord con los datos del usuario
    objetoUsuario = None
    # Canal donde se encuentra
    canalActual = "NoInsertado"

    def __init__(self, objetoUsuario, canalActual):
        self.objetoUsuario = objetoUsuario
        self.canalActual = canalActual