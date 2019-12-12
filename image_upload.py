import os, sys, signal
import os.path
import json

from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from os import path

latest_upload_filename = ''
latest_upload_text = ''
child_pid = None

PROJECT_BASE = os.path.dirname(__file__)
PROCESS_1 = os.path.join(PROJECT_BASE, 'testprocess1.py')
PROCESS_2 = os.path.join(PROJECT_BASE, 'testprocess2.py')
UPLOAD_FOLDER = os.path.join(PROJECT_BASE, 'media')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def start_new_child(filename):
    global child_pid
    if child_pid:
        os.kill(child_pid, signal.SIGKILL)
        os.wait()
    child_pid = os.fork()
    
    print("Child PID: " + str(child_pid), file=sys.stderr)
    if child_pid == 0:
        command = [filename]
        os.execvp(command[0], command)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/text_uploads', methods=['GET'])
def get_text_data():
    response = ''
    with open('data.txt', 'r+') as f:
        response = f.readlines()
        f.close()
    for i in range(len(response)):
        response[i] = response[i][:-1]
    return json.dumps(response)

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/index', methods=['GET'])
def serve_homepage():
    return send_from_directory('/home/brendon/led_display_server', 'index.html')

@app.route('/js/app.js', methods=['GET'])
def serve_react():
    return send_from_directory('/home/brendon/led_display_server/js', 'app.js')

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
            with open('data.txt', 'a') as f:
                f.write(text + '\n')
                f.close()
                
            print(latest_upload_text, file=sys.stderr)
            # Send to LED Board and Redirect
            # if PIDEXISTS, KILL 
            # FORK PROCESS1
            start_new_child(PROCESS_1)


        else:
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
    
                # if PIDEXISTS, KILL 
                # FORK PROCESS2
                
                start_new_child(PROCESS_2)
    
    
                return redirect(request.url)

    with open("website.html") as f:    
        response = f.read()
        f.close()

    latest_upload_pathname = os.path.join(PROJECT_BASE, latest_upload_filename)

    print(latest_upload_pathname)

    if latest_upload_text:
        header_tag = '<h4>{}</h4>'.format(latest_upload_text)
        response += header_tag
    if latest_upload_filename and not os.path.exists(latest_upload_pathname):
       image_tag = '<img src="/uploads/{}" style="width: 60%;">'.format(latest_upload_filename)
       response += image_tag
    
    with open("website.html", "w") as outf:
        outf.write(response)
        outf.close()

    return response
