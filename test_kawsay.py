import unittest

from paciente import Paciente
from medico import Medico
from cita import Cita

from registro import (
    pacientes,
    medicos,
    citas,
    buscar_por_codigo,
    buscar_pacientes_por_nombre
)

from busquedas import buscar_medicos_por_especialidad, historial_paciente
from gestion_citas import descripcion_valida


class TestSistemaKawsay(unittest.TestCase):

    # PREPARACIÓN ANTES DE CADA PRUEBA
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        Crea objetos ficticios independientes.
        """

        self.paciente = Paciente("PTEST", "Juan Perez", 30)
        self.medico = Medico("MTEST", "Dr. Pedro Lopez", "Medicina General")
        self.cita = Cita("CTEST", self.paciente, self.medico, "30/12/2026")


    # PRUEBA 1 CREACIÓN DE PACIENTE
    def test_crear_paciente(self):

        self.assertEqual(self.paciente.codigo, "PTEST")
        self.assertEqual(self.paciente.nombre, "Juan Perez")
        self.assertEqual(self.paciente.edad, 30)
        self.assertEqual(len(self.paciente.citas), 0)


    # PRUEBA 2 CREACIÓN DE MÉDICO
    def test_crear_medico(self):

        self.assertEqual(self.medico.codigo, "MTEST")
        self.assertEqual(self.medico.nombre, "Dr. Pedro Lopez")
        self.assertEqual(self.medico.especialidad, "Medicina General")


    # PRUEBA 3 AGREGAR CITA AL PACIENTE
    def test_agregar_cita_paciente(self):

        self.paciente.agregar_cita(self.cita)

        self.assertEqual(len(self.paciente.citas), 1)
        self.assertEqual(self.paciente.citas[0].codigo, "CTEST")


    # PRUEBA 4 REGISTRAR ATENCIÓN
    def test_registrar_atencion(self):

        self.cita.registrar_atencion("Muy buena", "Paciente atendido por control general.")

        self.assertEqual(self.cita.calificacion, "Muy buena")
        self.assertEqual(self.cita.atencion, "Paciente atendido por control general.")


    # PRUEBA 5 EVITAR DOBLE ATENCIÓN
    def test_no_permitir_doble_atencion(self):

        self.cita.registrar_atencion("Buena", "Paciente atendido correctamente.")

        with self.assertRaises(ValueError):
            self.cita.registrar_atencion("Muy buena", "Segunda atención que no debe guardarse.")


    # PRUEBA 6 DESCRIPCIÓN VACÍA
    def test_atencion_descripcion_vacia(self):

        with self.assertRaises(ValueError):
            self.cita.registrar_atencion("Buena", "")


    # PRUEBA 7 VALIDACIÓN DE DESCRIPCIÓN CORRECTA
    def test_descripcion_valida(self):

        descripcion = ("Paciente atendido por control general.")
        self.assertTrue(descripcion_valida(descripcion))


    # PRUEBA 8 RECHAZAR DESCRIPCIÓN MUY CORTA
    def test_descripcion_muy_corta(self):

        self.assertFalse(descripcion_valida("Dolor"))


    # PRUEBA 9 RECHAZAR SOLO NÚMEROS
    def test_descripcion_solo_numeros(self):

        self.assertFalse(descripcion_valida("123456789012345"))


    # PRUEBA 10 RECHAZAR CARACTERES REPETIDOS
    def test_descripcion_repetitiva(self):

        self.assertFalse(descripcion_valida("aaaaaaaaaaaaaaaa"))


    # PRUEBA 11 BUSCAR POR CÓDIGO
    def test_buscar_por_codigo(self):

        coleccion = {"P001": self.paciente}
        resultado = buscar_por_codigo("p001", coleccion)
        self.assertIs(resultado, self.paciente)


    # PRUEBA 12 BÚSQUEDA DE PACIENTE POR NOMBRE
    def test_buscar_paciente_por_nombre(self):

        codigo_prueba = "P999"
        pacientes[codigo_prueba] = self.paciente

        try:
            encontrados = buscar_pacientes_por_nombre("Juan")
            self.assertIn(self.paciente, encontrados)

        finally:
            pacientes.pop(codigo_prueba,None)


    # PRUEBA 13 BÚSQUEDA FUNCIONAL DE MÉDICOS
    def test_buscar_medicos_por_especialidad(self):

        encontrados = buscar_medicos_por_especialidad("Pediatría")

        self.assertGreater(len(encontrados), 0)
        self.assertTrue(all(medico.especialidad== "Pediatría" for medico in encontrados))


    # PRUEBA 14 HISTORIAL SOLO CON CITAS ATENDIDAS
    def test_historial_paciente(self):

        codigo_prueba = "P998"

        pacientes[codigo_prueba] = self.paciente

        cita_atendida = Cita("C998", self.paciente, self.medico, "30/12/2026")
        cita_pendiente = Cita("C999", self.paciente, self.medico, "31/12/2026")

        cita_atendida.registrar_atencion("Buena", "Paciente atendido por control médico.")

        self.paciente.agregar_cita(cita_atendida)
        self.paciente.agregar_cita(cita_pendiente)

        try:
            historial = historial_paciente(codigo_prueba)

            self.assertIn(cita_atendida, historial)
            self.assertNotIn(cita_pendiente, historial)

            self.assertEqual(len(historial), 1)

        finally:
            pacientes.pop(codigo_prueba, None)

# EJECUTAR PRUEBAS
if __name__ == "__main__":
    unittest.main(verbosity=2)

