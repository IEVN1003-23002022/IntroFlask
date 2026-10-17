from flask import Flask, render_template, request
import math

app=Flask(__name__)

@app.route("/") 
def index():
    titulo="Pagina de Inicio"
    listado= ['Python', 'Flask', 'Jinjaz', 'HTML', 'CSS']
    return render_template("index.html", titulo=titulo, listado=listado)


@app.route("/operasbas", methods=["GET","POST"])
def operasbas():
    n1 = 0
    n2 = 0
    res = 0
    operacion = ''
    opera=''


    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        operacion = request.form.get('operacion')
        

        if request.form.get('operacion') == 'suma':
            res = float(n1) + float(n2)
            opera = '+'

        
        if request.form.get('operacion') == 'resta':
            res = float(n1) - float(n2)
            opera = '-'
        
        if request.form.get('operacion') == 'multiplicacion':
            res = float(n1) * float(n2)
            opera = '*'
        
 
    return render_template('operasbas.html', n1=n1, n2=n2, res=res, operacion=operacion, opera=opera)
    

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    resultado = 0
    calculado = False

    if request.method == 'POST':
        x1 = float(request.form.get('x1', 0))
        y1 = float(request.form.get('y1', 0))
        x2 = float(request.form.get('x2', 0))
        y2 = float(request.form.get('y2', 0))


        resultado = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        calculado = True

    return render_template('distancia.html', x1=x1, y1=y1, x2=x2, y2=y2, resultado=resultado, calculado=calculado)









@app.route ("/hola") 
def hola():
    return "<h1> Hola PWA - IEVN1003 </h1>"

@app.route ("/user/<string:nom>") 
def user(nom):
    return "<h1> Hola User: {} </h1>" .format(nom)

@app.route ("/numero/<int:n>") 
def numero(n):
    return "<h1> Numero: {} </h1>" .format(n)

@app.route ("/user/<int:id>/<string:username>") 
def username(id,username):
    return "<h1> ID: {} nombre: {} </h1>" .format(id,username)

@app.route ("/sum/<float:n1>/<float:n2>") 
def func(n1,n2):
    return "<h1> La suma es: {} </h1>" .format(n1+n2)

if __name__=="__main__":
    app.run(debug=True)