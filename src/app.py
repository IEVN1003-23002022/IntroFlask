from flask import Flask
from flask_cors import CORS
from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp
from database import mysql
from config import config

app = Flask(__name__)

app.config.from_object(config['development'])

mysql.init_app(app)
CORS(app)

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

app.register_error_handler(404, pagina_no_encontrada)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
