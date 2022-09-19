import os
import shutil
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./static/images/"

def  save_image(file):
  if os.path.isdir(UPLOAD_FOLDER):
      shutil.rmtree(UPLOAD_FOLDER)
  os.mkdir(UPLOAD_FOLDER)
  filename = secure_filename(file.filename)  # ファイル名を安全なものに
  filepath = os.path.join(UPLOAD_FOLDER, filename)
  file.save(filepath)
  return filepath