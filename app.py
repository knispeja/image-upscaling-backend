# Restore trained data
import tensorflow as tf
import numpy as np
import sys
from scipy import misc

# Define TF model
from modules.utils import *
from modules.model import *

SCALE = 4
INPUT_SIZE = Dimensions(1080//4, 1920//4)
OUTPUT_SIZE = Dimensions(INPUT_SIZE.h*SCALE, INPUT_SIZE.w*SCALE)

sess = tf.Session()

def upscaler(in_tensor, in_channels, f_1, f_r, f_u, out_channels):
    upscale_model = Model("Upscaler", in_tensor)
    upscale_model.full_conv2d(3,f_1)
    upscale_model.relu()

    upscale_model.add_residual_block(f_1,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_1,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)
    upscale_model.add_residual_block(f_r,f_r)

    upscale_model.upscale([OUTPUT_SIZE.h//2,OUTPUT_SIZE.w//2])
    upscale_model.full_conv2d(f_r,f_u, mapsize=3)
    upscale_model.relu()
    
    upscale_model.upscale([OUTPUT_SIZE.h,OUTPUT_SIZE.w])
    upscale_model.full_conv2d(f_u,f_u, mapsize=3)
    upscale_model.relu()
    
    upscale_model.full_conv2d(f_u, 3, mapsize=1)
    upscale_model.rgb_bound()
    upscale_model.reshape([-1,OUTPUT_SIZE.h*OUTPUT_SIZE.w*3])
    return upscale_model

small_train = tf.placeholder('float32', shape = [None, INPUT_SIZE.h, INPUT_SIZE.w, 3])
upscale_model = upscaler(small_train, 3, 64, 64, 64, 3)
pred = tf.reshape(tf.cast(upscale_model.get_output(), dtype=tf.uint8),[-1,OUTPUT_SIZE.h, OUTPUT_SIZE.w, 3])
init = tf.initialize_all_variables()
sess.run(init)

saver = tf.train.Saver(upscale_model.variables)
saver.restore(sess, "s-1")

def upscale_image(input):
    return sess.run(pred, feed_dict={small_train: np.array([misc.imread(input, mode='RGB')])})[0]

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

            misc.imsave(upscaledPath, upscale_image(uploadedPath))

            return url_for('static', filename=upscaledPath[7:]) 
        else:
            print('File did not exist', file=sys.stderr)
    return 

@app.route('/')
def main():
    return render_template('index.html')