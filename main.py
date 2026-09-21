from registro import (
    pacientes,
    medicos,
    citas,
    ESPECIALIDADES,
    registrar_paciente,
    registrar_medico,
    buscar_por_codigo,
    buscar_pacientes_por_nombre
)
from gestion_citas import programar_cita, registrar_atencion
from busquedas import historial_paciente, buscar_medicos_por_especialidad

# MENÚ PRINCIPAL
def menu():

    print("\n========== SISTEMA KAWSAY ==========")
    print("1. Registrar paciente")
    print("2. Registrar médico")
    print("3. Buscar registro")
    print("4. Programar cita")
    print("5. Registrar atención")
    print("6. Ver historial de un paciente")
    print("7. Salir")

# PREGUNTAR OTRA OPERACIÓN
def preguntar_otra_operacion():

    while True:

        print("\n¿Desea realizar otra operación?")
        print("1. Sí")
        print("2. No")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            return True

        if opcion == "2":
            return False

        print("\nOpción no válida.")
        print("Seleccione 1 para Sí o 2 para No.")

# PREGUNTAR SI DESEA PROGRAMAR CITA
def preguntar_programar_cita():

    while True:

        print("\n¿Desea programar una cita para este paciente?")
        print("1. Sí")
        print("2. No")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            return True

        if opcion == "2":
            return False

        print("\nOpción no válida.")
        print("Seleccione 1 para Sí o 2 para No.")

# BUSCAR PACIENTE
def buscar_paciente():

    print("\n=== BUSCAR PACIENTE ===")

    if not pacientes:
        print("\nNo hay pacientes registrados.")
        return

    busqueda = input("Ingrese nombre o código: ").strip()

    if not busqueda:
        print("\nDebe ingresar un nombre o código.")
        return

    paciente = buscar_por_codigo(busqueda.upper(), pacientes)

    if paciente is not None:
        print("\nPaciente encontrado:")
        paciente.mostrar_datos()
        return

    encontrados = buscar_pacientes_por_nombre(busqueda)

    if not encontrados:
        print("\nNo se encontró ningún paciente.")
        return

    print("\nPaciente(s) encontrado(s):")

    for paciente in encontrados:
        paciente.mostrar_datos()

# BUSCAR MÉDICO
def buscar_medico():

    while True:
        print("\n=== BUSCAR MÉDICO ===")
        print("1. Buscar por nombre")
        print("2. Buscar por especialidad")
        print("3. Buscar por código")
        print("4. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        # POR NOMBRE
        if opcion == "1":
            nombre = input("\nIngrese el nombre del médico: ").strip().lower()

            if not nombre:
                print("\nDebe ingresar un nombre.")
                return

            encontrados = list(filter(lambda medico: nombre in medico.nombre.lower(), medicos.values()))

            if encontrados:
                print("\nMédico(s) encontrado(s):")

                for medico in encontrados:
                    medico.mostrar_datos()

            else:
                print("\nNo se encontraron médicos con ese nombre.")
            return

        # POR ESPECIALIDAD
        elif opcion == "2":
            print("\nEspecialidades disponibles:")

            for i, especialidad in enumerate(ESPECIALIDADES, start = 1):
                print(f"{i}. {especialidad}")

            try:

                seleccion = int(input("\nSeleccione una especialidad: "))

                if not 1 <= seleccion <= len(ESPECIALIDADES):
                    raise ValueError

                especialidad = ESPECIALIDADES[seleccion - 1]
                encontrados = buscar_medicos_por_especialidad(especialidad)

                print(f"\nMédicos de {especialidad}:")

                for medico in encontrados:
                    medico.mostrar_datos()

            except ValueError:
                print("\nSelección inválida.")
            return

        # POR CÓDIGO
        elif opcion == "3":
            codigo = input("\nIngrese código del médico: ").strip().upper()
            medico = buscar_por_codigo(codigo, medicos)

            if medico is not None:
                print("\nMédico encontrado:")
                medico.mostrar_datos()

            else:
                print("\nMédico no encontrado.")
            return

        elif opcion == "4":
            return

        else:
            print("\nOpción no válida.")

# BUSCAR CITA
def buscar_cita():

    print("\n=== BUSCAR CITA ===")

    if not citas:
        print("\nNo hay citas registradas.")
        return

    codigo = input("Ingrese el código de la cita: ").strip().upper()
    cita = buscar_por_codigo(codigo, citas)

    if cita is not None:
        print("\nCita encontrada:")
        cita.mostrar_datos()

    else:
        print("\nCita no encontrada.")

# BUSCAR REGISTRO
def buscar_registro():

    while True:

        print("\n=== BUSCAR REGISTRO ===")
        print("\n¿Qué desea buscar?")
        print("1. Paciente")
        print("2. Médico")
        print("3. Cita")
        print("4. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            buscar_paciente()
            return

        elif opcion == "2":
            buscar_medico()
            return

        elif opcion == "3":
            buscar_cita()
            return

        elif opcion == "4":
            return

        else:
            print("\nOpción no válida.")

# BASE PRINCIPAL
def main():

    ejecutar = True

    while ejecutar:

        menu()

        opcion = input("\nSeleccione una opción: ").strip()

        # 1. REGISTRAR PACIENTE
        if opcion == "1":

            paciente = registrar_paciente()

            if paciente is not None:

                if preguntar_programar_cita():
                    programar_cita(paciente)

                ejecutar = preguntar_otra_operacion()

        # 2. REGISTRAR MÉDICO
        elif opcion == "2":
            registrar_medico()
            ejecutar = preguntar_otra_operacion()

        # 3. BUSCAR REGISTRO
        elif opcion == "3":
            buscar_registro()
            ejecutar = preguntar_otra_operacion()

        # 4. PROGRAMAR CITA
        elif opcion == "4":
            programar_cita()
            ejecutar = preguntar_otra_operacion()

        # 5. REGISTRAR ATENCIÓN
        elif opcion == "5":
            registrar_atencion()
            ejecutar = preguntar_otra_operacion()

        # 6. HISTORIAL
        elif opcion == "6":
            print("\n=== HISTORIAL DEL PACIENTE ===")
            codigo = input("Código del paciente: ").strip().upper()
            paciente = buscar_por_codigo(codigo, pacientes)

            if paciente is None:
                print("\nPaciente no encontrado.")

            else:
                historial = historial_paciente(codigo)

                if historial:
                    print(f"\nHistorial de {paciente.nombre}:")
                    for cita in historial:
                        cita.mostrar_datos()

                else:
                    print("\nSin atenciones registradas para ese paciente.")

            ejecutar = preguntar_otra_operacion()

        # 7. SALIR
        elif opcion == "7":
            ejecutar = False

        else:
            print("\nOpción no válida. Seleccione una opción del 1 al 7.")

    # DESPEDIDA
    print("\n================================")
    print("     GRACIAS POR USAR KAWSAY")
    print("================================")
    print("¡Que tenga un excelente día!")

# EJECUTAR SISTEMA
if __name__ == "__main__":
    main()