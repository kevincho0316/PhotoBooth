import io
import json
import os

# import elon_filter
# import arcane_filter
# import depth_filter
import socket


# from torchvision import models
# import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask import render_template
import os
import zipfile
from glob import glob
B_path= os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

# html 연결
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        id = request.form.get('id')
        types = request.form.get('type')
        zip_f = request.files['zip']     
        input_file = os.path.join(B_path, types, 'before', zip_f.filename)
        output_zip = os.path.join(B_path, types, 'before', zip_f.filename[:-3])
        zip_f.save(input_file)

        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(output_zip)

        os.remove(os.path.join(types, 'before', zip_f.filename))


        if types == 'elon':
            output_file = 'el'
        elif types == 'depth':
            output_file = 'dep'
        elif types == 'arcane':
            output_file = 'arc'
        





        return jsonify({'id': id, 'file': 'http://'+socket.gethostbyname(socket.getfqdn())+'/'+output_file})
        