from app import app, jsonify, make_response

def respon(code, msg, data):
    return (
        make_response(jsonify({
            'code': code,
            'message': msg,
            'data': data
        }), code)
    )

@app.errorhandler(400)
def bad_request(e):
    return respon(400, 'Parameter anda kurang..', None)

@app.errorhandler(404)
def not_found(e):
    return respon(404,'URL anda salah!', None)

@app.errorhandler(405)
def method_not_allowed(e):
    return respon(405,'Dame desu yo!', None)

@app.errorhandler(500)
def internal_server_error(e):
    return respon(500,'Mohon maaf, ada gangguan pada server kami.', None)