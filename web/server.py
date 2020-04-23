from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/palindrome/<palabra>')
def es_palindrome(palabra):
    es = True
    for i in range(0,int(len(palabra)/2)):
        if palabra[i] != palabra[len(palabra)-i-1]:
            es = False
    return str(es)

@app.route('/multiplo/<numero1>/<numero2>')
def multiplo(numero1, numero2):
    es = False
    if int(numero2) != 0:
        if int(numero1)%int(numero2) == 0:
            es = True
    return str(es)

#Semana 3 - Lab:
@app.route('/create_user/<_name>/<_last>/<_password>/<_username>')
def create_user(_name, _last, _password, _username):
    user = entities.User(
        name = str(_name),
        fullname = str(_last),
        password = str(_password),
        username = str(_username)
    )
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "User created!"

@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    nombres = ""
    i = 0
    for user in users:
        print(i, "NAME:\t", user.name)
        i+=1
        nombres += user.name + " " + user.fullname + " " + user.password + " " + user.username + " " + "<br>"
    return nombres

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
