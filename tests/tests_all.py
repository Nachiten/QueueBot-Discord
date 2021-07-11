from unittest import TestCase
from src.clases.colas import Colas

'''
# Descipcion: 
# Estos tests son independientes y prueban 
# el funcionamiento del comando All
'''


# Corre antes de iniciar los tests
def setUpModule():
    print('[Corriendo tests de all]')


# Corre luego de termianr todos los tests
def tearDownModule():
    print('[Terminando tests de all]')


nombreCola1 = "soporte"
nombreCola2 = "labo"
nombreCola3 = "coloquio"


class Tests_All(TestCase):

    # Corre antes de cada test
    def setUp(self):
        print("Configurando valores iniciales")

    # Corre luego de cada test
    def tearDown(self):
        print("Limpiando luego del test")
        Colas.eliminarTodasLasColas()

    def test_0_listar_una_cola(self):
        print("test_0_listar_una_cola")
        Colas.agregarCola(nombreCola1)

        mensajeEmbed = Colas.generarMensajeListandoColas()

        nombresColas = mensajeEmbed.fields[0].value
        cantidadUsuariosColas = mensajeEmbed.fields[1].value

        self.assertEqual(nombresColas, "soporte\n")
        self.assertEqual(cantidadUsuariosColas, "0\n")

    def test_1_listar_tres_colas(self):
        print("test_1_listar_tres_colas")
        Colas.agregarCola(nombreCola1)
        Colas.agregarCola(nombreCola2)
        Colas.agregarCola(nombreCola3)

        mensajeEmbed = Colas.generarMensajeListandoColas()

        nombresColas = mensajeEmbed.fields[0].value
        cantidadUsuariosColas = mensajeEmbed.fields[1].value

        self.assertEqual(nombresColas, "soporte\nlabo\ncoloquio\n")
        self.assertEqual(cantidadUsuariosColas, "0\n0\n0\n")
