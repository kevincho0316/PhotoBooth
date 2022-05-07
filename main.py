import io
import json
import os

import elon_filter
import arcane_filter
import depth_filter


# from torchvision import models
# import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask import render_template


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
        file1 = request.files['pic1']               #    id-1,id-2 로 요청한다
        file2 = request.files['pic2']
        file3 = request.files['pic3']
        file4 = request.files['pic4']

        input_file1 = os.path.join(app.instance_path,  types, 'before', file1.filename)
        file1.save(input_file1)
        
        input_file2 = os.path.join(app.instance_path,  types, 'before', file2.filename)
        file1.save(input_file2)
        
        input_file3 = os.path.join(app.instance_path,  types, 'before', file3.filename)
        file1.save(input_file3)
        
        input_file4 = os.path.join(app.instance_path,  types, 'before', file4.filename)
        file1.save(input_file4)
        
        if types == 'elon':
            output_file = elon_filter.elon_sticker(input_file1,input_file2,input_file3,input_file4)
        elif types == 'depth':
            output_file = depth_filter.filter(input_file1,input_file2,input_file3,input_file4)
        elif types == 'arcane':
            output_file = arcane_filter.filter(input_file1,input_file2,input_file3,input_file4)
        





        return jsonify({'id': id, 'file': output_file})
        
if __name__ == '__main__':
    app.run()