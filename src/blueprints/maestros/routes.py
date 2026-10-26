from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


# 1. LISTAR MAESTROS (GET /maestros o /maestros/)
@maestros_bp.route("/", strict_slashes=False, methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()

        maestros = []
        for fila in datos:
            maestro = {
                "idmaestro": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)

        return jsonify({'maestros': maestros, 'mensaje': "Lista de maestros", 'exito': True}), 200

    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

    finally:
        if cursor is not None:
            cursor.close()


# 2. CONSULTAR UN MAESTRO (GET /maestros/<idmaestro>)
@maestros_bp.route("/<int:idmaestro>", methods=['GET'])
def leer_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros WHERE idmaestro = %s", (idmaestro,))
        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        maestro = fila_a_diccionario(cursor, fila)
        return jsonify({
            'maestro': maestro,
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f'Error al consultar maestro: {ex}',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# 3. REGISTRAR MAESTRO (POST /maestros o /maestros/)
@maestros_bp.route("/", strict_slashes=False, methods=['POST'])
def registrar_maestro():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    campos = ['nombre', 'apaterno', 'amaterno', 'correo']
    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios',
            'exito': False
        }), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO maestros (nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s)
        """, tuple(datos[campo].strip() for campo in campos))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'idmaestro': cursor.lastrowid,
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': f'Error al registrar maestro: {ex}',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route("/<int:idmaestro>", methods=['PUT'])
def modificar_maestro(idmaestro):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "No se recibieron datos para modificar",
            "exito": False
        }), 400

    # Obtener el nuevo id si viene en el JSON, o conservar el actual de la URL
    nuevo_id = datos.get('idmaestro', idmaestro)
    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno')
    correo = datos.get('correo')

    if not nombre or not apaterno or not correo:
        return jsonify({
            "mensaje": "Nombre, apellido paterno y correo son obligatorios",
            "exito": False
        }), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()

        # 1. Validar que el maestro que se quiere editar existe
        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe el maestro",
                "exito": False
            }), 404

        # 2. Si se solicitó cambiar el ID, verificar que el nuevo ID no esté ocupado
        if nuevo_id != idmaestro:
            cursor.execute(
                "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
                (nuevo_id,)
            )
            if cursor.fetchone() is not None:
                return jsonify({
                    "mensaje": f"El idmaestro {nuevo_id} ya está en uso",
                    "exito": False
                }), 409

        # 3. Actualizar los campos incluyendo idmaestro
        sql = """
            UPDATE maestros
            SET idmaestro = %s,
                nombre = %s,
                apaterno = %s,
                amaterno = %s,
                correo = %s
            WHERE idmaestro = %s
        """

        cursor.execute(sql, (
            nuevo_id,
            nombre.strip(),
            apaterno.strip(),
            amaterno.strip() if amaterno else '',
            correo.strip(),
            idmaestro  # El ID original que viene en la URL
        ))
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Maestro modificado correctamente",
            "idmaestro_anterior": idmaestro,
            "idmaestro_actual": nuevo_id,
            "exito": True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al modificar el maestro',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()



@maestros_bp.route("/<int:idmaestro>", methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe el maestro",
                "exito": False
            }), 404

        cursor.execute(
            "DELETE FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Maestro eliminado correctamente",
            "idmaestro": idmaestro,
            "exito": True
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al eliminar el maestro',
            'error': str(e),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()