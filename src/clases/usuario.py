# Mantiene todos los datos sobre un usuario en una cola
class Usuario:
    def __init__(self, usuario, canalActual):
        # Objeto de discord con los datos del usuario
        self.usuario = usuario
        # Canal donde se encuentra
        self.canalActual = canalActual

    def getTagUsuario(self):
        # El usuario es un string
        if isinstance(self.usuario, str):
            return f"**{self.usuario}**"
        # El usuario es un objeto al que le puedo sacar el id
        return f"<@{self.usuario.id}>"

    def getUsuarioName(self):
        # El usuario es un string
        if isinstance(self.usuario, str):
            return self.usuario
        # El usuario es un objeto al que le puedo sacar el nombre
        return self.usuario.name

    # Retorna el string canal actual, o avisa si cambio o lo dejo
    def getCanalActualString(self):
        # El usuario es un string
        if isinstance(self.usuario, str):
            return ""

        # Se fue del canal donde estaba
        if self.usuario.voice is None:
            return f" Estaba en el canal **{self.canalActual}** pero lo **abandono**."

        # Esta en el mismo canal que antes
        if str(self.usuario.voice.channel) == self.canalActual:
            return f" Canal **{self.canalActual}**."

        # Cambio de canal hacia otro
        return f" Cambio de canal hacia **{self.usuario.voice.channel}**."


