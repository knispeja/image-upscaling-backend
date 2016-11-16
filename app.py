# Restore trained data
import tensorflow as tf
import numpy as np
import sys

#TODO...


# Web app
from flask import Flask, jsonify, render_template, request
from datetime import datetime
import os.path

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/api', methods=['POST'])
def upscaler():

    for f in request.files:
        file = request.files[f]
        if file:
            print("File uploaded for upscaling", file=sys.stderr)
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            break
        else:
            print('File did not exist', file=sys.stderr)
    
    return jsonify({"success":True})

@app.route('/')
def main():
    return render_template('index.html')