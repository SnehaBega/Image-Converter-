# pip install flask opencv-python
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
import os, cv2

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'webp', 'grayscale'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and the filename is {filename}")
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    newfilename = None
    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newfilename = f"{filename.rsplit('.', 1)[0]}_gray.png"
        cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], newfilename), imgProcessed)
    elif operation == "cpng":
        newfilename = f"{filename.rsplit('.', 1)[0]}.png"
        cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], newfilename), img)
    elif operation == "cwebp" or operation == "vwebp":
        newfilename = f"{filename.rsplit('.', 1)[0]}.webp"
        cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], newfilename), img)
    elif operation == "cjpg":
        newfilename = f"{filename.rsplit('.', 1)[0]}.jpeg"
        cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], newfilename), img)
    print(f"New file saved as {newfilename}")
    return newfilename

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newfilename = processImage(filename, operation)
            if newfilename:
                flash(f"Your image has been processed and it is available <a href='/static/{newfilename}' target='_blank'>here</a>")
            else:
                flash("Error processing the image.")
            return render_template("index.html")
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
