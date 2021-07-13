import os
from flask import Flask, request, Response, render_template,jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

fulllet_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',
             16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z',26: 'a', 27: 'b', 28: 'c', 29: 'd', 30: 'e',
            31: 'f', 32: 'g', 33: 'h', 34: 'i', 35: 'j', 36: 'k', 37: 'l', 38: 'm', 39: 'n', 40: 'o', 41: 'p', 42: 'q', 43: 'r',
            44: 's', 45: 't', 46: 'u', 47: 'v', 48: 'w', 49: 'x', 50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3', 56: '4',
            57: '5', 58: '6', 59: '7', 60: '8', 61: '9'}

let_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',
             16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}

#For word model

word_dict = {0: 'bhoy', 1: 'last', 2: 'Ned', 3: 'bide'}



app = Flask(__name__)

def load(modelname):
    global model
    model = load_model(modelname)
    model.summary()
    print('Loaded the model')

@app.route('/')
def index():
    return render_template('index.html', label='')


@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    response = {'success': False}
    if request.method == 'POST':
        if request.files.get('file'): # image is stored as name "file"
            img_requested = request.files['file'].read()
            img = image.load_img(img_requested, target_size = (112,112), color_mode = "grayscale")
            img = image.img_to_array(img)
            img /= 255
            img = image.flatten().reshape(-1,28,28,1)
            img = 1-img

            preds = model.predict(img)
            act_pred = let_dict(preds[0])

            response['predictions'] = []
            row = {'label': preds, 'Prediction': act_pred} # numpy float is not good for json
            response['predictions'].append(row)
            response['success'] = True
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    load('letter_model.h5')

    # To let this run on HEROKU, model.predict should run once after initialized
    app.run(port=5000, debug=True)