from unittest import TestCase
from src.clases.colas import Colas

'''
# Descipcion: 
# Estos tests son independientes y prueban 
# el funcionamiento del comando Delete
'''


# Corre antes de iniciar los tests
def setUpModule():
    print('[Corriendo tests de delete]')


# Corre luego de termianr todos los tests
def tearDownModule():
    print('[Terminando tests de delete]')


nombreCola1 = "soporte"
nombreCola2 = "labo"
nombreCola3 = "coloquio"


class Tests_Delete(TestCase):

    # Corre antes de cada test
    def setUp(self):
        print("Configurando valores iniciales")

        Colas.agregarCola(nombreCola1)
        Colas.agregarCola(nombreCola2)
        Colas.agregarCola(nombreCola3)

    # Corre luego de cada test
    def tearDown(self):
        print("Limpiando luego del test")
        Colas.eliminarTodasLasColas()

    def test_0_eliminar_una_cola(self):
        print("test_0_eliminar_una_cola")
        Colas.quitarCola(nombreCola1)

        self.assertEqual(Colas.cantidadDeColas(), 2)

    def test_1_eliminar_tres_colas(self):
        print("test_1_eliminar_tres_colas")
        Colas.quitarCola(nombreCola1)
        Colas.quitarCola(nombreCola2)
        Colas.quitarCola(nombreCola3)

        self.assertEqual(Colas.cantidadDeColas(), 0)
