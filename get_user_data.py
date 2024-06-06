import requests
import json
import pandas as pd
import time

n_users = 5
row_limit = 1000
wait = 3

list_data = pd.read_csv('users/1.csv', index_col = 0)
l_rows = list_data.shape[0]

with open('anime_ids.txt', 'r') as f:
    anime_ids = set(f.readlines())
with open('logged_users.txt', 'r') as f:
    logged_users = [l.strip() for l in f.readlines()]
    logged_users = set(logged_users)
with open('usernames.txt', 'r') as f:
    usernames = [l.strip() for l in f.readlines()]
    usernames = set(usernames)
to_visit = list(usernames - logged_users)[:n_users]

with open('token.json', 'r') as f:
    data = json.load(f)
    access_token = data['access_token']

def url(user):
    return f'https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&limit={row_limit}'

row_list = []
usernames = []
print('\nGetting User Data:')
for user in to_visit:
    time.sleep(wait)
    response = requests.get(url(user), headers = {'Authorization' : 'Bearer ' + access_token})
    try:    response = response.json()
    except: continue
    if 'data' not in response:
        continue
    user_row = {}
    for row in response['data']:
        try:
            ID, title, picture = row['node'].values()
            status = row['list_status']['status']
            score = row['list_status']['score']
        except:
            continue
        if ID not in anime_ids:
            anime_ids.add(ID)
        if status == 'plan_to_watch' or score == 0:
            continue
        user_row[ID] = score
    logged_users.add(user)
    if user_row:
        row_list.append(user_row)
        usernames.append(user)
    print(user)

df = pd.DataFrame(row_list, index = usernames)
# df.index += l_rows
list_data = pd.concat([list_data, df], ignore_index = False)

list_data.to_csv('users/1.csv', index = True)

with open('logged_users.txt', 'w') as f:
    f.writelines([s + '\n' for s in list(logged_users)])

with open('anime_ids.txt', 'w') as f:
    f.writelines([str(s) + '\n' for s in list(anime_ids)])