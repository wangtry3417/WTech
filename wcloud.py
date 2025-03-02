from flask import Blueprint, request, redirect, url_for, send_from_directory, render_template, session, jsonify
import os
from werkzeug.utils import secure_filename
from hashlib import sha256

wcloud_bp = Blueprint('wcloud_bp', __name__, template_folder='templates/wcloud')

# 設定檔案上傳目錄
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'js'} # 允許上傳的檔案類型
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # 確保目錄存在

# 簡易使用者帳號密碼 (請替換成更安全的驗證方式在實際應用中)
USERS = {
  "allowUser":{
    "wtechProduct11202":sha256("Asd1230329299".encode("utf-8")).hexdigest(),
    "wtechProduct10292":sha256("Asiiw1088288".encode("utf-8")).hexdigest()
  }
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'wcloudUSERNAME' not in session or session['wcloudUSERNAME'] is None:
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
      files = os.listdir(session["userUploadFolder"])
      return render_template('wcloud/wcloud.html', files=files, username=username) # 顯示雲端服務首頁
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
          filename = secure_filename(file.filename) # 確保檔案名稱安全
          file.save(os.path.join(session["userUploadFolder"], filename))
          return redirect(url_for('wcloud_bp.wcloud')) # 上傳成功後重新導向 /wcloud 首頁
        return redirect("/wcloud/login")
    return 'Allowed file types are txt, pdf, png, jpg, jpeg, gif, py, js'

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
            return redirect(url_for('wcloud_bp.wcloud'))  # 刪除成功後重新導向
        return 'File not found', 404
    return redirect("/wcloud/login")

@wcloud_bp.route('/files')
@login_required
def list_files():
    if session["userUploadFolder"]:
      files = os.listdir(session["userUploadFolder"])
      return redirect("/wcloud")
    return redirect("/wcloud/login")