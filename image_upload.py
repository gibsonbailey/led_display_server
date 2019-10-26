import os, sys

from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

latest_upload_filename = ''
latest_upload_text = ''

UPLOAD_FOLDER = '/home/pi/led_project/media'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global latest_upload_filename
    global latest_upload_text

    print("UF", file=sys.stderr)
    if request.method == 'POST':
# check if the post request has the file part
        print("POST", file=sys.stderr)

        text = request.form.get('message')
        if text:
            latest_upload_text = text
            print(latest_upload_text, file=sys.stderr)
            # Send to LED Board and Redirect

        if 'file' not in request.files:
            print("No File", file=sys.stderr)
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            latest_upload_filename = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = url_for('uploaded_file', filename=filename)
            print('url for output', url, file=sys.stderr)
            return redirect(request.url)

    response = '''
    <!doctype html>
    <head>
    <link rel="icon" href="/uploads/Git-Logo-Black.png">
    </head>

    <title>Upload new File</title>

    <h1>Upload new File</h1>

    <form method=post enctype=multipart/form-data>
        <input type=text name=message>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    ''' 
    if latest_upload_text:
        header_tag = '<h4>{}</h4>'.format(latest_upload_text)
        response += header_tag
    if latest_upload_filename:
       image_tag = '<img src="/uploads/{}" style="width: 60%;">'.format(latest_upload_filename)
       response += image_tag
     
    return response
