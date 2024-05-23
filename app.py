from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3
import logging

app = Flask(__name__)

# 設定 logging
logging.basicConfig(filename='error.log', level=logging.ERROR)
# 資料庫預設名稱
dbname = 'mydb.db'


def Db_Search(userid, password):
    #連線資料庫驗證帳號密碼
    try:
        global dbname
        conn = sqlite3.connect(dbname)
        conn.row_factory = sqlite3.Row  # 設置 row_factory
        cursor = conn.cursor()  # 建立 cursor 物件
        cursor.execute(f'SELECT * FROM member WHERE idno=? AND pwd=?', (str(userid), str(password)))
        user = cursor.fetchone()  # 讀取資料
        return user
    except Exception as e:
        logging.error(e)  # 記錄錯誤
        return None
    finally:
        cursor.close()  # 關閉 cursor 物件
        conn.close()  # 關閉資料庫連線

@app.route('/')
def index():
    iid = request.cookies.get('iid')
    nm = request.cookies.get('nm')
    birth = request.cookies.get('birth')
    blood = request.cookies.get('blood')
    phone = request.cookies.get('phone')
    email = request.cookies.get('email')
    idno = request.cookies.get('idno')
    pwd = request.cookies.get('pwd')
    if iid:
        return render_template('index.html', userid=iid ,nm=nm, birth=birth, blood=blood, phone=phone, email=email, idno=idno, pwd=pwd)
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['idnumber']  # 身分證
        password = request.form['password']  # 密碼
        user = Db_Search(userid, password)  #查詢是否有資料
        if user:
            response = make_response(redirect(url_for('index')))
            response.set_cookie('iid', str(user['iid']))  # 儲存id
            response.set_cookie('nm', str(user['nm']))  # 儲存名字
            response.set_cookie('birth', str(user['birth']))  # 儲存生日
            response.set_cookie('blood', str(user['blood']))  # 儲存血型
            response.set_cookie('phone', str(user['phone']))  # 儲存手機號碼
            response.set_cookie('email', str(user['email']))  # 儲存email
            response.set_cookie('idno', str(user['idno']))  # 儲存身分證
            response.set_cookie('pwd', str(user['pwd']))  # 儲存密碼
            return response
        else:
            return render_template('login.html', error="請輸入正確的帳號密碼")
    else:
        return render_template('login.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':

        iid= request.cookies.get('iid')
        nm =request.form['nm']
        birth =request.form['birth']
        blood =request.form['blood']
        phone =request.form['phone']
        email =request.form['email']
        idno =request.form['idno']
        pwd =request.form['pwd']
        # 連線至資料庫
        global dbname
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("UPDATE member SET nm=?,birth=?,blood=?,phone=?,email=?,idno=?,pwd=? WHERE iid=?", (nm, birth, blood, phone, email, idno, pwd, iid))
        conn.commit()
        conn.close()

        #變更Cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie('iid', iid)  # 儲存id
        response.set_cookie('nm', nm)  # 儲存名字
        response.set_cookie('birth', birth)  # 儲存生日
        response.set_cookie('blood', blood)  # 儲存血型
        response.set_cookie('phone', phone)  # 儲存手機號碼
        response.set_cookie('email', email)  # 儲存email
        response.set_cookie('idno', idno)  # 儲存身分證
        response.set_cookie('pwd', pwd)  # 儲存密碼
        return response
    else:
        nm = request.cookies.get('nm')
        birth = request.cookies.get('birth')
        blood = request.cookies.get('blood')
        phone = request.cookies.get('phone')
        email = request.cookies.get('email')
        idno = request.cookies.get('idno')
        pwd = request.cookies.get('pwd')
        return render_template('edit.html', nm=nm, birth=birth, blood=blood, phone=phone, email=email, idno=idno, pwd=pwd)

@app.errorhandler(Exception)
def Error_handler(error):
    logging.exception("An error occurred: ") # 寫入詳細錯誤訊息到日誌
    return render_template('error.html') # 轉向錯誤頁面


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('iid', '', expires=0)  # 刪除Cookies
    response.set_cookie('nm', '')  # 儲存名字
    response.set_cookie('birth', '')  # 儲存生日
    response.set_cookie('blood', '')  # 儲存血型
    response.set_cookie('phone', '')  # 儲存手機號碼
    response.set_cookie('email', '')  # 儲存email
    response.set_cookie('idno', '')  # 儲存身分證
    response.set_cookie('pwd', '')  # 儲存密碼
    return response
