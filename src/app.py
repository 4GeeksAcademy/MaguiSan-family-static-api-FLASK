"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# -------------------------------------Endpoints--------------------------------
# GET /members-------------
# status_code 
# 200 si se realizó con éxito
# 400 si hubo un error por parte del cliente
# 500 si el servidor encuentra un error
# RESPONSE BODY (content-type: application/json):
# []  <!--- Lista de miembros de la familia -->

# Obtiene todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        if members == []:
           return jsonify({'error': 'Not found members'}), 404
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# GET /member/<int:member_id>----------------
# RESPONSE (content_type: application/json):
# status_code 200 si se realizó con éxito, 400 si hubo un error por parte del cliente, 500 si el servidor encuentra un error
# body:  <!--- el objeto json del miembro de la familia --> 
# {
#     "id": Int,
#     "first_name": String,
#     "age": Int,
#     "lucky_numbers": List
# }

# Obtiene un solo miembro de la familia
@app.route('/member/<int:member_id>', methods=['GET'])
def get_a_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        # print(member_id)
        if member == None:
           return jsonify({'error': 'Not found member'}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# POST /member -----------------
# REQUEST BODY (content_type: application/json):
# {
#     id: Int,
#     first_name: String,
#     age: Int,
#     lucky_numbers: []
# }
# RESPONSE (content_type: application/json):
# status_code 200 si se realizó con éxito, 400 si hubo un error por parte del cliente, 500 si el servidor encuentra un error

# Añade un nuevo miembro a la estructura de datos de la familia.
@app.route('/member', methods=['POST'])
def add_new_member():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Bad request', 'message': 'The request format is invalid. Please check the data you have sent.'}), 400
    try:
        request_body = request.get_json()
        # como sabe q tiene first_name, age, lucky_numbers :(, podria agregar mas keys
        # porq la funcion le da id y last_name
        new_list_members = jackson_family.add_member(request_body)
        return jsonify(new_list_members), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# DELETE /member/<int:member_id> -------------
# RESPONSE (content_type: application/json):
# status_code 200 si se realizó con éxito, 400 si hubo un error por parte del cliente, 500 si el servidor encuentra un error
# body: {
#     done: True
# }
# Elimina un miembro de la familia segun su id

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_a_member(member_id):
    try:
        deleted_member = jackson_family.delete_member(member_id)
        if deleted_member == None:
           return jsonify({'error': 'Not found member'}), 404
        return jsonify({'done': True}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
