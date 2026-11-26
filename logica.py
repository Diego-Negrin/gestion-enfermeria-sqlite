import sqlite3
from datos import conectar


# 1) Funciones de Insumos

def buscar_insumo(nombre_buscado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM insumos WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(?))", (nombre_buscado,))
    resultados = cursor.fetchone()
    conexion.close()
    return resultados

def agregar_insumo(nombre, stock, descripcion=""):
    if buscar_insumo(nombre):
        print(f"El insumo {nombre} ya existe en la base de datos.")
        return
    if stock <   0:
        print(f"Advertencia: El stock del insumo {nombre.strip()} es {stock}. Por favor, asegúrese de que sea un valor positivo.")
        return
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO insumos (nombre, stock, descripcion) VALUES (?, ?, ?)",
            (nombre.strip(), stock, descripcion.strip())
        )
        conexion.commit()
        print(f"Insumo {nombre.strip()} agregado a la base de datos.")
    except sqlite3.IntegrityError:
        print(f"El insumo {nombre} ya existe en la base de datos.")
    finally:
        conexion.close()

def mostrar_insumos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM insumos ORDER BY nombre")
    insumos = cursor.fetchall()
    conexion.close()

    if not insumos:
        print("No hay insumos registrados.")
        return
    for item in insumos:
        print(f"[ID: {item['id']}] Insumo: {item['nombre']} - Stock: {item['stock']} - Descripción: {item['descripcion']}")

def actualizar_stock_insumos(nombre, cant_sumar):
    if cant_sumar <= 0:
        print(f"La cantidad a sumar debe ser mayor que cero. Cantidad ingresada: {cant_sumar}.")
        return
    insumo = buscar_insumo(nombre)
    if insumo:
        stock = insumo["stock"] + cant_sumar
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE insumos SET stock = stock + ? WHERE id = ?",
            (cant_sumar, insumo["id"])
        )
    else:
        print(f"No se encontró el insumo: {nombre}. No se puede actualizar el stock.")
        return  
        conexion.commit()
        conexion.close()
        print(f"Stock del insumo {insumo['nombre']} actualizado a {stock}.")

#________________________________________________________________________________________________________________---
#2) Funciones de Tabla Camas

def mostrar_camas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas ORDER BY numero")
    camas = cursor.fetchall()   
    conexion.close()

    if not camas:
        print("No hay camas registradas.")
        return
    for cama in camas:
        if cama['estado'] == 'Libre':
            print(f"[Cama {cama['numero']}] - Estado: {cama['estado']}")
        else:
            print(f"[Cama {cama['numero']}] - Estado: {cama['estado']} - Paciente: {cama['paciente_nombre']} - Motivo: {cama['motivo_internacion']}")


def internar_paciente(numero_cama, paciente_nombre, motivo_internacion):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()

    if not cama:
        print(f"No existe la cama número {numero_cama}.")
        conexion.close()
        return

    if cama['estado'] == 'Ocupada':
        print(f"La cama número {numero_cama} ya está ocupada por {cama['paciente_nombre']}.")
        conexion.close()
        return

    cursor.execute(
        "UPDATE camas SET estado = 'Ocupada', paciente_nombre = ?, motivo_internacion = ? WHERE numero = ?",
        (paciente_nombre.strip(), motivo_internacion.strip(), numero_cama)
    )
    conexion.commit()
    conexion.close()
    print(f"Paciente {paciente_nombre.strip()} internado en la cama número {numero_cama}.")

def dar_alta_paciente(numero_cama):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()

    if not cama:
        print(f"No existe la cama número {numero_cama}.")
        conexion.close()
        return

    if cama['estado'] == 'Libre':
        print(f"La cama número {numero_cama} ya está libre.")
        conexion.close()
        return

    nombre_paciente = cama['paciente_nombre']

    cursor.execute(
        "UPDATE camas SET estado = 'Libre', paciente_nombre = NULL, motivo_internacion = NULL WHERE numero = ?",
        (numero_cama,)
    )
    conexion.commit()
    conexion.close()
    print(f"Paciente {nombre_paciente} dado de alta de la cama número {numero_cama}.")

#________________________________________________________________________________________________________________
#3) Funciones de Tabla Consumos

def registrar_consumo(numero_cama, nombre_insumo, cantidad, procedimiento):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si la cama existe y está ocupada
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()
    if not cama:
        print(f"No existe la cama número {numero_cama}.")
        conexion.close()
        return
    if cama['estado'] == 'Libre':
        print(f"La cama número {numero_cama} está libre. No se puede registrar consumo.")
        conexion.close()
        return

    # Verificar si el insumo existe y tiene stock suficiente
    cursor.execute("SELECT * FROM insumos WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(?))", (nombre_insumo,))
    insumo = cursor.fetchone()
    if cantidad <= 0:
        print(f"La cantidad a registrar debe ser mayor que cero. Cantidad ingresada: {cantidad}.")
        conexion.close()
        return
    if not insumo:
        print(f"No existe el insumo: {nombre_insumo}.")
        conexion.close()
        return
    if insumo['stock'] < cantidad:
        print(f"No hay suficiente stock del insumo: {nombre_insumo}. Stock disponible: {insumo['stock']}.")
        conexion.close()
        return

    # Registrar el consumo
    cursor.execute(
        "INSERT INTO consumos (fecha, cama_numero, paciente_nombre, insumo_id, insumo_nombre, cantidad, procedimiento) VALUES (datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?)",
        (numero_cama, cama['paciente_nombre'], insumo['id'], insumo['nombre'], cantidad, procedimiento.strip())
    )
    
    # Actualizar el stock del insumo
    cursor.execute(
        "UPDATE insumos SET stock = stock - ? WHERE id = ?",
        (cantidad, insumo['id'])
    )

    conexion.commit()
    conexion.close()
    print(f"Consumo registrado: {cantidad} unidades de {insumo['nombre']} para el paciente {cama['paciente_nombre']} en la cama número {numero_cama}.")

def ver_consumos_cama(numero_cama):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si la cama existe
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()
    if not cama:
        print(f"No existe la cama número {numero_cama}.")
        conexion.close()
        return

    # Obtener los consumos de la cama
    cursor.execute("SELECT * FROM consumos WHERE cama_numero = ? ORDER BY fecha DESC", (numero_cama,))
    consumos = cursor.fetchall()
    conexion.close()

    if not consumos:
        print(f"No hay consumos registrados para la cama número {numero_cama}.")
        return

    print(f"Consumos para la cama número {numero_cama}:")
    for consumo in consumos:
        print(f"[{consumo['fecha']}] - ID: {consumo['id']} - {consumo['paciente_nombre']} - Insumo: {consumo['insumo_nombre']} - Cantidad: {consumo['cantidad']} - Procedimiento: {consumo['procedimiento']}")

def eliminar_consumo(consumo_id):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si el consumo existe
    cursor.execute("SELECT * FROM consumos WHERE id = ?", (consumo_id,))
    consumo = cursor.fetchone()
    if not consumo:
        print(f"No existe el consumo con ID {consumo_id}.")
        conexion.close()
        return

    # Restaurar el stock del insumo
    cursor.execute(
        "UPDATE insumos SET stock = stock + ? WHERE id = ?",
        (consumo['cantidad'], consumo['insumo_id'])
    )

    # Eliminar el registro de consumo
    cursor.execute("DELETE FROM consumos WHERE id = ?", (consumo_id,))

    conexion.commit()
    conexion.close()
    print(f"Consumo con ID {consumo_id} eliminado y stock del insumo {consumo['insumo_nombre']} restaurado.")
#________________________________________________________________________________________________________________