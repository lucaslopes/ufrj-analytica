import datetime
import requests


localhost = 'http://localhost:5000/'
data = {
    'name': 'Lucas Lopes',
    'birthdate': '1995-07-12',
    'date': '2050-07-12'}
    # 'date': datetime.date.today().strftime('%Y-%m-%d')}


req = requests.post(localhost+'age', json=data)
res = req.json()
print(res)