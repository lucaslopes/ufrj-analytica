import utils
from flask import Blueprint, jsonify, request


age_bp = Blueprint('age', __name__)


def validade_data(data):
    error_messages = list()
    required_fields = ['name', 'birthdate', 'date']
    for field in required_fields:
        if field not in data:
            error_msg = f'Missing required field: {field}'
            error_messages.append(error_msg)
        if 'date' in field:
            try:
                utils.str2date(data[field])
            except ValueError:
                error_msg = 'Invalid date format, expected yyyy-mm-dd'
                error_messages.append(error_msg)
    if utils.str2date(data['date']) <= utils.today():
        error_msg = '`date` must be in the future'
        error_messages.append(error_msg)
    errors = None
    if len(error_messages) > 0:
        errors = '; '.join(error_messages)
    return errors


@age_bp.route('/age', methods=['POST'])
def age():
    data = request.json
    error_message = validade_data(data)
    if error_message is not None:
        return jsonify({'error': error_message}), 400
    name = data['name']
    birthdate = utils.str2date(data['birthdate'])
    future_date = utils.str2date(data['date'])
    fut_date_str = future_date.strftime('%d/%m/%Y')
    ageNow = utils.calc_age(birthdate)
    ageThen = utils.calc_age(birthdate, future_date)
    quote = f'Olá, {name}! Você tem {ageNow} anos e em {fut_date_str} você terá {ageThen} anos.'
    res = jsonify({
        'ageNow': ageNow,
        'ageThen': ageThen,
        'quote': quote})
    return res, 200

