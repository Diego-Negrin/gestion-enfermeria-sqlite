from datos import inicializar_bd
import logica

#1. Inicializar la base de datos y las tablas si no existen

inicializar_bd()

#2. Definir los submenus

def submenu_camas():
    while True:
        print("\nGestión de Camas:")
        print("1. Mostrar estado de camas")
        print("2. Internar un paciente en una cama")
        print("3. Dar de alta a un paciente de una cama")
        print("4. Volver al menú principal")
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            logica.mostrar_camas()
        elif opcion == "2":
            try:
                numero_cama = int(input("Ingrese el número de la cama: "))
                paciente_nombre = input("Ingrese el nombre del paciente: ")
                motivo_internacion = input("Ingrese el motivo de la internación: ")
                logica.internar_paciente(numero_cama, paciente_nombre, motivo_internacion)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido para la cama.")
        elif opcion == "3":
            try:
                numero_cama = int(input("Ingrese el número de la cama: "))
                logica.dar_alta_paciente(numero_cama)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido para la cama.")
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Por favor, intente nuevamente.")

def submenu_insumos():
    while True:
        print("\nGestión de Insumos:")
        print("1. Mostrar insumos")
        print("2. Agregar insumo")
        print("3. Modificar Stock de insumos")
        print("4. Volver al menú principal")
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            logica.mostrar_insumos()
        elif opcion == "2":
            try:
                nombre = input("Ingrese el nombre del insumo: ")
                stock = int(input("Ingrese la cantidad de stock: "))
                descripcion = input("Ingrese una descripción del insumo (opcional): ")
                logica.agregar_insumo(nombre, stock, descripcion)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido para el stock.")
        elif opcion == "3":
            try:
                nombre = input("Ingrese el nombre del insumo: ")
                cant_sumar = int(input("Ingrese la cantidad a sumar al stock: "))
                logica.actualizar_stock_insumos(nombre, cant_sumar)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido para la cantidad.")
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Por favor, intente nuevamente.")

def submenu_consumos():
    while True:
        print("\nGestión de Consumos en Camas:")
        print("1. Registrar consumo en una cama")
        print("2. Eliminar consumo de una cama")
        print("3. Volver al menú principal")
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            try:
                numero_cama = int(input("Ingrese el número de la cama: "))
                insumo_nombre = input("Ingrese el nombre del insumo: ")
                cantidad = int(input("Ingrese la cantidad consumida: "))
                procedimiento = input("Ingrese el procedimiento realizado: ")
                logica.registrar_consumo(numero_cama, insumo_nombre, cantidad, procedimiento)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese números válidos para la cama y la cantidad.")
        elif opcion == "2":
            try:
                consumo_id = int(input("Ingrese el ID del consumo a eliminar: "))
                logica.eliminar_consumo(consumo_id)
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido para el ID del consumo.")
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Por favor, intente nuevamente.")

#3. Menu principal

while True:
    print("\nBienvenido al servicio de cirujia. Por favor, seleccione una opción:")
    print("1. Gestion de Camas")
    print("2. Gestion de Insumos")
    print("3. Gestion de Consumos")
    print("4. Ver Historial de Consumos por Camas")
    print("5. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        submenu_camas()
    elif opcion == "2":
        submenu_insumos()
    elif opcion == "3":
        submenu_consumos()
    elif opcion == "4":
        try:
            numero_cama = int(input("Ingrese el número de la cama: "))
            logica.ver_consumos_cama(numero_cama)
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número válido para la cama.")    
    elif opcion == "5":
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, intente nuevamente.")

#_________________________________________________________________________________________________________________