from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, send_file
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Batas ukuran file 10MB
app.secret_key = 'your_secret_key'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'removed_' + filename)
        
        input_image = Image.open(filepath)
        output_image = remove(input_image)
        
        # Increase resolution
        new_size = (input_image.width * 2, input_image.height * 2)
        output_image = output_image.resize(new_size, Image.LANCZOS)
        
        output_image.save(output_path)
        
        return redirect(url_for('result', filename=filename))
    else:
        flash('File type is not allowed')
        return redirect(request.url)

@app.route('/result/<filename>')
def result(filename):
    original_file = url_for('static', filename='uploads/' + filename)
    processed_file = url_for('static', filename='uploads/removed_' + filename)
    return render_template('result.html', original_file=original_file, processed_file=processed_file, filename=filename)

@app.route('/download/<filename>/<format>')
def download_file(filename, format):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'removed_' + filename)
    image = Image.open(file_path)
    
    if format not in ALLOWED_EXTENSIONS:
        flash('File format not allowed')
        return redirect(url_for('result', filename=filename))
    
    new_filename = f"removed_{filename.rsplit('.', 1)[0]}.{format}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    image.save(output_path, format.upper())
    
    return send_file(output_path, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File size exceeds maximum limit of 10MB')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
