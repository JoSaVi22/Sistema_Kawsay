class Medico:
    def __init__(self, codigo, nombre, especialidad):
        self._codigo = codigo
        self._nombre = nombre
        self._especialidad = especialidad

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def especialidad(self):
        return self._especialidad

    def mostrar_datos(self):
        print(f"[Médico] Código: {self._codigo} | Nombre: {self._nombre} | Especialidad: {self._especialidad}")