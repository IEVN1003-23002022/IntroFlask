from flask import Flask, render_template

app=Flask(__name__)

@app.route("/") #Etiquetas
def index():
    titulo="Pagina de Inicio"
    listado= ['Python', 'Flask', 'Jinjaz', 'HTML', 'CSS']
    return render_template("index.html", titulo=titulo, listado=listado)

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