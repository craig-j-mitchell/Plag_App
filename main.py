import sys, os, re
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from config import *

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
