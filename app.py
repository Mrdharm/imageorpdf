from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid
from pdf2image import convert_from_bytes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert-image-to-pdf', methods=['POST'])
def image_to_pdf():
    files = request.files.getlist('images')
    output_name = request.form.get('output_name', 'converted')
    output_filename = f"{output_name}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    images = []
    for file in files:
        if file and file.filename != '':
            img = Image.open(file).convert('RGB')
            images.append(img)

    if not images:
        return "No images uploaded.", 400

    images[0].save(output_path, save_all=True, append_images=images[1:])
    return send_file(output_path, as_attachment=True)

@app.route('/convert-pdf-to-image', methods=['POST'])
def pdf_to_image():
    file = request.files.get('pdf_file')
    output_name = request.form.get('output_name', 'converted_image')
    if not file or file.filename == '':
        return "No PDF uploaded.", 400

    images = convert_from_bytes(file.read())
    saved_images = []

    for i, image in enumerate(images):
        filename = f"{output_name}_page{i+1}.png"
        path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(path, 'PNG')
        saved_images.append(path)

    # Return first image (for demo)
    return send_file(saved_images[0], as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
