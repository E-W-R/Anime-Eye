import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

n_users = input("\nNumber of Users: ")
row_limit = 1000
wait = input("Time to Wait: ")

list_data = pd.read_csv('list_data.csv')
l_rows = list_data.shape[0]
anime_data = pd.read_csv('anime_data.csv')
anime_ids = set(anime_data['id'])

with open('logged_users.txt') as f:
    logged_users = [l.strip() for l in f.readlines()]
    logged_users = set(logged_users)
with open('usernames.txt') as f:
    usernames = [l.strip() for l in f.readlines()]
    usernames = set(usernames)
to_visit = list(usernames - logged_users)[:n_users]

with open('token.json') as f:
    data = json.load(f)
    access_token = data['access_token']

def url(user):
    return f'https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&limit={row_limit}'

i = l_rows
row_list = []
print('\nGetting User Data:')
for user in to_visit:
    response = requests.get(url(user), headers = {'Authorization' : 'Bearer ' + access_token})
    response = response.json()
    if 'data' not in response:
        continue
    for row in response['data']:
        ID, title, picture = row['node'].values()
        medium, large = picture.values()
        status = row['list_status']['status']
        score = row['list_status']['score']
        if status == 'plan_to_watch' or score == 0:
            continue
        row_list.append({'user': user, 'id': ID, 'status': status, 'score': score})
        if ID not in anime_ids:
            anime_data = pd.concat([anime_data,
            pd.DataFrame({'id': ID, 'title': title, 'medium_picture': medium, 'large_picture': large}, index = [0])],
            ignore_index = True)
            anime_ids.add(ID)
    logged_users.add(user)
    print(user)

with open('logged_users', 'w') as f:
    f.writelines(list(logged_users))

df = pd.DataFrame(row_list)
df.index += l_rows
list_data = pd.concat([list_data, df], ignore_index = True)

anime_data.to_csv('anime_data.csv')
list_data.to_csv('list_data.csv')
