from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/recuperacion')
def recuperacion():
    return render_template('recuperacion.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
