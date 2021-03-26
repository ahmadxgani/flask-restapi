from app.model.plugin import Plugin
from flask import request, jsonify
from app import response, db, abort
from app.controller import UserController
from flask_jwt_extended import *

@jwt_required()
def index():
    try:
        id = request.args.get('user_id')
        if not id:
            abort(400)
        plugin = Plugin.query.filter_by(user_id=id).all()
        if not plugin:
            return response.respon(400, 'User tidak ditemukan!', None)
        data = transform(plugin)
        return response.respon(200, 'oke', data)
    except Exception as e:
        print(e)
        abort(400)


def store():
    try:
        fitur = request.json['fitur']
        user_id = request.json['user_id']

        plugin = Plugin(user_id=user_id, fitur=fitur)
        db.session.add(plugin)
        db.session.commit()

        return response.respon(200, 'Successfully create plugin!', None)

    except Exception as e:
        print(e)
        abort(400)

def update(id):
    try:
        fitur = request.json['fitur']

        plugin = Plugin.query.filter_by(id=id).first()
        plugin.fitur = fitur

        db.session.commit()

        return response.respon(200, 'Successfully update plugin!', None)

    except Exception as e:
        print(e)

def show(id):
    try:
        plugin = Plugin.query.filter_by(id=id).first()
        if not plugin:
            return response.respon(400, 'Empty....', None)

        data = singleTransform(plugin)
        return response.respon(200, 'oke', data)
    except Exception as e:
        print(e)


def delete(id):
    try:
        plugin = Plugin.query.filter_by(id=id).first()
        if not plugin:
            return response.respon(400, 'Empty....', None)

        db.session.delete(plugin)
        db.session.commit()

        return response.respon(200, 'Successfully delete data!', None)
    except Exception as e:
        print(e)


def transform(plugin):
    array = []
    for i in plugin:
        array.append(singleTransform(i))
    return array


def singleTransform(plugin):
    data = {
        'id': plugin.id,
        'fitur': plugin.fitur,
        'user_id': plugin.user_id,
        'created_at': plugin.created_at,
        'user': UserController.singleTransform(plugin.user, withPlugin=False)
    }

    return data