from app import app, p_scraper, request, abort, render_template
from app.controller import UserController, PluginController
from app import response
from flask_jwt_extended import *

@app.route('/')
def index():
    return abort(500)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return UserController.index()
    else:
        return UserController.store()

@app.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def userDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)

@app.route('/plugin', methods=['POST', 'GET'])
def plugin():
    if request.method == 'GET':
        return PluginController.index()
    else:
        return PluginController.store()

@app.route('/plugin/<id>', methods=['PUT', 'GET', 'DELETE'])
def pluginDetail(id):
    if request.method == 'GET':
        return PluginController.show(id)
    elif request.method == 'PUT':
        return PluginController.update(id)
    elif request.method == 'DELETE':
        return PluginController.delete(id)

@app.route('/login', methods=['POST'])
def login():
    return UserController.login()

@app.route('/refresh', methods=['POST'])
def refresh():
    return UserController.refresh()

@jwt_required()
@app.route('/pinterest/<key>')
def pinterest(key):
    try:
        if not key:
            abort(400)
        is_success = p_scraper.make_ready(key)
        if is_success:
            return response.respon(200, 'Berhasil', is_success)
        else:
            abort(404)
    except:
        abort(500)
