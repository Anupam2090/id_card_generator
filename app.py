from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os

from config import PHOTO_FOLDER, UPLOAD_FOLDER, ID_CARD_FOLDER, EXCEL_PATH, ALLOWED_EXTENSIONS
from utils.generator import generate_id_cards

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ID_CARD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('excel')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Optionally overwrite EXCEL_PATH
            generate_id_cards(filepath, PHOTO_FOLDER, ID_CARD_FOLDER)



            return redirect(url_for('index'))

    images = os.listdir(ID_CARD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/static/id_cards/<filename>')
def serve_image(filename):
    return send_from_directory(ID_CARD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
