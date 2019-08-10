from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

import random
import myDB
import hashlib

@app.route("/logout", methods=["POST"])
def logout(): 
    data = request.get_json()
    sqlFormula = "UPDATE users SET loginStatus = %s, token = %s WHERE idusers = %s"
    sqlTuple = (0, random.randint(0, 999), data["idusers"])
    noError = myDB.sqlChange(sqlFormula, sqlTuple)

    return jsonify(noError)

@app.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():  
    

    data = request.get_json()

    h = hashlib.md5()
    h.update(data["password"].encode('utf-8'))
    h = h.hexdigest()

    sqlFormula = "SELECT password, token, idusers FROM users WHERE email = " + "\"" + data["email"] + "\""
        
    user = myDB.sqlQuery(sqlFormula)
    
    if user[0][0] == h:

        sqlFormula = "UPDATE users SET loginStatus = %s WHERE email = " + "\"" + data["email"] + "\""
        sqlTuple = (1, )
        myDB.sqlChange(sqlFormula, sqlTuple)

        response = {
            "token" : user[0][1],
            "idusers" : user[0][2]
        }
    
        res = make_response("token")
        res.set_cookie(key="token", value=str(response["idusers"]))

        return res

    response = {
        "token" : False,
        "idusers" : False
    }

    return res

@app.route("/verifylogin", methods=["POST"])
def verifyToken():

    data = request.get_json()

    sqlFormula = "SELECT token, loginStatus FROM users WHERE idusers = " + str(data["idusers"])
    
    query = myDB.sqlQuery(sqlFormula)
    token = query[0][0]
    loginStatus = query[0][1]
    
    if token == data["token"] and loginStatus == 1:
        
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
    noError = myDB.sqlChange(sqlFormula, sqlTuple)

    return jsonify(noError)


@app.route("/profile/<int:idusers>", methods=["GET"])
def getProfile(idusers):
    
    sqlFormula = "SELECT username, email FROM users WHERE idusers = " + str(idusers)
    query = myDB.sqlQuery(sqlFormula)

    data = {
        "username": query[0][0],
        "email": query[0][1]
    }
    
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

@app.route("/cookie")
def checkCookie():
    if not request.cookies.get('token'):
        res = make_response("Setting a cookie")
        res.set_cookie('token', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie token is {}".format(request.cookies.get('token')))
    return res

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000

