from flask import Flask, request

# UPLOAD_FOLDER = 'D:/uploads'

app = Flask(__name__)
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# import argparse
import requests
import numpy as np
from fuzzywuzzy import fuzz

import pandas as pd
from PIL import Image

import tensorflow as tf # TF2
import os
# print(os.__version__)
#import magic
import urllib.request
# from app import app
from flask import Flask, flash, request, redirect, render_template

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]



@app.route('/', methods=['GET','POST'])
def upload_file():

    if request.method == 'POST':
        # if request.files:
            print('hi')

            img = request.files["file"]
# {{url_for('static', filename='ayrton_senna_movie_wallpaper_by_bashgfx-d4cm6x6.jpg')}}
            img.save(os.path.join(os.getcwd()+'\static', img.filename))
            filename = img.filename

            interpreter = tf.lite.Interpreter(model_path="test 2.tflite")
            interpreter.allocate_tensors()

            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # check the type of the input tensor
            floating_model = input_details[0]['dtype'] == np.float32

            # NxHxWxC, H:1, W:2
            height = input_details[0]['shape'][1]
            width = input_details[0]['shape'][2]
            img = Image.open(img.filename).resize((width, height))

            # add N dim
            input_data = np.expand_dims(img, axis=0)

            if floating_model:
                input_data = (np.float32(input_data) - args.input_mean) / args.input_std

            interpreter.set_tensor(input_details[0]['index'], input_data)

            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
            results = np.squeeze(output_data)

            top_k = results.argsort()[-5:][::-1]
            labels = load_labels("test 2.txt")
            maxresult=[]
            for i in top_k:
                if floating_model:

                    maxresult.append('{:08.6f}: {}'.format(float(results[i]), labels[i]))
                else:
                    maxresult.append('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))

            print(maxresult[0].split(": ")[1])
            label = maxresult[0].split(": ")[1]
            
            # url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

            # querystring = {"ingr":label.lower()}

            # headers = {
            #     'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
            #     'x-rapidapi-key': "56c90952ccmshfa7a0287d1349e4p1bfb12jsn63e239475148"
            #     }

            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print(response)
            # res=response.json()
            # print('m res',res)
            # main=[]
            # for i in range(len(res["hints"])):

            #     if res["hints"][i]["food"]["category"] =="Generic foods" or res["hints"][i]["food"]["category"] =="Generic meals":
            #         if fuzz.partial_ratio(label.lower(),res["hints"][i]["food"]["label"].lower()) >=90:
            #             main.append(res["hints"][i]["food"]["nutrients"])

            # print(main)
            # print('hi')
            # df=pd.DataFrame(main).describe()

            # #output
            dframe = ''#df.iloc[1,:]

            # print(image)
            name=[label,filename,dframe]
        
            return render_template('result.html',name = name)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)