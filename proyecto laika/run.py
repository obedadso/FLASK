from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
import string

app = Flask(__name__, static_folder="static")

# Configuración de la base de datos MySQL
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tienda_laika.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Modelo de Productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Modelo de Empleados
class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)

# Modelo de Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

# Ruta principal
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("El correo ya está registrado. Intenta con otro.", "danger")
            return redirect(url_for('registro'))

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and bcrypt.check_password_hash(usuario.password, password):
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nombre', None)
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('login'))

# Generar nueva contraseña aleatoria
def generar_nueva_contrasena():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(10))

# Recuperación de contraseña
@app.route('/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        email = request.form['email']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            nueva_contrasena = generar_nueva_contrasena()
            usuario.password = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
            db.session.commit()

            flash(f"Tu nueva contraseña es: {nueva_contrasena}. Cámbiala después de iniciar sesión.", "info")
            return redirect(url_for('login'))
        else:
            flash("Correo no encontrado.", "danger")

    return render_template('recuperacion.html')

# Otras páginas
@app.route('/gatos')
def gatos():
    return render_template('gatos.html')

@app.route('/perros')
def perros():
    return render_template('perros.html')

@app.route('/accesorios')
def accesorios():
    return render_template('accesorios.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Crear la base de datos y ejecutar la app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
