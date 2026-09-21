class Cita:
    def __init__(self, codigo, paciente, medico, fecha):
        self._codigo = codigo
        self._paciente = paciente
        self._medico = medico
        self._fecha = fecha
        self._calificacion = None
        self._atencion = None

    @property
    def codigo(self):
        return self._codigo

    @property
    def paciente(self):
        return self._paciente

    @property
    def medico(self):
        return self._medico

    @property
    def fecha(self):
        return self._fecha

    @property
    def calificacion(self):
        return self._calificacion

    @property
    def atencion(self):
        return self._atencion

    def registrar_atencion(self, calificacion, descripcion):
        # Una cita solo puede ser atendida
        # una vez.
        if self._atencion is not None:
            raise ValueError("La cita ya tiene una atención registrada.")

        calificacion = calificacion.strip()
        descripcion = descripcion.strip()

        if not calificacion:
            raise ValueError("La calificación no puede estar vacía.")

        if not descripcion:
            raise ValueError("La descripción no puede estar vacía.")

        self._calificacion = calificacion
        self._atencion = descripcion

    def mostrar_datos(self):
        calificacion = self._calificacion or "Sin calificar"
        atencion = self._atencion or "Pendiente"

        print(f"[Cita] Código: {self._codigo} | "
            f"Paciente: {self._paciente.nombre} | "
            f"Médico: {self._medico.nombre} | "
            f"Fecha: {self._fecha} | "
            f"Calificación: {calificacion} | "
            f"Atención: {atencion}"
        )