import requests
from utils import localhost


data = {
    'name': 'Lucas Lopes',
    'birthdate': '1995-07-12',
    'date': '2050-07-12'}
req = requests.post(localhost+'age', json=data)
res = req.json()
print(res)
# {'ageNow': 27, 'ageThen': 55, 'quote': 'Olá, Lucas Lopes! Você tem 27 anos e em 12/07/2050 você terá 55 anos.'}


data_wrong = {
    'birthdate': '12/7/1995',
    'date': '2020-07-12'}
req_wrong = requests.post(localhost+'age', json=data_wrong)
res_wrong = req_wrong.json()
print(res_wrong)
# {'error': 'Missing required field: name; Invalid date format, expected yyyy-mm-dd; `date` must be in the future'}

