from registro import medicos, pacientes, buscar_por_codigo

# BUSCAR MÉDICOS POR ESPECIALIDAD
# Paradigma funcional: filter + lambda

def buscar_medicos_por_especialidad(especialidad):

    return list(filter(lambda medico: medico.especialidad.lower() == especialidad.lower(), medicos.values()))

# HISTORIAL DEL PACIENTE
# Solo devuelve citas atendidas

def historial_paciente(codigo_paciente):

    paciente = buscar_por_codigo(codigo_paciente, pacientes)

    if paciente is None:
        return []

    citas_atendidas = filter(lambda cita: cita.atencion is not None, paciente.citas)

    return list(citas_atendidas)