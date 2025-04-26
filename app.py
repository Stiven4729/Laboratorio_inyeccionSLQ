from flask import Flask, render_template, request, redirect, url_for
from conexion.db import create_tables, get_db_connection

app = Flask(__name__)

# Crear tablas al iniciar la app si no existen
create_tables()

# Ruta principal (Login)
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'")
            result = cursor.fetchone()
            if result:
                return redirect(url_for('panel'))
            else:
                error = "❌ Usuario o contraseña incorrectos"
        except Exception as e:
            error = str(e)
        conn.close()

    return render_template('login.html', error=error)

# Ruta para registrar usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        if cursor.fetchone():
            message = "⚠️ El usuario ya existe"
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            message = "✅ Usuario registrado correctamente"

        conn.close()

    return render_template('register.html', message=message)

# Ruta del panel administrativo
@app.route('/panel')
def panel():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, grade FROM students")
    estudiantes = cursor.fetchall()
    conn.close()
    return render_template('panel.html', estudiantes=estudiantes)

# Ruta para registrar un estudiante
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    msg = None
    if request.method == 'POST':
        name = request.form['name']
        program = request.form['program']
        email = request.form['email']
        grade = request.form['grade']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, program, email, grade) VALUES (?, ?, ?, ?)",
                       (name, program, email, grade))
        conn.commit()
        conn.close()
        msg = "✅ Estudiante registrado correctamente"
    return render_template('add_student.html', message=msg)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    return redirect(url_for('login'))  # Redirige al login después de cerrar sesión


# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
