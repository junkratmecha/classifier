def imagejudge():
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
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)  # ファイル名を安全なものに
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 画像の読み込み
        image = Image.open(filepath)
        image = image.convert("RGB")
        image = image.resize((img_size, img_size))

        normalize = transforms.Normalize(
            (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))  # 平均値を0、標準偏差を1に
        to_tensor = transforms.ToTensor()
        transform = transforms.Compose([to_tensor, normalize])

        x = transform(image)
        x = x.reshape(1, 3, img_size, img_size)

        # 予測
        net = Net()
        net.load_state_dict(torch.load(
            "model_cnn.pth", map_location=torch.device("cpu")))
        net.eval()  # 評価モード

        y = net(x)
        y = F.softmax(y, dim=1)[0]
        sorted_idx = torch.argsort(-y)  # 降順でソート
        result = ""
        for i in range(n_result):
            idx = sorted_idx[i].item()
            ratio = y[idx].item()
            label = labels[idx]
            result += "<p>" + str(round(ratio*100, 1)) + \
                "%の確率で" + label + "です。</p>"
        return render_template("result.html", result=Markup(result), filepath=filepath)
    else:
        return redirect(url_for("index"))