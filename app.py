from flask import Flask, request, send_from_directory, send_file, render_template
from flask_restful import Resource, Api
from db import db_session
from models import Entry
from circlejerk import driver
import json
import os
import math

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def base():
    return render_template('index.html')

@app.route("/api")
def index():
    return render_template('index.html')

@app.route("/api/")
def index2():
    return render_template('index.html')


@app.route("/api/browser_upload", methods=['GET', 'POST'])
def browser_upload():
    connection = db_session()
    if request.method == 'POST':
        f = request.files['file']
        user = request.form['user']
        filePath = './static/files/'+f.filename
        augPath = './static/files/augmented'+f.filename
        f.save(filePath)
        results = driver(filePath)
        results[0].save(augPath)
        connection = db_session()
        if (connection.query(Entry).filter(Entry.filepath == filePath).first() is None):
            newFile = Entry(user, filePath, results[1])
            connection.add(newFile)
            connection.commit()

        #print(filePath)
        return {"status":True, "score":results[1], "filepath" : augPath[1:]}
    else:
        return render_template('index.html')

@app.route("/api/topten", methods=['GET','POST'])
def get_results():
    connection = db_session()
    results = connection.query(Entry).\
            order_by(Entry.score)
    Dict = {}
    if(results.count()>=10):
        for i in range(0,10):
            Dict[i] = {"username" : results[i].name,"score" : results[i].score}
        print(Dict)
    else:
        counter = 0
        for i in range(results.count()):
            Dict[i] = {"username" : results[i].name,"score" : results[i].score}
            counter+=1
        for i in range(counter,10):
            Dict[i] = {"username" : "", "score" : -1}
    return(Dict)

@app.route("/api/serveimage", methods=['GET','POST'])
def serve_image():
    connection = db_session()
    if request.method == 'POST':
        username = request.form['user']
    result = connection.query(Entry).filter(Entry.name == username).first()
    if result is None:
        return({"filepath" : "", "status": False})
    print(result)
    filepath = result.filepath.rsplit("/",3)
    filepath = filepath[-1]
    return({"filepath" : "/static/files/augmented"+filepath, "status": True})



if __name__ == "__main__":
    app.run(debug=True)
