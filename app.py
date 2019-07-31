from flask import Flask, jsonify, request
from flask_cors import CORS

import random
import myDB

app = Flask(__name__)
CORS(app)


@app.route("/")
def home(): 
    return "Hello!"

@app.route("/login", methods=["POST"])
def login():
    return "login"

@app.route("/signup", methods=["POST"])
def signUp():
    data = request.get_json()
    print(data)
    sqlFormula = "INSERT INTO users (email, username, password, loginStatus, token, isActive, admin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sqlTuple = (data["email"], data["user"], hash(data["password"]), False, random.randint(0, 999), True, False)
    myDB.sqlQuery(sqlFormula, sqlTuple)
    return jsonify(data)

@app.route("/edit/name", methods=["PUT"])
def editName():
    return

@app.route("/edit/email", methods=["PUT"])
def editEmail():
    return

@app.route("/edit/delete", methods=["DELETE"])
def editDelete():
    return    

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000

