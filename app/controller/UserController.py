from app.model.user import User
from app import response, app, abort, request, db, render_template, mail
from flask_mail import Message
import datetime
from flask_jwt_extended import *

def index():
    try:
        users = User.query.all()
        data = transform(users)
        return response.respon(200, 'Berhasil', data)
    except Exception as e:
        print(e)
        return abort(500)

def show(id):
    try:
        users = User.query.filter_by(id=id).first()
        print(users)
        if not users:
            return response.respon(404, f'user dengan id {id} tidak ditemukan!', None)

        data = singleTransform(users)
        return response.respon(200, "Berhasil", data)
    except Exception as e:
        print(e)
        return abort(400)

def store():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        users = User(username=username, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()

        msg = Message("Hello, {} welcome to shinoa-api".format(username), sender="bindakun2nd@gmail.com")
        msg.add_recipient(email)
        msg.html = render_template('mail.html', app_name="shinoa-api", app_contact="bindakun2nd@gmail.com", name=username, email=email)
        mail.send(msg)

        return response.respon(200, 'Registrasi berhasil dilakukan, silahkan check email anda untuk mengaktifkan akun.', username)
    except Exception as e:
        print(e)
        return abort(400)

def update(id):
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.respon(400, f'user dengan id {id} tidak ditemukan!')
        user.email = email
        user.username = username
        user.setPassword(password)
        
        db.session.commit()
        return response.respon(200, 'Sukses update data!', username)
    except Exception as e:
        print(e)
        abort(400)

def delete(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.respon(400, f'user dengan id {id} tidak ditemukan!', False)
        db.session.delete(user)
        db.session.commit()
        return response.respon(200, 'Sukses delete data!', None)
    except Exception as e:
        print(e)
        abort(400)

def login():
    try:
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return response.respon(400, 'Email salah, user tidak terdaftar!', None)

        if not user.checkPassword(password):
            return response.respon(405, 'Password anda salah!', None)

        data = singleTransform(user)
        expires = datetime.timedelta(days=1, weeks=52)
        expires_refresh = datetime.timedelta(days=3, weeks=52)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.respon(200, 'Berhasil login', {
            "result": data,
            "token_access": access_token,
            "token_refresh": refresh_token
        })
    except Exception as e:
        print(e)
        abort(400)

@jwt_required(refresh=True)
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return response.respon(200, 'token baru berhasil digenerate!', new_token)
    except Exception as e:
        print(e)
        abort(400)

def singleTransform(users, withPlugin=True):
    data = {
        'id': users.id,
        'username': users.username,
        'email': users.email
    }

    if withPlugin:
        plugin = []
        for i in users.plugin:
            plugin.append({
                'id': i.id,
                'fitur': i.fitur
            })
        data['plugins'] = plugin

    return data

def transform(users):
    array = []
    for i in users:
        array.append(singleTransform(i))
    return array