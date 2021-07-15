from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import pytesseract
import pyttsx3
from flask import Flask, render_template
from summary.summary import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/summary")

app.config['UPLOAD_FOLDER'] = "images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("basic.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    # text="this is sample text"
    if request.method == 'POST':
        if request.form.get('myid') == "1":
            if request.files:
                if request.files['file'].filename != "":
                    print(1)
                    file = request.files['file']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        print(filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        text = pytesseract.image_to_string(img)
                        print(text)
        elif request.form.get('myid') == "2":
            return redirect('/summary')


        else:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()

    # return redirect(url_for('home1'))
    return render_template('result.html', text=text)
    # return redirect(f"/user",text)


if __name__ == "__main__":
    app.run(debug=True)
