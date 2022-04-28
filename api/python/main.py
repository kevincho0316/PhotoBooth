import io
import json
import os

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
        ID = request.form.get('id')
        types = request.form.get('type')
        file = request.files['pic']
        file.save(os.path.join(app.instance_path,  types, 'before', file.filename))
        




        return jsonify({'id': ID, 'type':types, 'file': file.filename})
        
if __name__ == '__main__':
    app.run()