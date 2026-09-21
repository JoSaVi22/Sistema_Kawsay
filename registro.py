from paciente import Paciente
from medico import Medico
from datos_medicos import DATOS_MEDICOS

# COLECCIONES DEL SISTEMA
pacientes = {}
medicos = {}
citas = {}

# ESPECIALIDADES
ESPECIALIDADES = [
    "Medicina General",
    "Pediatría",
    "Obstetricia",
    "Ginecología",
    "Cirugía General",
    "Nutrición"
]

# CARGAR MÉDICOS PREDEFINIDOS
for codigo, nombre, especialidad in DATOS_MEDICOS:
    medicos[codigo] = Medico(codigo, nombre, especialidad)

# CREAR PERSONA
def crear_persona(tipo, codigo, nombre, dato_extra):

    if tipo == "paciente":
        return Paciente(codigo, nombre, dato_extra)

    if tipo == "medico":
        return Medico(codigo, nombre, dato_extra)

    return None

# BUSCAR POR CÓDIGO
def buscar_por_codigo(codigo, coleccion):
    return coleccion.get(codigo.upper())

# PEDIR NOMBRE. 2 intentos
def pedir_nombre():

    for intento in range(2):

        nombre = input("Ingrese el nombre: ").strip()
        nombre_sin_espacios = nombre.replace(" ", "")

        if nombre and nombre_sin_espacios.isalpha():
            return nombre.title()

        if intento == 0:
            print("\nNombre inválido.")
            print("Ingrese únicamente letras y espacios.")
            print("Tiene una oportunidad más.")

        else:
            print("\nNombre inválido nuevamente.")
            print("Registro cancelado.")

    return None

# PEDIR EDAD. 2 intentos
def pedir_edad():
    for intento in range(2):
        try:
            edad = int(input("Ingrese la edad: "))

            if 1 <= edad <= 100:
                return edad
            raise ValueError

        except ValueError:
            if intento == 0:
                print("\nEdad inválida.")
                print("Ingrese un número entre 1 y 100.")
                print("Tiene una oportunidad más.")

            else:
                print("\nEdad inválida nuevamente.")
                print("Registro cancelado.")

    return None

# GENERAR CÓDIGO PACIENTE
def generar_codigo_paciente():
    numero = 1
    while True:
        codigo = f"P{numero:03d}"

        if codigo not in pacientes:
            return codigo

        numero += 1

# GENERAR CÓDIGO MÉDICO
def generar_codigo_medico():
    numero = 1
    while True:
        codigo = f"M{numero:03d}"

        if codigo not in medicos:
            return codigo

        numero += 1

# BÚSQUEDA FUNCIONAL DE PACIENTES
def buscar_pacientes_por_nombre(nombre):
    texto = nombre.lower().strip()
    return list(filter(lambda paciente: texto in paciente.nombre.lower(), pacientes.values()))

# REGISTRAR PACIENTE
def registrar_paciente():

    print("\n=== REGISTRAR PACIENTE ===")
    nombre = pedir_nombre()

    if nombre is None:
        return None

    edad = pedir_edad()

    if edad is None:
        return None

    codigo = generar_codigo_paciente()
    nuevo_paciente = crear_persona("paciente", codigo, nombre, edad)
    pacientes[codigo] = nuevo_paciente

    print("\n================================")
    print(" PACIENTE REGISTRADO CORRECTAMENTE")
    print("================================")
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
    print(f"Código generado: {codigo}")

    return nuevo_paciente

# REGISTRAR MÉDICO
def registrar_medico():

    print("\n=== REGISTRAR MÉDICO ===")

    nombre = pedir_nombre()

    if nombre is None:
        return None

    print("\nEspecialidades disponibles:")

    for i, especialidad in enumerate(ESPECIALIDADES, start = 1):

        print(f"{i}. {especialidad}")

    especialidad = None

    for intento in range(2):

        try:
            opcion = int(input("\nSeleccione una especialidad: "))

            if 1 <= opcion <= len(ESPECIALIDADES):
                especialidad = ESPECIALIDADES[opcion - 1]
                break

            raise ValueError

        except ValueError:

            if intento == 0:
                print("\nOpción inválida.")
                print("Tiene una oportunidad más.")

            else:
                print("\nOpción inválida nuevamente.")
                print("Registro de médico cancelado.")

    if especialidad is None:
        return None

    codigo = generar_codigo_medico()

    nuevo_medico = crear_persona("medico", codigo, nombre, especialidad)

    medicos[codigo] = nuevo_medico

    print("\n================================")
    print("  MÉDICO REGISTRADO CORRECTAMENTE")
    print("================================")
    print(f"Nombre: {nombre}")
    print(f"Especialidad: {especialidad}")
    print(f"Código generado: {codigo}")

    return nuevo_medico
