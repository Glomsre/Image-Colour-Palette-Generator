from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
import os
from PIL import Image

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    file = 'static/myphoto.png'
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)

    return render_template("index.html")


@app.route('/upload_file', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        path_image = request.form.get('my_image')
        image = Image.open(path_image)
        image.save('static/myphoto.png')

        return redirect('/show_color_image')
    return render_template("index.html")


@app.route('/show_color_image', methods=["GET", "POST"])
def show_color_image():
    img = Image.open("static/myphoto.png")
    img = img.convert("RGB")

    d = img.getdata()
    color_counter = {}

    for item in d:
        if item in color_counter:
            color_counter[item] += 1
        else:
            color_counter[item] = 1

    common_color = sorted(color_counter, key=color_counter.get, reverse=True)
    top_10 = common_color[:10]
    image_saved = 'yes'

    return render_template("index.html", list_color=top_10, image_saved=image_saved)


@app.route('/restart')
def restart():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
