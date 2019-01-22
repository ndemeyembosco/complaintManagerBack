import os 
from flask import request, jsonify 
from app import app, mongo, flask_bcrypt, jwt  
from app.schemas import validate_user 
import logger 
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/user/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def user_with_id(id):
    if request.method == 'GET':
        data = mongo.db.users.find() 
        data_list = list(data)
        user_data = data_list[id]
        return jsonify(user_data), 200
    data = list(mongo.db.users.find())[id]

    if request.method == 'DELETE': 
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email' : data['email']})
            if db_response.deleted_count == 1:
                response = {'ok' : True, 'message' : 'record delete'}
            else:
                response = {'ok' : True, 'message': 'no record found'}
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400 


    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})}
            )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else: 
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        query = request.args 
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    data = request.get_json()

    if request.method == 'DELETE': 
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email' : data['email']})
            if db_response.deleted_count == 1:
                response = {'ok' : True, 'message' : 'record delete'}
            else:
                response = {'ok' : True, 'message': 'no record found'}
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400 


    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})}
            )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else: 
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400



@app.route('/register', methods=['POST'])
def register():
    ''' register user account '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        #mongo.db.users.createIndex({user_id : 1})
        mongo.db.users.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters : {}'.format(data['message'])}), 400



@app.route('/auth', methods=['POST'])
def auth_user():
    """ authentication endpoint """
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {'_id': 0}) # not sure why the 0
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token 
            user['refresh'] = refresh_token 
            return jsonify({'ok': True, 'data': user}), 200 
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400 


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token' : create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok' : False,
        'message' : 'Missing Authorization Header'
    }), 401