# Restore trained data
import tensorflow as tf
import numpy as np
import sys

# TODO: define TF model like below
# x = tf.placeholder("float", [None, 784])
# sess = tf.Session()

# with tf.variable_scope("convolutional"):
#     keep_prob = tf.placeholder("float")
#     y2, variables = model.convolutional(x, keep_prob)
# saver = tf.train.Saver(variables)
# saver.restore(sess, "mnist/data/convolutional.ckpt")
# def convolutional(input):
#     return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()

# Web app
from flask import Flask, render_template, request, url_for
from datetime import datetime
import os.path

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploaded'
app.config['UPSCALE_FOLDER'] = 'static/upscaled'

@app.route('/api', methods=['POST'])
def upscaler():
    for f in request.files:
        file = request.files[f]
        if file:
            print("File uploaded for upscaling", file=sys.stderr)
            now = datetime.now()
            filename = "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1])
            uploadedPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upscaledPath = os.path.join(app.config['UPSCALE_FOLDER'], filename)
            file.save(uploadedPath)

            # TODO: put image through restored TF model and save it at upscaledPath

            # TODO: replace filename below with TF output saved at upscaledPath
            return url_for('static', filename=uploadedPath[7:]) 
        else:
            print('File did not exist', file=sys.stderr)
    return 

@app.route('/')
def main():
    return render_template('index.html')