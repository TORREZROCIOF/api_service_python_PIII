'''
Flask [Python]
Ejercicios de práctica

Autor: Ing.Jesús Matías González
Version: 2.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las usuarios registradas.

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

# Realizar HTTP POST con --> post.py

import traceback
from flask import Flask, request, jsonify, render_template_string, Response, redirect

import utils
import usuario

app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///usuarios.db"
# Asociamos nuestro controlador de la base de datos con la aplicacion
usuario.db.init_app(app)

""" @app.before_first_request
def before_first_request_func(): """
with app.app_context():
    # Borrar y crear la base de datos
    usuario.db.create_all()
    #usuario.db.drop_all()
    # Completar la base de datos
    usuario.fill()
    print("Base de datos generada")

@app.route('/user/<int:user_id>/titles')
def user_titles(user_id):
    count = usuario.title_completed_count(user_id)
    return f"El usuario con ID {user_id} ha completado {count} títulos."

@app.route('/user/graph')
def user_graph():
    users = usuario.report()
    x = []
    y = []
    
    for user in users:
        count_completed = usuario.title_completed_count(user["userId"])
        x.append(user["userId"])
        y.append(count_completed)

    image_html = utils.graficar(x, y)

    html = f'''
    <html>
        <body>
            <h1>Gráfico de títulos completados por usuario</h1>
            <img src="data:image/png;base64,{image_html}" alt="Gráfico de títulos completados por usuario">
        </body>
    </html>
    '''

    return render_template_string(html)


@app.route('/user/titles')
def user_titles_json():
    users = session.query(Usuario.userId).distinct()
    user_data = {user.userId: usuario.title_completed_count(user.userId) for user in users}
    return jsonify(user_data)


if __name__ == '__main__':
    print('JMRG@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
