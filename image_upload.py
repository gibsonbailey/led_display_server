import os
import flask
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/pi/led_project/media/'
ALLOWED_EXTENSIONS = {''}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


