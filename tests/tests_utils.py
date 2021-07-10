from unittest import TestCase
from src.utils.utils import stringEsValido
from src.utils.utils import cantidadDeParametrosEs


class Tests_Utils(TestCase):
    def test_stringsValidos(self):
        stringValido1 = stringEsValido("hola como estas")
        stringValido2 = stringEsValido("jorge")
        stringValido3 = stringEsValido("create")

        self.assertTrue(stringValido1)
        self.assertTrue(stringValido2)
        self.assertTrue(stringValido3)

    def test_strings_invalidos(self):
        stringInvalido1 = stringEsValido("")
        stringInvalido2 = stringEsValido(" ")
        stringInvalido3 = stringEsValido("      ")

        self.assertFalse(stringInvalido1)
        self.assertFalse(stringInvalido2)
        self.assertFalse(stringInvalido3)

    cantidadMaximaParametros = 6

    def test_cantidad_parametros_correctos(self):
        esUnParametro = cantidadDeParametrosEs(1, "!queue"
                                               .split(" ", self.cantidadMaximaParametros))
        sonDosParametros = cantidadDeParametrosEs(2, "!queue create"
                                                  .split(" ", self.cantidadMaximaParametros))
        sonTresParametros = cantidadDeParametrosEs(3, "!queue create hola"
                                                   .split(" ", self.cantidadMaximaParametros))
        sonCuatroParametros = cantidadDeParametrosEs(4, "!queue create hola jorge"
                                                     .split(" ", self.cantidadMaximaParametros))

        self.assertTrue(esUnParametro)
        self.assertTrue(sonDosParametros)
        self.assertTrue(sonTresParametros)
        self.assertTrue(sonCuatroParametros)

    def test_cantidad_parametros_incorrectos(self):
        esUnParametro = cantidadDeParametrosEs(1, "!queue add hola"
                                               .split(" ", self.cantidadMaximaParametros))
        sonDosParametros = cantidadDeParametrosEs(2, "!queue"
                                                  .split(" ", self.cantidadMaximaParametros))
        sonTresParametros = cantidadDeParametrosEs(3, "!queue create hola jorge"
                                                   .split(" ", self.cantidadMaximaParametros))
        sonCuatroParametros = cantidadDeParametrosEs(4, "!queue create hola jorge algoMas"
                                                     .split(" ", self.cantidadMaximaParametros))

        self.assertFalse(esUnParametro)
        self.assertFalse(sonDosParametros)
        self.assertFalse(sonTresParametros)
        self.assertFalse(sonCuatroParametros)
