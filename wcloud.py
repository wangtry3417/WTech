from flask import Blueprint, request, redirect, url_for, send_from_directory, render_template, session, jsonify, g
import os
from werkzeug.utils import secure_filename
from hashlib import sha256

wcloud_bp = Blueprint('wcloud_bp', __name__, template_folder='templates/wcloud')

# 設定檔案上傳目錄
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'js', '.zip', 'tar.gz'} # 允許上傳的檔案類型
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # 確保目錄存在

# 簡易使用者帳號密碼 (請替換成更安全的驗證方式在實際應用中)
USERS = {
  "allowUser":{
    "wtechProduct11202":sha256("Asd1230329299".encode("utf-8")).hexdigest(),
    "wtechProduct10292":sha256("Asiiw1088288".encode("utf-8")).hexdigest(),
    "wtechProduct09819":sha256("Asdoehsj101099".encode("utf-8")).hexdigest()
  }
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'wcloudUSERNAME' not in session or session['wcloudUSERNAME'] is None and session['uploadTimes'] is None:
            return redirect("/wcloud/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@wcloud_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if USERS["allowUser"].get(request.form['username']) == request.form['password']:
            session["wcloudUSERNAME"] = request.form['username']
            user_upload_folder = os.path.join(UPLOAD_FOLDER, session["wcloudUSERNAME"])
            session["userUploadFolder"] = user_upload_folder
            session['uploadTimes'] = ["Ok",0]
            if session["wcloudUSERNAME"] == "wtechProduct11202":
              session['uploadTimes'] = ["wtechProduct11202",20]
            elif session["wcloudUSERNAME"] == "wtechProduct10292":
              session['uploadTimes'] = ["wtechProduct10292",5]
            elif session["wcloudUSERNAME"] == "wtechProduct09819":
              session['uploadTimes'] = ["wtechProduct09819",10]
            # 如果需要，可以在這裡創建該文件夾
            if not os.path.exists(user_upload_folder):
                os.makedirs(user_upload_folder)
            return redirect("/wcloud") # 登入成功後導向 /wcloud
        error = 'Invalid credentials'
    return render_template('wcloud/login.html', error=error)

@wcloud_bp.route('/') # 根路由設定為 /wcloud
@login_required
def wcloud():
    username = session["wcloudUSERNAME"]
    if session["userUploadFolder"]:
      count = int(session['uploadTimes'][1])
      files = os.listdir(session["userUploadFolder"])
      return render_template('wcloud/wcloud.html', files=files, username=username, count=count) # 顯示雲端服務首頁
    return redirect("/wcloud/login")

@wcloud_bp.route("/getkey")
def wcloud_getKey():
  pid = request.args.get("pid")
  if pid:
    return jsonify(code=USERS["allowUser"].get(pid))
  return "Key not found", 400

@wcloud_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        if session["userUploadFolder"]:
          if not os.path.exists(session["userUploadFolder"]):
            os.makedirs(session["userUploadFolder"])
          if int(session['uploadTimes'][1]) == 0:
            return redirect("/wcloud")
          session['uploadTimes'][1] = int(session['uploadTimes'][1]) - 1
          filename = secure_filename(file.filename) # 確保檔案名稱安全
          file.save(os.path.join(session["userUploadFolder"], filename))
          return redirect(url_for('wcloud_bp.wcloud')) # 上傳成功後重新導向 /wcloud 首頁
        return redirect("/wcloud/login")
    return 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, py, js, zip, tar.gz'

@wcloud_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    if session["userUploadFolder"]:
      return send_from_directory(session["userUploadFolder"], filename)
    return redirect("/wcloud/login")

@wcloud_bp.route('/rename', methods=['POST'])
@login_required
def rename_file():
    old_filename = request.form['old_filename']
    new_filename = request.form['new_filename']
    
    if session["userUploadFolder"]:
        old_file_path = os.path.join(session["userUploadFolder"], old_filename)
        new_file_path = os.path.join(session["userUploadFolder"], secure_filename(new_filename))
        
        # 檢查舊檔案是否存在且是檔案
        if os.path.isfile(old_file_path):
            # 檢查新檔案名稱是否已存在
            if not os.path.exists(new_file_path):
                os.rename(old_file_path, new_file_path)
                return redirect(url_for('wcloud_bp.wcloud'))  # 重命名成功後重新導向
            return 'New filename already exists', 400
        return 'File not found or is a directory', 404
    return redirect("/wcloud/login")

@wcloud_bp.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    if session["userUploadFolder"]:
        file_path = os.path.join(session["userUploadFolder"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            if session["wcloudUSERNAME"] == "wtechProduct11202":
              if int(session['uploadTimes'][1]) == 20:
                pass
              session['uploadTimes'] = int(session['uploadTimes'][1]) + 1
            elif session["wcloudUSERNAME"] == "wtechProduct10292":
              if int(session['uploadTimes']) == 5:
                pass
              session['uploadTimes'][1] = int(session['uploadTimes'][1]) + 1
            elif session["wcloudUSERNAME"] == "wtechProduct09819":
              if int(session['uploadTimes']) == 10:
                pass
              session['uploadTimes'] = int(session['uploadTimes'][1]) + 1
            return redirect(url_for('wcloud_bp.wcloud'))  # 刪除成功後重新導向
        return 'File not found', 404
    return redirect("/wcloud/login")

@wcloud_bp.route('/run_file', methods=['POST'])
def run_file():
    data = request.get_json()
    filename = data['filename']
    language = data['language']

    output = ''
    try:
        if language == 'python':
            # 使用 os.system 執行 Python 檔案並將輸出重定向到 output.txt
            os.system(f'python {filename} > output.txt 2>&1')
            with open('output.txt', 'r') as f:
                output = f.read()
        # 可根據需要添加其他語言的執行邏輯
    except Exception as e:
        output = str(e)

    return jsonify({'output': output})

@wcloud_bp.route('/run_cmds', methods=['POST'])
def run_cmds():
    data = request.get_json()
    c = data['command']

    output = ''
    try:
      os.system(f'{c} > output.txt 2>&1')
      with open('output.txt', 'r') as f:
        output = f.read()
    except Exception as e:
        output = str(e)

    return jsonify({'output': output})

@wcloud_bp.route('/files')
@login_required
def list_files():
    if session["userUploadFolder"]:
      files = os.listdir(session["userUploadFolder"])
      return redirect("/wcloud")
    return redirect("/wcloud/login")