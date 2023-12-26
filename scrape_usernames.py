import requests
from bs4 import BeautifulSoup
import time

n_refresh = 100
wait = 2

with open('usernames.txt', 'r') as f:
    out = f.readlines()

for i in range(n_refresh):

    response = requests.get('https://myanimelist.net/users.php')
    soup = BeautifulSoup(response.text)

    print('\nBatch ' + str(i) + ':')
    for user in soup.find_all(class_ = 'picSurround'):
        link = user.find('a').get('href')
        user = link[9:]
        print(user)
        out.append(user + '\n')

    time.sleep(wait)

out = list(set(out))

with open('usernames.txt', 'w') as f:
    f.writelines(out)