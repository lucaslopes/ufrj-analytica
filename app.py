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


@app.route('/age', methods=['POST'])
def age():
    data = request.json
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
    return res


def main():
    app.run(debug=True)
    return True


__name__ == '__main__' and main()