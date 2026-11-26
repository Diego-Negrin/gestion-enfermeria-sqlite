import sqlite3
import os

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(CARPETA_ACTUAL, "enfermeria.db")

def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def inicializar_bd():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. Crear tabla insumos (si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL,
            descripcion TEXT
        )
    """)

    # 2. Crear tabla de Camas (si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camas (
            numero INTEGER PRIMARY KEY,
            estado TEXT NOT NULL DEFAULT 'Libre',
            paciente_nombre TEXT,
            motivo_internacion TEXT
        )
    """)

    # 3. Crear tabla de consumos (si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cama_numero INTEGER NOT NULL,
            paciente_nombre TEXT NOT NULL,
            insumo_id INTEGER NOT NULL,
            insumo_nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            procedimiento TEXT NOT NULL,
            FOREIGN KEY (cama_numero) REFERENCES camas(numero),
            FOREIGN KEY (insumo_id) REFERENCES insumos(id)
        )
    """)

    for numero in range(1, 24):
        cursor.execute("INSERT OR IGNORE INTO camas (numero, estado) VALUES (?, 'Libre')", (numero,))

    conexion.commit()
    conexion.close()

