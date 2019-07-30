from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello!"

@app.route("/login", methods=["POST"])
def login():
    return "fala mané"

@app.route("/signup", methods=["POST"])
def signUp():
    data = request.get_json()
    print(data)
    return jsonify(data)

@app.route("/edit/name", methods=["PUT"])
def editName():
    return

@app.route("/edit/email", methods=["PUT"])
def editEmail():
    return

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000