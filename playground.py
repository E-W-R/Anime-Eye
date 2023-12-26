import requests
import json
from bs4 import BeautifulSoup

response = requests.get('https://api.myanimelist.net/v2/users/Evan0/animelist?fields=list_status&limit=1000', headers = {"Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNmZWUyMDc4NDFhNjYyODEyZWUzMTU5NjRmODg5NjI4YTNjYzlhZmNkYTA2MWZhMTJmY2NhMDU5ODE5ZTU1NzNmOGFlYTMyMzljZGQ3YTIwIn0.eyJhdWQiOiJjMzY5YzA2MzZkOTdmOTY2MmQ5YWIxNmI0OTRjNzRlZiIsImp0aSI6ImNmZWUyMDc4NDFhNjYyODEyZWUzMTU5NjRmODg5NjI4YTNjYzlhZmNkYTA2MWZhMTJmY2NhMDU5ODE5ZTU1NzNmOGFlYTMyMzljZGQ3YTIwIiwiaWF0IjoxNzAzMTk5NjgzLCJuYmYiOjE3MDMxOTk2ODMsImV4cCI6MTcwNTg3ODA4Mywic3ViIjoiMTUxNzQ2NDkiLCJzY29wZXMiOltdfQ.qyXc_VVnbgloP4ZGTwBd3gBIqLDeZ9JvvUr9pYKk6ecFyBXxgY8Qu_JzypDRjmlMsUfsUN3jwM3XVEU2_G22KmCofVp_JzjfczuEy4b0oCEVfzf3Z3y5UE2VhkeXPbM79fVb1co-WCFaJLV-JemBeFpbchD1yJeDQaw5TiDZA-ewOjXyU1pQYlheJS3F32lgv_T38frJPml7cy492Rx2RuCNUOyDg4r-rGXq0Ehfn8K5Z1YEv-Tvrzuki5TfyPAW71xJ3hJvsh3XiqQXYNlqJccSSbvvXLw3ZW-0RLaqJ5QbJKnW-uXDsFS0bj7DaupKQrPAOjVnWaVR3hpuDO_DvA"})

response.text

soup = BeautifulSoup(response.text)

with open('response.json', 'w') as file:
    json.dump(response.json(), file, indent = 4)

resp = response.json()

resp['data'][0]['list_status']


rep = requests.get('https://myanimelist.net/users.php')
rep.text
soup = BeautifulSoup(rep.text)

soup.find_all(class_ = 'picSurround')