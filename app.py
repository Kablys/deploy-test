from flask import Flask, request, render_template, url_for
from PIL import Image, ImageOps
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = os.path.join(app.root_path, 'static')
RESULT_FOLDER = os.path.join(STATIC_FOLDER, 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', result_url=None)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if not file or not file.filename:
        return "No selected file"
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Process the image
    image = Image.open(filepath)
    inverted_image = ImageOps.invert(image.convert('RGB'))
    result_path = os.path.join(RESULT_FOLDER, filename)
    inverted_image.save(result_path)

    # Pass the result image URL to the template
    result_url = url_for('static', filename=f'results/{filename}')
    return render_template('index.html', result_url=result_url)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
