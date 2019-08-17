from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

import random
import myDB
import hashlib
from myException import InvalidUsage

def tokenCheck(idusersPL, tokenPL):
    
    sqlFormula = "SELECT token, loginStatus FROM users WHERE idusers = " + idusersPL
    
    query = myDB.sqlQuery(sqlFormula)
    token = query[0][0]
    loginStatus = query[0][1]
    
    if token == int(tokenPL) and loginStatus == 1:
        return True 
    return False



@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response





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
        res.set_cookie(key="tokenPL", value=str(response["token"]), max_age=60*60*24*30)
        res.set_cookie(key="idusersPL", value=str(response["idusers"]), max_age=60*60*24*30)

        return res

    return

@app.route("/verifylogin", methods=["GET"])
@cross_origin(supports_credentials=True)
def verifyToken():

    try:
        tokenPL = request.cookies.get('tokenPL')
        idusersPL = request.cookies.get('idusersPL')
    except AttributeError as error:
        print(error)
        raise InvalidUsage("Erro ao fazer Login. Tente novamente." , status_code=401)

    
    sqlFormula = "SELECT token, loginStatus FROM users WHERE idusers = " + idusersPL
    
    query = myDB.sqlQuery(sqlFormula)
    token = query[0][0]
    loginStatus = query[0][1]
    

    if token == int(tokenPL) and loginStatus == 1:
        return "Success"
    return 

@app.route("/signup", methods=["POST"])
def signUp():

    data = request.get_json()

    h = hashlib.md5()
    h.update(data["password"].encode('utf-8'))
    h = h.hexdigest()
    
    sqlFormula = "INSERT INTO users (email, username, password, loginStatus, token, isActive, admin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    sqlTuple = (data["email"], data["username"], h, False, random.randint(0, 999), True, False)
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


@app.route("/edit/username", methods=["PUT"])
def editName():

    data = request.get_json()
    sqlFormula = "UPDATE users SET username = %s WHERE idusers = %s"
    sqlTuple = (data["username"], data["idusers"])
    noError = myDB.sqlChange(sqlFormula, sqlTuple)
    return jsonify(noError)

@app.route("/edit/email", methods=["PUT"])
def editEmail():

    data = request.get_json()
    sqlFormula = "UPDATE users SET email = %s WHERE idusers = %s"
    sqlTuple = (data["email"], data["idusers"])
    noError = myDB.sqlChange(sqlFormula, sqlTuple)
    return jsonify(noError)

@app.route("/edit/delete", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def editDelete():

    idusersPL = request.cookies.get('idusersPL')
    
    sqlFormula = "DELETE FROM users WHERE idusers = %s"
    sqlTuple = (idusersPL, )
    noError = myDB.sqlChange(sqlFormula, sqlTuple)
    
    return jsonify(noError)   

@app.route("/post/set", methods=["POST"])
@cross_origin(supports_credentials=True)
def setPost():

    try:
        tokenPL = request.cookies.get('tokenPL')
        idusersPL = request.cookies.get('idusersPL')
    except AttributeError as error:
        print(error)
        raise InvalidUsage("Erro na autenticação. Tente novamente." , status_code=401)

    if tokenCheck(idusersPL, tokenPL):

        data = request.get_json()
        sqlFormula = "INSERT INTO posts (idusers, text, time) VALUES (%s, %s, %s)"
        sqlTuple = (idusersPL, data["text"], data["time"])
        noError = myDB.sqlChange(sqlFormula, sqlTuple)
        
        if noError:
            return

    raise InvalidUsage("Erro ao salvar o post. Tente novamente." , status_code=410)
    

@app.route("/post/get/page/<int:page>/<int:perPage>", methods=["GET"])
def getPage(page, perPage):
    
    return

@app.route("/post/get/<int:idposts>", methods=["GET"])
def getPost(idposts):
    
    return




if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000

