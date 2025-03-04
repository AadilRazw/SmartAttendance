from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from main import main

app = Flask(__name__)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Basic route
@app.route('/')
def home():
    return "Hello, Flask!"

# Upload route to handle image uploads
@app.route('/compare', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        res = main(file_path)
        return jsonify({'message': 'Image uploaded successfully', 'file_path': res}), 200

    return jsonify({'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
