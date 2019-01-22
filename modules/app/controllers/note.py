import os
from datetime import datetime 
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import app, mongo
from app.schemas import validate_note
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))



@app.route('/notes', methods=['GET', 'POST'])
def note():
    if request.method == 'GET':
        query = request.args 
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200
    data = request.get_json()

    if request.method == 'POST':
        data = validate_note(data)
        if data['ok'] :
                data = data['data']
                data['timestamp'] = str(datetime.today())
                insert_id = mongo.db.notes.insert_one(data)
                # print type(insert_id)
                return_data = mongo.db.notes.find_one({'_id' : insert_id.inserted_id})
                return jsonify({'ok': True, 'data': return_data}), 200
        else:
                return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
        

# @app.route('/note/<string:complaint_t>', methods=['GET'])
# def complaint_notes(complaint_t):
#     if request.method == 'GET':
#         my_data = {'complaint_title' : complaint_t }
#         data = mongo.db.notes.find({'complaint_title' : my_data['complaint_title']})
#         return jsonify(data), 200

    # data = mongo.db.notes.find({'complaint_title' : complaint_t})






    data = request.get_json()

    if request.method == 'DELETE': 
        if data.get('_id', None) is not None:
            db_response = mongo.db.notes.delete_one({'_id' : data['_id']})
            if db_response.deleted_count == 1:
                response = {'ok' : True, 'message' : 'record delete'}
            else:
                response = {'ok' : True, 'message': 'no record found'}
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400 


    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.notess.update_one(
                data['query'], {'$set': data.get('payload', {})}
            )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else: 
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400