import time

from datetime import datetime, date
from cita import Cita
from registro import (
    pacientes,
    medicos,
    citas,
    ESPECIALIDADES,
    buscar_por_codigo,
    buscar_pacientes_por_nombre
)

# GENERAR CÓDIGO DE CITA
def generar_codigo_cita():
    numero = 1

    while True:
        codigo = f"C{numero:03d}"

        if codigo not in citas:
            return codigo

        numero += 1

# PEDIR FECHA
def pedir_fecha():

    for intento in range(2):
        fecha = input("\nFecha de la cita (dd/mm/aaaa): ").strip()

        try:
            if len(fecha) != 10:
                raise ValueError
            
            if fecha[2] != "/" or fecha[5] != "/":
                raise ValueError
            numeros = fecha.replace("/", "")

            if not numeros.isdigit():
                raise ValueError
            fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y").date()

            if fecha_convertida < date.today():
                print("\nNo puede programar una cita en una fecha pasada.")
                raise ValueError
            return fecha

        except ValueError:
            if intento == 0:
                print("\nFecha inválida.")
                print("Ingrese una fecha válida en formato dd/mm/aaaa.")
                print("Ejemplo: 18/10/2026")
                print("Tiene una oportunidad más.")

            else:
                print("\nFecha inválida nuevamente.")
                print("Programación de cita cancelada.")
    return None

# SELECCIONAR PACIENTE
def seleccionar_paciente():

    print("\n=== SELECCIONAR PACIENTE ===")

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        print("Registre primero un paciente.")
        return None

    busqueda = input("\nIngrese el nombre o código del paciente: ").strip()

    if not busqueda:
        print("\nDebe ingresar un nombre o código.")
        return None

    # Primero buscamos por código.
    paciente = buscar_por_codigo(busqueda.upper(), pacientes)
    if paciente is not None:
        return paciente

    # Si no es código,buscamos por nombre.
    encontrados = buscar_pacientes_por_nombre(busqueda)

    if not encontrados:
        print("\nNo se encontró ningún paciente.")
        return None

    if len(encontrados) == 1:
        return encontrados[0]

    print("\nSe encontraron varios pacientes:")

    for i, paciente in enumerate(encontrados, start = 1):
        print(f"{i}. {paciente.nombre} - Código: {paciente.codigo}")

    for intento in range(2):

        try:
            opcion = int(input("\nSeleccione un paciente: "))

            if 1 <= opcion <= len(encontrados):
                return encontrados[opcion - 1]
            raise ValueError

        except ValueError:

            if intento == 0:
                print("\nOpción inválida.")
                print("Tiene una oportunidad más.")

            else:
                print("\nOpción inválida nuevamente.")
                print("Selección cancelada.")

    return None

# SELECCIONAR ESPECIALIDAD
def seleccionar_especialidad():

    print("\nEspecialidades disponibles:")

    for i, especialidad in enumerate(ESPECIALIDADES, start = 1):
        print(f"{i}. {especialidad}")

    for intento in range(2):

        try:
            opcion = int(input("\nSeleccione una especialidad: "))

            if 1 <= opcion <= len(ESPECIALIDADES):
                return ESPECIALIDADES[opcion - 1]
            raise ValueError

        except ValueError:

            if intento == 0:
                print("\nOpción inválida.")
                print(f"Ingrese un número del 1 al {len(ESPECIALIDADES)}.")
                print("Tiene una oportunidad más.")

            else:
                print("\nOpción inválida nuevamente.")
                print("Programación de cita cancelada.")

    return None

# SELECCIONAR MÉDICO
# Paradigma funcional
def seleccionar_medico(especialidad):

    medicos_disponibles = list(filter(lambda medico: medico.especialidad == especialidad,medicos.values()))

    if not medicos_disponibles:
        print("\nNo hay médicos disponibles para esa especialidad.")
        return None

    print(f"\nMédicos disponibles en {especialidad}:")

    for i, medico in enumerate(medicos_disponibles, start = 1):
        print(f"{i}. {medico.nombre} - Código: {medico.codigo}")

    for intento in range(2):

        try:
            opcion = int(input("\nSeleccione un médico: "))

            if 1 <= opcion <= len(medicos_disponibles):
                return medicos_disponibles[opcion - 1]
            raise ValueError

        except ValueError:

            if intento == 0:
                print("\nOpción de médico inválida.")
                print(f"Ingrese un número del 1 al {len(medicos_disponibles)}.")
                print("Tiene una oportunidad más.")

            else:
                print("\nOpción inválida nuevamente.")
                print("Programación de cita cancelada.")

    return None

# PROGRAMAR CITA
def programar_cita(paciente=None):

    print("\n=== PROGRAMAR CITA ===")

    if paciente is None:
        paciente = seleccionar_paciente()

        if paciente is None:
            return False

    print("\nPaciente seleccionado:")

    print(f"{paciente.nombre} - Código: {paciente.codigo}")

    especialidad = seleccionar_especialidad()

    if especialidad is None:
        return False

    medico = seleccionar_medico(especialidad)

    if medico is None:
        return False

    fecha = pedir_fecha()

    if fecha is None:
        return False

    print("\nProcesando cita...")

    time.sleep(2)

    codigo_cita = generar_codigo_cita()
    nueva_cita = Cita(codigo_cita, paciente, medico, fecha)
    citas[codigo_cita] = nueva_cita

    paciente.agregar_cita(nueva_cita)

    print("\n================================")
    print("     CITA PROGRAMADA CON ÉXITO")
    print("================================")
    print(f"Paciente: {paciente.nombre}")
    print(f"Código del paciente: {paciente.codigo}")
    print(f"Especialidad: {especialidad}")
    print(f"Médico: {medico.nombre}")
    print(f"Fecha: {fecha}")
    print(f"Código de cita: {codigo_cita}")
    print("\nGracias por confiar en Sistema Kawsay.")

    return True

# VALIDAR TEXTO DE ATENCIÓN
def descripcion_valida(texto):

    texto = texto.strip()

    # Debe tener un mínimo de contenido.
    if len(texto) < 10:
        return False

    # Debe contener letras.
    if not any(caracter.isalpha() for caracter in texto):
        return False

    # Tomamos solo letras para detectar entradas como "aaaaaaaaaaaa".
    letras = [caracter.lower() for caracter in texto if caracter.isalpha()]

    if not letras:
        return False

    # Si todas las letras son iguales, consideramos que el texto no es válido.
    if len(set(letras)) == 1:
        return False

    return True

# SELECCIONAR CALIFICACIÓN
def seleccionar_calificacion():

    print("\n¿Cómo califica la atención?")
    print("1. Buena")
    print("2. Muy buena")
    print("3. Mala")
    print("4. Otro")

    for intento in range(2):

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            return "Buena"

        elif opcion == "2":
            return "Muy buena"

        elif opcion == "3":
            return "Mala"

        elif opcion == "4":

            otra = input("\nEspecifique la calificación: ").strip()

            # Para una calificación personalizada basta con que contenga letras
            # y tenga al menos 3 caracteres.
            if len(otra) >= 3 and any(caracter.isalpha() for caracter in otra):
                return otra.capitalize()

            print("\nLa calificación ingresada no es válida.")

            if intento == 0:
                print("Tiene una oportunidad más.")
            continue

        if intento == 0:

            print("\nOpción inválida.")
            print("Seleccione una opción del 1 al 4.")
            print("Tiene una oportunidad más.")

    print("\nNo se pudo registrar una calificación válida.")

    return None

# PEDIR DESCRIPCIÓN DE ATENCIÓN
def pedir_descripcion_atencion():

    for intento in range(2):

        descripcion = input("\nDescriba la atención realizada: ").strip()

        if descripcion_valida(descripcion):
            return descripcion

        if intento == 0:
            print("\nDescripción inválida.")
            print("Ingrese una descripción relacionada con la atención realizada.")
            print("Debe contener texto descriptivo y al menos 10 caracteres.")
            print("Tiene una oportunidad más.")

        else:
            print("\nDescripción inválida nuevamente.")
            print("Registro de atención cancelado.")

    return None

# REGISTRAR ATENCIÓN
def registrar_atencion():

    print("\n=== REGISTRAR ATENCIÓN ===")

    if not citas:
        print("\nNo hay citas programadas.")
        return False

    codigo = input("Ingrese el código de la cita: ").strip().upper()
    cita = buscar_por_codigo(codigo, citas)

    if cita is None:
        print("\nCita no encontrada.")
        return False

    print("\nCita encontrada:")
    cita.mostrar_datos()

    # EVITAR DOBLE ATENCIÓN
    if cita.atencion is not None:
        print("\nEsta cita ya tiene una atención registrada.")
        print(f"Calificación: {cita.calificacion}")
        print(f"Atención: {cita.atencion}")
        return False

    # CALIFICACIÓN
    calificacion = seleccionar_calificacion()

    if calificacion is None:
        return False

    # DESCRIPCIÓN
    descripcion = pedir_descripcion_atencion()

    if descripcion is None:
        return False

    # REGISTRAR
    try:

        cita.registrar_atencion(calificacion, descripcion)

        print("\n================================")
        print("   ATENCIÓN REGISTRADA CON ÉXITO")
        print("================================")
        print(f"Código de cita: {cita.codigo}")
        print(f"Paciente: {cita.paciente.nombre}")
        print(f"Médico: {cita.medico.nombre}")
        print(f"Fecha: {cita.fecha}")
        print(f"Calificación: {cita.calificacion}")
        print(f"Atención: {cita.atencion}")
        return True

    except ValueError as error:
        print(f"\nNo se pudo registrar la atención: {error}")
        return False