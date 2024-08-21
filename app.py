from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #funcion para cargar el archivo hmtl (el index) 
template_dir = os.path.join(template_dir, 'src', 'templates' )              #a la app flask 

app = Flask (__name__, template_folder = template_dir)

#ruta y metodo de renderizado de la aplicacion con flask
@app.route('/')
def home():
    cursor = db.database.cursor() #cargar la funcion para la conexion a la base de datos en la variable
    cursor.execute("SELECT * FROM users") #selecciona toda la informacion de la base de datos
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject) #renderiza la pagina web con los datos anteriores

#Ruta y metodo para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor() #usa la variable cursor creada anteriormente para acceder a la base de datos 
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data) #execute es un metodo de sql para usar una query y añadirle una veriable con informacion
        db.database.commit()
    return redirect(url_for('home')) #en cada ejecucion del motodo la pagina se actualiza redirigiendose al home

#Ruta y metodo para eliminar usuarios en la bdd
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))
    
#Ruta y metodo para editar usuarios en la bdd
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


#se usa el puerto 4000 del localhost
if __name__ == '__main__':
    app.run(debug=True, port=4000)
