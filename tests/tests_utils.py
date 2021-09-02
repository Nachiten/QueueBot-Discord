from unittest import TestCase
from utils.utils import stringEsValido
from utils.utils import cantidadDeParametrosEs


# Corre antes de iniciar los tests
def setUpModule():
    print('[Corriendo tests de utils]')


# Corre luego de termianr todos los tests
def tearDownModule():
    print('[Terminando tests de utils]')


class Tests_Utils(TestCase):
    def test_0_strings_validos(self):
        print("test_0_strings_validos")
        stringValido1 = stringEsValido("hola como estas")
        stringValido2 = stringEsValido("jorge")
        stringValido3 = stringEsValido("create")

        self.assertTrue(stringValido1)
        self.assertTrue(stringValido2)
        self.assertTrue(stringValido3)

    def test_1_strings_invalidos(self):
        print("test_1_strings_invalidos")
        stringInvalido1 = stringEsValido("")
        stringInvalido2 = stringEsValido(" ")
        stringInvalido3 = stringEsValido("      ")

        self.assertFalse(stringInvalido1)
        self.assertFalse(stringInvalido2)
        self.assertFalse(stringInvalido3)

    cantidadMaximaParametros = 6

    def test_2_cantidad_parametros_correctos(self):
        print("test_2_cantidad_parametros_correctos")
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

    def test_3_cantidad_parametros_incorrectos(self):
        print("test_3_cantidad_parametros_incorrectos")
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
