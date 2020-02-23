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
        return {"status":True, "score":results[1]}
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
            Dict[i] = {"username" : results[i].name,"score" : math.floor(results[i].score)}
        print(Dict)
    else:
        counter = 0
        for i in range(results.count()):
            Dict[i] = {"username" : results[i].name,"score" : math.floor(results[i].score)}
            counter+=1
        for i in range(counter,10):
            Dict[i] = {"username" : "", "score" : -1}
    return(Dict)





# @app.route("/api/browser_download", methods=['GET', 'POST'])
# def browser_download():
#     if request.method == 'POST' and os.path.exists('auth.txt'):
#
#         r = request.json
#         file = r['file']
#         connection = db_session()
#         uid = connection.query(User.uid).filter(User.username == r['username'], User.password == r['password']).first()
#         fid = connection.query(File.fid).filter(File.filename == file).first()
#         if (uid is not None and fid is not None):
#             if (connection.query(Permission).filter(Permission.fid == fid[0], Permission.uid == uid[0]).first() is not None):
#                 w = connection.query(File.filepath).filter(File.fid == fid).first()[0]
#                 f = os.path.abspath(w)
#                 return send_file(os.path.dirname(f) + '/' + file,attachment_filename=file,as_attachment=True)
#
#         return {'file':False}
#     else:
#         return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
