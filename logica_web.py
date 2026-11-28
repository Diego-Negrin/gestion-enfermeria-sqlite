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
    try:
        stock = int(stock)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero válido."
    if not nombre or not nombre.strip():
        return False, "El nombre del insumo no puede estar vacio"
    if buscar_insumo(nombre):
        return False, f"El insumo {nombre} ya existe en la base de datos."
    if stock <   0:
        return False, f"Advertencia: El stock del insumo {nombre.strip()} es {stock}. Por favor, asegúrese de que sea un valor positivo."
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO insumos (nombre, stock, descripcion) VALUES (?, ?, ?)",
            (nombre.strip(), stock, descripcion.strip())
        )
        conexion.commit()
        return True, f"Insumo {nombre.strip()} agregado a la base de datos."
    except sqlite3.IntegrityError:
        return False, f"El insumo {nombre} ya existe en la base de datos."
    finally:
        conexion.close()

def mostrar_insumos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM insumos ORDER BY nombre")
    insumos = cursor.fetchall()
    conexion.close()
    return insumos

def actualizar_stock_insumos(nombre, cant_sumar):
    try:
        cant_sumar = int(cant_sumar)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero válido."
    if cant_sumar <= 0:
        return False, f"La cantidad a sumar debe ser mayor que cero. Cantidad ingresada: {cant_sumar}."
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
        return False, f"No se encontró el insumo: {nombre}. No se puede actualizar el stock."
    conexion.commit()
    conexion.close()
    return True, f"Stock del insumo {insumo['nombre']} actualizado a {stock}."

#________________________________________________________________________________________________________________---
#2) Funciones de Tabla Camas

def mostrar_camas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas ORDER BY numero")
    camas = cursor.fetchall()   
    conexion.close()
    return camas

def internar_paciente(numero_cama, paciente_nombre, motivo_internacion):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()

    if not paciente_nombre or not paciente_nombre.strip():
        return False, "El nombre del paciente no puede estar vacío."

    if not motivo_internacion or not motivo_internacion.strip():
        return False, "El motivo de internación no puede estar vacío."

    if not cama:
        conexion.close()
        return False, f"No existe la cama número {numero_cama}."

    if cama['estado'] == 'Ocupada':
        conexion.close()
        return False, f"La cama número {numero_cama} ya está ocupada por {cama['paciente_nombre']}."

    cursor.execute(
        "UPDATE camas SET estado = 'Ocupada', paciente_nombre = ?, motivo_internacion = ? WHERE numero = ?",
        (paciente_nombre.strip(), motivo_internacion.strip(), numero_cama)
    )
    conexion.commit()
    conexion.close()
    return True, f"Paciente {paciente_nombre.strip()} internado en la cama número {numero_cama}."

def dar_alta_paciente(numero_cama):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()

    if not cama:
        conexion.close()
        return False, f"No existe la cama número {numero_cama}."

    if cama['estado'] == 'Libre':
        conexion.close()
        return False, f"La cama número {numero_cama} ya está libre."

    nombre_paciente = cama['paciente_nombre']

    cursor.execute(
        "UPDATE camas SET estado = 'Libre', paciente_nombre = NULL, motivo_internacion = NULL WHERE numero = ?",
        (numero_cama,)
    )
    conexion.commit()
    conexion.close()
    return True, f"Paciente {nombre_paciente} dado de alta de la cama número {numero_cama}."

#________________________________________________________________________________________________________________
#3) Funciones de Tabla Consumos

def registrar_consumo(numero_cama, nombre_insumo, cantidad, procedimiento=""):
    try:
        numero_cama = int(numero_cama)
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero válido."
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si la cama existe y está ocupada
    cursor.execute("SELECT * FROM camas WHERE numero = ?", (numero_cama,))
    cama = cursor.fetchone()
    if not cama:
        conexion.close()
        return False, f"No existe la cama número {numero_cama}."
    if cama['estado'] == 'Libre':
        conexion.close()
        return False, f"La cama número {numero_cama} está libre. No se puede registrar consumo."

    # Verificar si el insumo existe y tiene stock suficiente
    cursor.execute("SELECT * FROM insumos WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(?))", (nombre_insumo,))
    insumo = cursor.fetchone()
    if cantidad <= 0:
        conexion.close()
        return False, f"La cantidad a registrar debe ser mayor que cero. Cantidad ingresada: {cantidad}."
    if not insumo:
        conexion.close()
        return False, f"No existe el insumo: {nombre_insumo}."
    if insumo['stock'] < cantidad:
        conexion.close()
        return False, f"No hay suficiente stock del insumo: {nombre_insumo}. Stock disponible: {insumo['stock']}."

    # Registrar el consumo
    cursor.execute(
        "INSERT INTO consumos (fecha, cama_numero, paciente_nombre, insumo_id, insumo_nombre, cantidad, procedimiento) VALUES (datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?)",
        (numero_cama, cama['paciente_nombre'], insumo['id'], insumo['nombre'], cantidad, (procedimiento or "sin especificar").strip())
    )
    
    # Actualizar el stock del insumo
    cursor.execute(
        "UPDATE insumos SET stock = stock - ? WHERE id = ?",
        (cantidad, insumo['id'])
    )

    conexion.commit()
    conexion.close()
    return True, f"Consumo registrado: {cantidad} unidades de {insumo['nombre']} para el paciente {cama['paciente_nombre']} en la cama número {numero_cama}."

def ver_consumos_cama(numero_cama):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM consumos WHERE cama_numero = ? ORDER BY fecha DESC", (numero_cama,))
    consumos = cursor.fetchall()
    conexion.close()
    return consumos

def eliminar_consumo(consumo_id):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si el consumo existe
    cursor.execute("SELECT * FROM consumos WHERE id = ?", (consumo_id,))
    consumo = cursor.fetchone()
    if not consumo:
        conexion.close()
        return False, f"No existe el consumo con ID {consumo_id}."

    # Restaurar el stock del insumo
    cursor.execute(
        "UPDATE insumos SET stock = stock + ? WHERE id = ?",
        (consumo['cantidad'], consumo['insumo_id'])
    )

    # Eliminar el registro de consumo
    cursor.execute("DELETE FROM consumos WHERE id = ?", (consumo_id,))

    conexion.commit()
    conexion.close()
    return True, f"Consumo con ID {consumo_id} eliminado y stock del insumo {consumo['insumo_nombre']} restaurado."

def mostrar_historial_consumos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM consumos ORDER BY fecha DESC")
    consumos = cursor.fetchall()
    conexion.close()
    return consumos

#________________________________________________________________________________________________________________