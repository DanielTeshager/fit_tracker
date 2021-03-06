import os
from flask import Flask, request, jsonify, abort, redirect, session, render_template, url_for
from sqlalchemy import exc
import json
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from database.models import setup_db, User, Body_Measurement, db
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.secret_key = 'super secret key'
setup_db(app)
CORS(app)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='10aH57S9A0QVZyoQqyX0FqIcFif9Sn1Q',
    client_secret='vHCb6SSYnBUnZ46YOtv0iwyKIx3dU0VTQiJ9xKSYiI1adztZWqiC9tqxIDY8fhDJ',
    api_base_url='https://dev-ht91p085.us.auth0.com',
    access_token_url='https://dev-ht91p085.us.auth0.com' + '/oauth/token',
    authorize_url='https://dev-ht91p085.us.auth0.com' + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


# ROUTES
@app.route('/')
def login():
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True),
        audience='protones')


@app.route("/callback")
def callback():
    # Handles response from token endpoint
    return jsonify(auth0.authorize_access_token())


'''
    GET /users
        it should be a public endpoint
    returns status code 200 and json {"success": True, "users": users} 
        or appropriate status code indicating reason for failure
'''


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    try:
        return jsonify({
            'success': True,
            'users': [user.format()['nick_name'] for user in users]
        }), 200
    except:
        abort(422)


'''
    GET /body_measurements
        it should be a public endpoint
    returns status code 200 and json {"success": True, "body_measurements": body_measurements}
        or appropriate status code indicating reason for failure
'''


@app.route('/body_measurements', methods=['GET'])
def get_body_measurements():
    body_measurements = Body_Measurement.query.all()
    try:
        return jsonify({
            'success': True,
            'body_measurements': [body_measurement.format() for body_measurement in body_measurements]
        }), 200
    except:
        abort(422)


'''
GET /users-detail
    it should be a secure endpoint where only fitnesstracker admins can access it
    it should require the 'get:users-detail' permission
    it should return status code 200 and json {"success": True, "users": users}
        or appropriate status code indicating reason for failure
'''


@app.route('/users-detail', methods=['GET'])
@requires_auth('get:user-detail')
def get_users_detail():
    users = User.query.all()
    try:
        return jsonify({
            'success': True,
            'users': [user.format() for user in users]
        }), 200
    except:
        abort(422)


'''
    GET /user/body_measurements
        it should be a private endpoint
        it should require the 'get:body_measurements' permission
        it should return status code 200 and json {"success": True, "body_measurements": body_measurements}
'''


@app.route('/user/body_measurements', methods=['GET'])
@requires_auth('get:body_measurements')
def get_user_body_measurements(payload):
    user_id = payload['sub']
    body_measurements = Body_Measurement.query.filter_by(user_id=user_id).all()
    try:
        return jsonify({
            'success': True,
            'body_measurements': [body_measurement.format() for body_measurement in body_measurements]
        }), 200
    except:
        abort(422)


'''
    GET /user/body_measurements/<int:id>
        it should be a private endpoint
        it should require the 'get:body_measurements' permission
        it should return status code 200 and json {"success": True, "body_measurement": body_measurement}
            or appropriate status code indicating reason for failure
'''


@app.route('/user/body_measurements/<int:id>', methods=['GET'])
@requires_auth('get:body_measurements')
def get_user_body_measurement(payload, id):
    user_id = payload['sub']
    body_measurement = Body_Measurement.query.filter_by(
        user_id=user_id, id=id).first()
    try:
        return jsonify({
            'success': True,
            'body_measurement': body_measurement.format()
        }), 200
    except:
        abort(422)


'''
  DELETE /user/body_measurements/<int:id>
        it should be a private endpoint
        it should require the 'delete:body_measurements' permission

'''


@app.route('/user/body_measurements/<int:id>', methods=['DELETE'])
@requires_auth('delete:body_measurements')
def delete_user_body_measurement(payload, id):
    user_id = payload['sub']
    body_measurement = Body_Measurement.query.filter_by(
        user_id=user_id, id=id).first()
    try:
        body_measurement.delete()
        return jsonify({
            'success': True,
            'deleted': id
        }), 200
    except:
        abort(422)


'''
    PATH /body_measurements/<int:id>
        it should be a private endpoint
        it should require the 'patch:body_measurements' permission
'''


@app.route('/body_measurements/<int:id>', methods=['PATCH'])
@requires_auth('patch:body_measurements')
def update_user_body_measurement(payload, id):
    user_id = payload['sub']
    body_measurement = Body_Measurement.query.filter_by(
        user_id=user_id, id=id).first()
    body_measurement_data = request.get_json()
    if body_measurement_data is None:
        abort(422)
    if 'weight' in body_measurement_data:
        body_measurement.weight = body_measurement_data['weight']
    if 'height' in body_measurement_data:
        body_measurement.height = body_measurement_data['height']
    try:
        body_measurement.update()
        return jsonify({
            'success': True,
            'updated': id
        }), 200
    except:
        abort(422)


'''
    POST /users
        it should create a new user
        it should require the 'post:users' permission
        it should return status code 200 and json {"success": True, "users": user}
            or appropriate status code indicating reason for failure
'''


@app.route('/users', methods=['POST'])
@requires_auth('post:users')
def create_user(payload):
    user_data = request.get_json()
    print(user_data)
    if user_data is None:
        abort(422)
    if 'full_name' not in user_data:
        abort(422)
    if 'nick_name' not in user_data:
        abort(422)
    if 'age' not in user_data:
        abort(422)
    try:
        user = User(
            full_name=user_data['full_name'],
            nick_name=user_data['nick_name'],
            age=user_data['age']
        )
        user.insert()
        return jsonify({
            'success': True,
            'created': user.id
        }), 200
    except:
        abort(422)


@app.route('/users/body_measurements', methods=['POST'])
@requires_auth('post:body_measurements')
def create_user_body_measurement(payload):
    body_measurement_data = request.get_json()
    print(body_measurement_data)
    if body_measurement_data is None:
        abort(422)
    if 'weight' not in body_measurement_data:
        abort(422)
    print('b')
    if 'height' not in body_measurement_data:
        abort(422)
    print('c')
    if 'user_id' not in body_measurement_data:
        abort(422)
    print('d')
    try:
        body_measurement = Body_Measurement(
            user_id=body_measurement_data['user_id'],
            weight=body_measurement_data['weight'],
            height=body_measurement_data['height']
        )
        body_measurement.insert()
        return jsonify({
            'success': True,
            'created': body_measurement.id
        }), 200
    except:
        abort(422)


'''
  DELETE /user/<int:id>
        it should delete a user
        it should require the 'delete:users' permission
        it should return status code 200 and json {"success": True, "delete": id}
            or appropriate status code indicating reason for failure
'''


@app.route('/user/<int:id>', methods=['DELETE'])
@requires_auth('delete:users')
def delete_user(payload, id):
    user = User.query.filter_by(id=id).first()
    try:
        user.delete()
        return jsonify({
            'success': True,
            'deleted': id
        }), 200
    except:
        abort(422)


'''
Error Handling
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)
