from flask import Flask, jsonify, request
from flask_cors import CORS

import random
import myDB
import hashlib

app = Flask(__name__)
CORS(app)


@app.route("/logout")
def logout(): 

    data = request.get_json()
    sqlFormula = "UPDATE users SET isActive = %s, token = %s WHERE idusers = %s"
    sqlTuple = (0, random.randint(0, 999), data["idusers"])
    myDB.sqlChange(sqlFormula, sqlTuple)

    return True

@app.route("/login", methods=["POST"])
def login():  

    data = request.get_json()

    h = hashlib.md5()
    h.update(data["password"].encode('utf-8'))
    h = h.hexdigest()

    sqlFormula = "SELECT password, token, idusers FROM users WHERE email = " + "\"" + data["email"] + "\""
        
    user = myDB.sqlQuery(sqlFormula)
    
    if user[0][0] == h:

        sqlFormula = "UPDATE users SET isActive = %s"
        sqlTuple = (1, )
        myDB.sqlChange(sqlFormula, sqlTuple)

        response = {
            "token" : user[0][1],
            "idusers" : user[0][2]
        }

        return jsonify(response)

    response = {
        "token" : False,
        "idusers" : False
    }

    return jsonify(response)

@app.route("/verifylogin", methods=["POST"])
def verifyToken():

    data = request.get_json()

    sqlFormula = "SELECT token FROM users WHERE idusers = " + str(data["idusers"])
    
    token = myDB.sqlQuery(sqlFormula)[0][0]
    
    if token == data["token"]:
        
        return jsonify(True)
        
    return jsonify(False)

@app.route("/signup", methods=["POST"])
def signUp():

    data = request.get_json()

    h = hashlib.md5()
    h.update(data["password"].encode('utf-8'))
    h = h.hexdigest()
    
    sqlFormula = "INSERT INTO users (email, username, password, loginStatus, token, isActive, admin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    sqlTuple = (data["email"], data["user"], h, False, random.randint(0, 999), True, False)
    myDB.sqlChange(sqlFormula, sqlTuple)
    return jsonify(data)

@app.route("/edit/name", methods=["PUT"])
def editName():

    data = request.get_json()
    sqlFormula = "UPDATE users SET name = %s WHERE idusers = %s"
    sqlTuple = (data["name"], data["idusers"])
    myDB.sqlChange(sqlFormula, sqlTuple)
    return

@app.route("/edit/email", methods=["PUT"])
def editEmail():

    data = request.get_json()
    sqlFormula = "UPDATE users SET email = %s WHERE idusers = %s"
    sqlTuple = (data["email"], data["idusers"])
    myDB.sqlChange(sqlFormula, sqlTuple)
    return

@app.route("/edit/delete", methods=["DELETE"])
def editDelete():

    data = request.get_json()
    sqlFormula = "DELETE FROM users WHERE idusers = %s"
    sqlTuple = (data["idusers"], )
    myDB.sqlChange(sqlFormula, sqlTuple)
    return    

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000

