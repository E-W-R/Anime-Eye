import pandas as pd
import requests
import json
import time

n_anime = 10
wait = 1

anime_data = pd.read_csv('anime_data.csv')
more_anime_data = pd.read_csv('more_anime_data.csv')
anime_dict = anime_data[['id', 'title']].set_index('id')['title'].to_dict()
covered = set(more_anime_data['id'])

with open('token.json') as f:
    data = json.load(f)
    access_token = data['access_token']

def url(ID):
    return f'''https://api.myanimelist.net/v2/anime/{ID}?fields=id,title,main_picture,
    alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,
    num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,
    num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,
    background,related_anime,related_manga,recommendations,studios,statistics'''
    
row_list = []
print('\nGetting Anime Information:')
for ID in anime_dict.keys():
    if n_anime == 0:
        break
    if ID in covered:
        continue
    time.sleep(wait)
    response = requests.get(url(ID), headers = {'Authorization' : 'Bearer ' + access_token})
    response = response.json()
    has_prequel = 'prequel' in [anime['relation_type'] for anime in response['related_anime']]
    genres = [genre['name'] for genre in response['genres']] + [""] * 5
    if response['media_type'] not in ['tv', 'movie', 'ona', 'ova']:
        continue
    Row = {key: response[key] for key in ['id', 'start_date', 'end_date',
    'mean', 'num_list_users', 'nsfw', 'media_type', 'num_episodes', 'rating']}
    Row['title'] = response['alternative_titles']['en']
    if Row['title'] == '':
        Row['title'] = response['title']
    Row['picture'] = response['main_picture']['large']
    Row['prequel'] = has_prequel
    Row['genre1'], Row['genre2'], Row['genre3'], Row['genre4'], Row['genre5'] = \
        genres[0], genres[1], genres[2], genres[3], genres[4]
    row_list.append(Row)
    n_anime -= 1
    print(Row['title'])

df = pd.DataFrame(row_list)
more_anime_data = pd.concat([more_anime_data, df], ignore_index = True)
more_anime_data.to_csv('more_anime_data.csv', index = False)