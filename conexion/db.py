import sqlite3

def get_db_connection():
    """Obtiene una conexión a la base de datos."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados por nombre de columna
    return conn

def create_tables():
    """Crea las tablas necesarias si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla para los usuarios (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Tabla para los estudiantes (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        email TEXT NOT NULL,
        grade REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
