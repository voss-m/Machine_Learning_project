import os
from flask import request, render_template
from app import app
from flask_wtf.csrf import CSRFError
import cv2
from .face_recognition import pipeline_model

filename = None


def crop_picture(filename):
    directory = app.config["UPLOAD_FOLDER"]
    image = cv2.imread(os.path.join(directory, filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        cv2.imwrite(os.path.join(directory, filename), roi_color)


@app.route('/results')
def uploaded_file():
    global filename
    directory = app.config["UPLOAD_FOLDER"]
    image = cv2.imread(os.path.join(directory, filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        cv2.imwrite(os.path.join(directory, filename), roi_color)
    img = cv2.imread(os.path.join(directory, filename))
    result, score = pipeline_model(img)
    return render_template('results.html', filename=filename, result=result, score=round(score, 2))


@app.route('/', methods=['GET', 'POST'])
def upload():
    global filename
    if request.method == 'POST':
        file = request.files['file']
        # filename = secure_filename(file.filename)
        filename = "upload.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file'))
    return render_template('model.html')


# handle CSRF error
@app.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400


@app.route('/about', methods=['GET'])
def about_project():
    return render_template('about_project.html')


@app.route('/authors', methods=['GET'])
def about_us():
    return render_template('about_us.html')


@app.after_request
def add_header(response):
    response.cache_control.max_age = 10
    return response


