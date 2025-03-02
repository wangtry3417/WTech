from flask import Blueprint, request, redirect, url_for, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename

wcloud_bp = Blueprint('wcloud_bp', __name__, template_folder='templates/wcloud')

# 設定檔案上傳目錄
UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'js'} # 允許上傳的檔案類型
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # 確保目錄存在

# 簡易使用者帳號密碼 (請替換成更安全的驗證方式在實際應用中)
USERS = {'wtech': 'Abcd1234!'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@wcloud_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if USERS.get(request.form['username']) == request.form['password']:
            return redirect(url_for('wcloud_bp.wcloud')) # 登入成功後導向 /wcloud
        error = 'Invalid credentials'
    return render_template('wcloud/login.html', error=error)

@wcloud_bp.route('/') # 根路由設定為 /wcloud
@login_required
def wcloud():
    return render_template('wcloud/wcloud.html') # 顯示雲端服務首頁

@wcloud_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # 確保檔案名稱安全
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('wcloud_bp.wcloud')) # 上傳成功後重新導向 /wcloud 首頁
    return 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'

@wcloud_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@wcloud_bp.route('/files')
@login_required
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return redirect("/wcloud")

if __name__ == '__main__':
    app.run(debug=True) # 開啟 debug 模式方便開發，部署時需關閉