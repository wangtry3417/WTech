"""WTech - Database Models & Admin View Classes"""

from extensions import db
from flask_login import UserMixin, current_user
from markupsafe import Markup
import pandas as pd
from flask import jsonify, redirect, Response, request
from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, BooleanField, SelectField, FloatField, IntegerField
from sqlalchemy import text
import psycopg2
import paypalrestsdk

# ═══════════════════════════════════════════════
# 1. DB Models
# ═══════════════════════════════════════════════

class wbankwallet(db.Model, UserMixin):
    __tablename__ = 'wbankwallet'
    username = db.Column(db.String(64), primary_key=True, nullable=False)
    balance = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    verify = db.Column(db.String(64), nullable=False, default='no')
    sub = db.Column(db.String(64), nullable=True)
    accnumber = db.Column(db.String(60), nullable=True)
    openpay = db.Column(db.Boolean, nullable=True, default=False)
    role = db.Column(db.String(60), nullable=False, default='NonVerify')
    setamount = db.Column(db.Integer, nullable=False, default=20000)
    nowamount = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(70), nullable=True)
    mfa_key = db.Column(db.String(120), nullable=True)

    def __init__(self, username, balance, password, verify, sub, accnumber,
                 openpay, role, setamount, nowamount, email):
        self.username = username
        self.balance = balance
        self.password = password
        self.verify = verify
        self.sub = sub
        self.accnumber = accnumber
        self.openpay = openpay
        self.role = role
        self.setamount = setamount
        self.nowamount = nowamount
        self.email = email

    def get_id(self):
        return self.username


class wbankrecord(db.Model):
    __tablename__ = 'wbankrecord'
    username = db.Column(db.String(64), primary_key=True, nullable=False)
    action = db.Column(db.String(120), nullable=True)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, action, time):
        self.username = username
        self.action = action
        self.time = time


class oauth_client(db.Model):
    __tablename__ = 'clients'
    clientID = db.Column(db.String(120), nullable=False, primary_key=True)
    clientSecret = db.Column(db.String(120), nullable=False)
    scrope = db.Column(db.String(64), nullable=False)

    def __init__(self, clientID, clientSecret, scrope):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.scrope = scrope


class wbankkyc(db.Model):
    __tablename__ = 'wbankkyc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(120), nullable=False)
    id_number = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    career = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(64), db.ForeignKey('wbankwallet.username'), nullable=False)
    pp_image = db.Column(db.Text, nullable=True)


class wbankauthpay(db.Model):
    __tablename__ = 'wbankauthpay'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payer = db.Column(db.String(64), db.ForeignKey('wbankwallet.username'), nullable=False)
    reviewer = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, payer, reviewer, amount):
        self.payer = payer
        self.reviewer = reviewer
        self.amount = amount


class cashout(db.Model):
    __tablename__ = 'cashout'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='待處理Pending')


# ═══════════════════════════════════════════════
# 2. Form Classes
# ═══════════════════════════════════════════════

class IDBrandForm(BaseForm):
    username = StringField('用戶名', validators=[DataRequired()])
    balance = StringField('餘額', validators=[DataRequired()])
    password = StringField('密碼', validators=[DataRequired()])
    verify = StringField('驗證狀態', validators=[DataRequired()])
    sub = SelectField('備註', choices=[], validators=[])
    role = StringField('目前身分', validators=[DataRequired()])
    openpay = BooleanField('是否開啟Pay mode')
    nowamount = IntegerField("總共轉帳金額", validators=[NumberRange(min=0)])
    email = StringField('電郵')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub.choices = self.get_dynamic_choices()

    def get_dynamic_choices(self):
        return [
            ('', ''),
            ('由於閣下的資料存在問題，因此將會被暫時凍結', '資料問題凍結'),
            ('由於閣下的帳戶存在洗錢，因此將被暫時凍結', '使錢凍結'),
            ('可能存在不明原因，建議尋找WBank分行解決此問題', '不明原因凍結')
        ]


class cashForm(BaseForm):
    name = StringField('用戶名稱', validators=[DataRequired()])
    amount = FloatField('金額(WTC$)', validators=[DataRequired()])
    status = SelectField('狀態', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status.choices = self.get_dynamic_choices()

    def get_dynamic_choices(self):
        return [("待處理Pending", "Pending"), ("成功", "Done"), ("失敗", "Fail")]


# ═══════════════════════════════════════════════
# 3. Admin View Classes
# ═══════════════════════════════════════════════

class WBankRecordView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/wbankrecord.html')

    @expose('/execute_query', methods=['POST'])
    def execute_query(self):
        user = request.form.get('username')
        query = text("SELECT * FROM wbankrecord WHERE username=:username ORDER BY time DESC")
        res = db.session.execute(query, {'username': user})
        records = res.fetchall()
        result = [{'username': r[0], 'action': r[1], 'time': str(r[2])} for r in records]
        return jsonify(result)

    @expose('/export', methods=['GET'])
    def export_data(self):
        query = text("SELECT * FROM wbankrecord")
        res = db.session.execute(query)
        records = res.fetchall()
        df = pd.DataFrame(records, columns=['username', 'action', 'time'])
        csv = df.to_csv(index=False)
        return Response(csv, mimetype='text/csv',
                        headers={"Content-disposition": "attachment; filename=wbankrecord.csv"})


class walletView(ModelView):
    column_display_pk = True
    column_searchable_list = ('username', 'sub')
    column_labels = {
        'username': '用戶名',
        'balance': '餘額',
        'password': '密碼',
        'verify': '驗證狀態',
        'sub': '備註',
        'openpay': '是否開啟Pay mode',
        'setamount': '設置交易限額',
        'nowamount': '目前交易額'
    }
    edit_modal = True
    form = IDBrandForm

    def is_accessible(self):
        return (current_user.is_active and current_user.is_authenticated
                and (current_user.role == "staff" or current_user.role == "admin"))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                return jsonify({"msg": "非管理人員不能訪問"})
            else:
                return redirect("/wbank")


class kycView(ModelView):
    column_list = ('username', 'fname', 'id_number', 'address', 'career', 'pp_image')
    column_searchable_list = ('fname', 'id_number')
    form_args = {
        'username': {'validators': [DataRequired()]},
        'fname': {'validators': [DataRequired()]},
        'id_number': {'validators': [DataRequired()]},
        'address': {'validators': [DataRequired()]},
        'career': {'validators': [DataRequired()]},
        'pp_image': {'validators': []}
    }
    column_display_pk = True
    edit_modal = True
    column_labels = {
        'username': '用戶名或帳戶號碼',
        'fname': '全名',
        'id_number': '護照號碼',
        'address': '地址',
        'career': '職業',
        'pp_image': '護照b64Code'
    }
    column_formatters = {
        'pp_image': lambda view, ctx, model, name: (
            Markup(f"<img src={model.pp_image} style='width: 50px; height: 50px;' />")
            if model.pp_image else "沒有護照圖片或翻譯失敗"
        )
    }

    def is_accessible(self):
        return (current_user.is_active and current_user.is_authenticated
                and current_user.role == "admin")

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                return jsonify({"msg": "Only authenticated user can use"})
            else:
                return redirect("/wbank")


class cashView(ModelView):
    column_display_pk = True
    column_searchable_list = ('id', 'name', 'status')
    column_labels = {
        'id': '序號',
        'name': '用戶名稱',
        'amount': '金額(WTC$)',
        'status': '狀態'
    }
    edit_modal = True
    form = cashForm

    def is_accessible(self):
        return (current_user.is_active and current_user.is_authenticated
                and (current_user.role == "staff" or current_user.role == "admin"))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                return jsonify({"msg": "非管理人員不能訪問"})
            else:
                return redirect("/wbank")


# ═══════════════════════════════════════════════
# 4. External DB Connection (legacy psycopg2)
# ═══════════════════════════════════════════════

# Legacy psycopg2 connection (used by some socketio handlers)
try:
    conn = psycopg2.connect(
        database="neondb", user="neondb_owner",
        password="npg_KP2Zat1YscBz",
        host="ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech",
        port=5432, sslmode="require"
    )
except Exception as _conn_err:
    print(f'[WARN] Legacy psycopg2 conn failed: {_conn_err}')
    conn = None

# ═══════════════════════════════════════════════
# 5. PayPal SDK 設定 (live)
# ═══════════════════════════════════════════════

paypalrestsdk.configure({
    'mode': 'live',
    'client_id': 'AZsh7JUNnTOO2eYLuwhfwMltWUUCcDS--qf2TzNVDCvlDK20lhbUrbRXYfZgfJEaDskmPi5nmssIQWme',
    'client_secret': 'ELlPg1idvYkNyzL1nBip5r2qL-fLBhHUpuz_aFQUD6OC7D1AlYj7qxPislk8_0igdkcp0afgPw2O5K0a'
})