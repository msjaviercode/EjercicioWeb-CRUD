from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #function to load the HTML file (the index) 
template_dir = os.path.join(template_dir, 'src', 'templates' )              #to the Flask app

app = Flask (__name__, template_folder = template_dir)

#route and rendering method for the application with Flask
@app.route('/')
def home():
    cursor = db.database.cursor() #load the function for the database connection into the variable
    cursor.execute("SELECT * FROM users") #selects all information from the database
    myresult = cursor.fetchall()
    # convert the data to a dictionary
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject) #renders the webpage with the previous data

#Route and method to save users in the database
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username'] #request retrieves the information from HTML using the given parameter
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor() #uses the previously created cursor variable to access the database
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data) #execute is a MySQL method to use a query and add a variable with information
        db.database.commit() #commit executes the order ("sends" the data)
    return redirect(url_for('home')) #each time the method runs, the page refreshes, redirecting to home

#Route and method to delete users in the database
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()# connection to the database
    sql = "DELETE FROM users WHERE id=%s" # delete a user from the database using the ID
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))
    
#Route and method to edit the users from the database
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


#initializes the app with the framework Flask and using the port 4000 in localhost
if __name__ == '__main__':
    app.run(debug=True, port=4000)
