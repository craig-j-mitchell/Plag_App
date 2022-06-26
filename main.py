import sys, os, re
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import sqlite3 as sql
from config import *
from init_db import *



app = Flask(__name__)
app.secret_key = app_key


@app.route('/')
def welcome():
    return 'Welcome to Plag_App'


# on page '/upload' load display the upload file
@app.route('/upload')
def upload_form():
    return render_template('upload.html')


if not os.path.isdir(upload_dest):
    os.mkdir(upload_dest)

app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/upload', methods=['POST'])

# Database implementation

@app.route('/enternew')
def new_student():
   return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city,pin) VALUES(?, ?, ?, ?)",(nm,addr,city,pin) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)



def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

    files = request.files.getlist('files[]')

    for file in files:
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_dest, filename))
    flash('File(s) uploaded')
    return redirect('/upload')


if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:8080/upload')
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
