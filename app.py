from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    if file and allowed_file(file.filename):
        # Save the image to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'Image uploaded successfully', 'path': filepath}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Image Upload API! Use POST /upload to upload an image.'})

if __name__ == '__main__':
    app.run(debug=True)
