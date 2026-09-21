class Paciente:
    def __init__(self, codigo, nombre, edad):
        self._codigo = codigo
        self._nombre = nombre
        self._edad = edad
        self._citas = []

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def edad(self):
        return self._edad

    @property
    def citas(self):
        # Se devuelve una copia para proteger la lista interna del paciente.
        return list(self._citas)

    def agregar_cita(self, cita):
        self._citas.append(cita)

    def mostrar_datos(self):
        print(f"[Paciente] Código: {self._codigo} | Nombre: {self._nombre} | Edad: {self._edad} | N° citas: {len(self._citas)}")