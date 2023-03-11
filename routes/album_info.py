from flask import Blueprint, jsonify, request

album_bp = Blueprint('album-info', __name__)

@album_bp.route('/album-info', methods=['GET'])
def album_info():
    res = jsonify({'data': 'hi'})
    return res, 200

