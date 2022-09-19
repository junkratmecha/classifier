from flask import Flask, request, redirect, url_for, render_template, Markup
from flask_bootstrap import Bootstrap

from logic.save_image import save_image
from logic.predict_image import predict_image

import note_seq
from note_seq.protobuf import music_pb2

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

@app.route("/rnn", methods=["GET", "POST"])
def rnn():
    if request.method == "GET":

        seed = music_pb2.NoteSequence()  # NoteSequence

        # notesにnoteを追加
        seed.notes.add(pitch=80, start_time=0.0, end_time=0.4, velocity=80)
        seed.notes.add(pitch=80, start_time=0.4, end_time=0.8, velocity=80)
        seed.notes.add(pitch=87, start_time=0.8, end_time=1.2, velocity=80)
        seed.notes.add(pitch=87, start_time=1.2, end_time=1.6, velocity=80)
        seed.notes.add(pitch=89, start_time=1.6, end_time=2.0, velocity=80)
        seed.notes.add(pitch=89, start_time=2.0, end_time=2.4, velocity=80)
        seed.notes.add(pitch=87, start_time=2.4, end_time=3.2, velocity=80)

        seed.total_time = 3.2  # 所要時間
        seed.tempos.add(qpm=75);  # 曲のテンポを指定

        graph = note_seq.plot_sequence(seed)  # NoteSequenceの可視化
        music = note_seq.play_sequence(seed, synth=note_seq.fluidsynth)  # NoteSequenceの再生
        
        return render_template("rnn.html", graph=graph, music=music)
    else:
        return redirect(url_for("index"))

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