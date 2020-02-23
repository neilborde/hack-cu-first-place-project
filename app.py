from flask import Flask, request, send_from_directory, send_file, render_template
from flask_restful import Resource, Api
from db import db_session
from models import Entry
import json
import os

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/api")
def index():
    return render_template('index.html')


@app.route("/api/browser_upload", methods=['GET', 'POST'])
def browser_upload():
    connection = db_session()
    if request.method == 'POST':
        f = request.files['file']
        user = request.form['user']
        connection = db_session()
        filePath = './server/files/'+f.filename
        # user = f.filename.rsplit('.',1)
        # user = user[0]
        if (connection.query(Entry).filter(Entry.filepath == filePath).first() is None):
            newFile = Entry(user, filePath)
            connection.add(newFile)
            connection.commit()
        # newFile = Entry('user', 'hello')
        # connection.add(newFile)
        # connection.commit()
        # fileTableEntry = connection.query(File).filter(File.filepath == filePath).first()
        # newPermission = Permission(fileTableEntry.fid, userTableEntry.uid)
        # connection.add(newPermission)
        # connection.commit()
        #print(filePath)
        f.save(filePath)
        return {"status":True}
    else:
        return render_template('index.html')


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
