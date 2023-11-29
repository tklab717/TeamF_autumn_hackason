from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re
from models import dbConnect
from flask_mail import Mail, Message
from util.SSM import SSM

app = Flask(__name__)

# クラウド環境の場合のみFlaskメールを使用する
try:
    #EC2でSSMに接続し、REGION情報を入手できるかでクラウド環境かを判断
    REGION_now = SSM.get_parameters('RDS-REGION')
    #flask-mailでsmtpサーバに接続するために必要なパラメータをセット
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587                             # TLSは587、SSLなら465
    app.config['MAIL_USERNAME'] = SSM.get_parameters('FLASKMAIL-USER')
    app.config['MAIL_PASSWORD'] = SSM.get_parameters('FLASKMAIL-PASS')  # GmailのApp用のmパスワード設定をしておく必要あり
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] =  SSM.get_parameters('FLASKMAIL-USER')    # これがあるとsender設定が不要になる
    mail = Mail(app)
    #flask-mailを使う場合はフラグを立てる
    f_fmail=1
except:
    #flask-mailを使わない場合はフラグを落とす
    f_fmail=0

#cookieを暗号化する秘密鍵を設定(ランダムなuuid(重複しないID）を作成しセット)
app.secret_key = uuid.uuid4().hex
#セッションがアクティブでなくてもセッション情報を保持する期間
app.permanent_session_lifetime = timedelta(days=30)


# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/mypage')
    return redirect('/signup')

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/mypage')
    return redirect('/login')


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

# チーム情報の受け渡し・登録
@app.route('/teamSelectProcess', methods=['POST'])
def teamSelectProcess():
    # uidはセッションで受け渡し
    uid = session.get("uid")
    # フォームからデータを取得
    year = request.form['year']
    season = request.form['season']
    team = request.form['team']
    github = request.form['github']

    # ここでデータを処理（例：セッションに保存、データベースに保存など）
    DBteamList = dbConnect.getteamList(uid, year, season, team, github)
    if year == '' or season == '' or team == '' or github == '':
        flash('からのフォームがあるようです')
    # チーム登録済みの場合は登録しない。全てのパラメータが同じ場合。
    elif DBteamList != None:
        flash('既に登録されているようです')
        session['year'] = year
        session['season'] = season
        session['team'] = team
        session['github'] = github
        return redirect('/') 
        

    else: 
        dbConnect.createteamLists(uid, year, season, team, github) 
        Year = (year) 
        Season = (season) 
        Team = (team) 
        Github = (github) 
        session['year'] = Year
        session['season'] = Season
        session['team'] = Team
        session['github'] = Github
        return redirect('/')
    return redirect('/login')  


# 各チームのチャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    year = session.get("year")
    season = session.get("season")
    team = session.get("team")
    github = session.get("github")

    if uid is None:
        return redirect('/login')
    else:
        #セッションid,year,season,team,githubからチームチャネルを取得する
        channels = dbConnect.selectTeam(uid, year, season, team, github)
        #該当するチャネルが存在しない場合は空の情報を作成
        if channels == ():
            channels =[{'id':'', 'uid': '', 'name': '', '': ''}]

    return render_template('index.html', channels=channels, uid=uid, github=github)


# flaskメールを押した場合にメールを送る
@app.route("/send_mail")
def send_mail():
    if f_fmail==1:
        uid = session.get("uid")
        year = session.get("year")
        season = session.get("season")
        team = session.get("team")
        github = session.get("github")
        name=dbConnect.getUserName(uid)
        mails=dbConnect.getEmailGather(uid, year, season, team, github)
        msg = Message(name['user_name']+'さんからの集まれコール',sender = 'admin@oasis.blog', recipients=mails)

        msg.html = '<p><font size="3.5"><strong>オアシスで待っていますo( 〃゜▽ﾟ〃)ゝｵｫｰｲ!!</strong></font></p>\n' \
                    '<img src="cid:Myimage">\n'\
                    '<p><font size="6"><strong>https://oasishub.blog/</strong></font></p>\n'


        with app.open_resource("static/img/icon1.png") as fp:
            msg.attach("icon1.png", 'static/img', fp.read(), 'inline', headers=[['Content-ID', '<Myimage>']])
        mail.send(msg)

    else:
        flash('ローカル環境では機能は使えません')
    return redirect('/')

# チャンネルの追加
@app.route('/', methods=['POST'])
def add_channel():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    channel_name = request.form.get('channelTitle')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        dbConnect.addChannel(uid, channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)


# チャンネルの更新
@app.route('/update_channel', methods=['POST'])
def update_channel():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = request.form.get('cid')
    channel_name = request.form.get('channelTitle')
    channel_description = request.form.get('channelDescription')

    dbConnect.updateChannel(uid, channel_name, channel_description, cid)
    return redirect('/detail/{cid}'.format(cid = cid))


# チャンネルの削除
@app.route('/delete/<cid>')
def delete_channel(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(cid)
        if channel["uid"] != uid:
            flash('チャンネルは作成者のみ削除可能です')
            return redirect ('/')
        else:
            dbConnect.deleteChannel(cid)
            channels = dbConnect.getChannelAll()
            return redirect('/')


# チャンネル詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)

    return render_template('detail.html', messages=messages, channel=channel, uid=uid)


# メッセージの投稿
@app.route('/message', methods=['POST'])
def add_message():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    message = request.form.get('message')
    cid = request.form.get('cid')

    if message:
        dbConnect.createMessage(uid, cid, message)

    return redirect('/detail/{cid}'.format(cid = cid))


# メッセージの削除
@app.route('/delete_message', methods=['POST'])
def delete_message():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    message_id = request.form.get('message_id')
    cid = request.form.get('cid')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect('/detail/{cid}'.format(cid = cid))


@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'),404


@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
