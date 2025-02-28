from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static")
app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bd_laika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)

# Definición de rutas
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')

    user = Usuario.query.filter_by(correo=correo, contraseña=contraseña).first()

    if user:
        session['usuario_id'] = user.id
        session['nombre'] = user.nombre
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Correo o contraseña incorrectos', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/recuperacion')
def recuperacion():
    return render_template('recuperacion.html')

@app.route('/recovery', methods=['POST'])
def recovery_post():
    correo = request.form.get('correo')

    user = Usuario.query.filter_by(correo=correo).first()

    if user:
        flash('Se ha enviado un correo para recuperar tu cuenta', 'success')
    else:
        flash('El correo no está registrado', 'error')
    return redirect(url_for('login'))

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register', methods=['POST'])
def register_post():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')

    try:
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    except:
        db.session.rollback()
        flash('El correo ya está en uso', 'error')
        return redirect(url_for('registro'))

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

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/juguetes')
def juguetes():
    return render_template('juguetes.html')

@app.route('/snacks')
def snacks():
    return render_template('snacks.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/agregar_empleado')
def agregar_empleado():
    return render_template('agregar_empleado.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/agregar_cliente')
def agregar_cliente():
    return render_template('agregar_cliente.html')

@app.route('/sucursales')
def sucursales():
    return render_template('sucursales.html')


# Ejecutar la app en modo debug solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
