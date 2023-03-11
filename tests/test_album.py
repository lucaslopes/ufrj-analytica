import requests
from utils import localhost

req = requests.get(localhost+'album-info')
res = req.json()
print(res)