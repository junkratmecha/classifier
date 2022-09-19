from flask import Flask, request, redirect, url_for, render_template, Markup
from flask_bootstrap import Bootstrap

from logic.save_image import save_image
from logic.predict_image import predict_image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = "./static/images/"
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/cnn", methods=["GET", "POST"])
def cnn():
    return render_template("cnn.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        # ファイルの存在と形式を確認
        if "file" not in request.files:
            print("File doesn't exist!")
            return redirect(url_for("index"))
        file = request.files["file"]
        if not allowed_file(file.filename):
            print(file.filename + ": File not allowed!")
            return redirect(url_for("index"))
        # ファイルの保存
        filepath = save_image(file)
        # # 画像の読み込みと予測
        result = predict_image(filepath)

        return render_template("result.html", result=Markup(result), filepath=filepath)
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS