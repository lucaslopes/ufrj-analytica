import requests


localhost = 'http://localhost:5000/'
data = {'name': 'Lucas'}
req = requests.post(localhost+'age', json=data)
res = req.json()
print(res)