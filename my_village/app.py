from flask import Flask, render_template, request, jsonify, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file types for upload (images and videos)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

# Helper function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve the main page (optional, in case you need to render HTML from Flask)
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files[]')
    file_urls = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_urls.append(url_for('static', filename=f'uploads/{filename}'))

    return jsonify(file_urls)

# Endpoint to fetch uploaded files for the gallery
@app.route('/gallery', methods=['GET'])
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_urls = [
        {
            'name': file,
            'url': url_for('static', filename=f'uploads/{file}'),
            'type': 'video' if file.lower().endswith(('mp4', 'mov', 'avi')) else 'image'
        }
        for file in files
    ]
    return jsonify(file_urls)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
