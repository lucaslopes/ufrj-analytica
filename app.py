import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify, request


app = Flask(__name__)


def str2date(
        date: str,
    ) -> datetime.date:
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def today(
        output_str: bool = False,
        format: str = '%Y-%m-%d',
    ) -> datetime.date:
    today_date = datetime.date.today()
    if output_str:
        today_date = today_date.strftime(format)
    return today_date


def calc_age(
        birthdate: datetime.date,
        date: datetime.date = None,
    ) -> int:
    if type(birthdate) is str:
        birthdate = str2date(birthdate)
    if type(date) is str:
        date = str2date(date)
    date = today() if date is None else date
    age = relativedelta(date, birthdate).years
    return age


#############################################


def validade_data(data):
    error_messages = list()
    required_fields = ['name', 'birthdate', 'date']
    for field in required_fields:
        if field not in data:
            error_msg = f'Missing required field: {field}'
            error_messages.append(error_msg)
        if 'date' in field:
            try:
                str2date(data[field])
            except ValueError:
                error_msg = 'Invalid date format, expected yyyy-mm-dd'
                error_messages.append(error_msg)
    if str2date(data['date']) <= today():
        error_msg = '`date` must be in the future'
        error_messages.append(error_msg)
    errors = None
    if len(error_messages) > 0:
        errors = '; '.join(error_messages)
    return errors


@app.route('/age', methods=['POST'])
def age():
    data = request.json
    error_message = validade_data(data)
    if error_message is not None:
        return jsonify({'error': error_message}), 400
    name = data['name']
    birthdate = str2date(data['birthdate'])
    future_date = str2date(data['date'])
    fut_date_str = future_date.strftime('%d/%m/%Y')
    ageNow = calc_age(birthdate)
    ageThen = calc_age(birthdate, future_date)
    quote = f'Olá, {name}! Você tem {ageNow} anos e em {fut_date_str} você terá {ageThen} anos.'
    res = jsonify({
        'ageNow': ageNow,
        'ageThen': ageThen,
        'quote': quote})
    return res, 200


def main():
    app.run(debug=True)
    return True


__name__ == '__main__' and main()