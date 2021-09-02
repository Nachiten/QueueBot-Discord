from unittest import TestCase
from clases.colas import Colas

'''
# Descipcion: 
# Estos tests son independientes y prueban 
# el funcionamiento del comando Create
'''


# Corre antes de iniciar los tests
def setUpModule():
    print('[Corriendo tests de create]')


# Corre luego de termianr todos los tests
def tearDownModule():
    print('[Terminando tests de create]')


nombreCola1 = "soporte"
nombreCola2 = "labo"
nombreCola3 = "coloquio"


class Tests_Create(TestCase):

    # Corre antes de cada test
    def setUp(self):
        print("Configurando valores iniciales")

    # Corre luego de cada test
    def tearDown(self):
        print("Limpiando luego del test")
        Colas.eliminarTodasLasColas()

    def test_0_crear_una_cola(self):
        print("test_0_crear_una_cola")

        Colas.agregarCola(nombreCola1)

        self.assertEqual(Colas.getColaPorNombre(nombreCola1).nombre, nombreCola1)
        self.assertEqual(Colas.cantidadDeColas(), 1)

    def test_1_crear_tres_colas(self):
        print("test_1_crear_tres_colas")

        Colas.agregarCola(nombreCola1)
        Colas.agregarCola(nombreCola2)
        Colas.agregarCola(nombreCola3)

        self.assertEqual(Colas.getColaPorNombre(nombreCola1).nombre, nombreCola1)
        self.assertEqual(Colas.getColaPorNombre(nombreCola2).nombre, nombreCola2)
        self.assertEqual(Colas.getColaPorNombre(nombreCola3).nombre, nombreCola3)
        self.assertEqual(Colas.cantidadDeColas(), 3)
