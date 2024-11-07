from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f"Usuario:{self.userId} - Title {self.title}"


def insert(userId, title,completed):
    # Crear una nueva Usuarios
    user = Usuario(userId=userId, title=title, completed=completed)

    # Agregar la Usuarios a la DB
    db.session.add(user)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las usuarios
    query = db.session.query(Usuario)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Usuario podría tener una función
    # para pasar a JSON/diccionario
    for usuario in query:
        json_result = {'userId': usuario.userId, 'title': usuario.title, 'completed': usuario.completed}
        json_result_list.append(json_result)

    return json_result_list

def dashboard():

    query = db.session.query(Usuario)
    
    userIds = []
    titles = []
    completed = []

    for usuario in query:
        user = {usuario.name}
        userIds.append(user)
        title = {usuario.title}
        titles.append(title)
        completed = {usuario.completed}
        completeds.append(completed)

    return userIds, titles, completeds

""" # Esquema del ejercicio
- Deben crear su archivo de python "app.py" y crear las funciones mencionadas en este documento. Deben crear la sección "if _name_ == "_main_" y ahí lanzar el server Flask
- Crear la funciones mencionadas para poder invocar a los endpoints que explorarán los datos.
- Deberán crear y completar la base de datos dentro del método que se invoca la primera vez que lanzamos la aplicación """
def fill():
    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data = response.json()

    for item in data:
        insert(userId=item['id'],title=item['userId'],completed=item['completed'])

def title_completed_count(user_id):
    return db.session.query(Usuario).filter(Usuario.userId == user_id, Usuario.completed == True).count()

if __name__ == "__main__":
    # Crear una aplicación Flask para testing
    # y una base de datos fantasma (auxiliar o dummy)
    # Referencia:
    # https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"
    # Bindear la DB con nuestra app Flask
    db.init_app(app)
    app.app_context().push()

    db.create_all()

    # Aquí se puede ensayar todo lo que necesitemos con nuestra DB
    # ...
    insert("Rocio","Profesora",False)
    datos = report()
    print(datos)
    
    #dashboard()
        
    db.session.remove()
    db.drop_all()