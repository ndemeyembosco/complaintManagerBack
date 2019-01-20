import os
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import app, mongo
from app.schemas import validate_complaint, validate_complaint_update
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/complaint', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def complaint():
    ''' route read complaints'''
    if request.method == 'GET':
        query = request.args
        data  = mongo.db.tasks.find_one({'__id': ObjectId(query['id'])})
        return jsonify({'ok': True, 'data': data}), 200


    data = request.get_json()

    if request.method == 'POST':
        user = get_jwt_identity()
        data['email'] = user['email']  # change to use id instead of email
        data = validate_complaint(data)
        if data['ok'] :
            db_response = mongo.db.complaints.insert_one(data['data'])
            return_data = mongo.db.complaints.find_one({'_id' : db_response.insert_id})
            return jsonify({'ok': True, 'data': return_data}), 201
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    if request.method == 'DELETE':
        if data.get('id', None) is not None:
            db_response = mongo.db.complaints.delete_one({'_id': ObjectId(data['id'])})
            if db_response.delete_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        data = validate_complaint_update(data)
        if data['ok']:
            data = data['data']
            mongo.db.complaints.update_one(
                {'_id': ObjectId(data['id'])}, {'$set': data['payload']}
            )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/list/complaint/<int:user_id>', methods=['GET'])
def list_complaints(user_id):
    ''' route to get all complaints for a user '''
    user = {'id': user_id}
    if request.method == 'GET':
        query = request.args
        data  = mongo.db.complaints.find({'_id': ObjectId(user['id'])})
        if query.get('group', None):
            return_data = {}
            for complaint in data:
                try:
                    return_data[complaint['status']].append(complaint)
                except:
                    return_data[complaint['status']] = [complaint]
        else:
            return_data = list(data)
        return jsonify({'ok': True, 'data': return_data})