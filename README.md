# Sistema de Gestión de Camas e Insumos - Enfermería (v1.0)

Aplicación de consola desarrollada en Python con base de datos relacional SQLite para el control de stock de insumos médicos, ocupación de 23 camas de internación y registro de consumos por paciente.

## Arquitectura
- `datos.py`: Conexión a SQLite, activación de claves foráneas y creación de tablas (`insumos`, `camas`, `consumos`).
- `logica.py`: Reglas de negocio, validaciones y transacciones atómicas de stock y consumos.
- `main.py`: Interfaz de usuario por consola con menús jerárquicos.

## Requisitos
- Python 3.x (usa únicamente librería estándar `sqlite3` y `os`).