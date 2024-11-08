# importamos las clases y metodos
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def aritmetica():
    if request.method == "POST":
        # Valores que recibo del form n1, n2 son pasados
        num1 = float(request.form.get('n1'))
        num2 = float(request.form.get('n2'))
        # Realizamos operaciones aritmeticas
        suma = num1 + num2
        resta = num1 - num2
        multiplicacion = num1 * num2
        division = num1 / num2
        return render_template('index.html', total_suma=suma,
                               total_resta=resta,
                               total_multiplicacion=multiplicacion,
                               total_division=division)

    return render_template('index.html')

@app.route('/divisa', methods=['GET', 'POST'])
def divisa():
   if request.method == "POST":
        # Valores que recibo del form n1, n2 son pasados
        num3 = float(request.form.get('n3'))
        
        # Realizamos operaciones aritmeticas
        
        multiplicacion = num3 * 4398
        return render_template('divisa.html', total_multiplicacion=multiplicacion
                               )
   return render_template('divisa.html')
   
if __name__ == "__main__":
    app.run(debug=True)
