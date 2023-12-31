import pandas as pd
import numpy as np
import requests
import json

df = pd.read_csv('list_data.csv')
df = df.pivot_table(index = 'user', columns = 'id', values = 'score', aggfunc = 'max')
ids = list(df.columns)
score_matrix = df.values

df = pd.read_csv('anime_data.csv')
anime_dict = df[['id', 'title']].set_index('id')['title'].to_dict()

with open('token.json') as f:
    data = json.load(f)
    access_token = data['access_token']

def url(user):
    return f'https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&limit=1000'

def vector(user):
    response = requests.get(url(user), headers = {'Authorization' : 'Bearer ' + access_token})
    response = response.json()
    scores = {}
    for row in response['data']:
        try:
            ID, title, picture = row['node'].values()
            medium, large = picture.values()
            status = row['list_status']['status']
        except:
            continue
        if status == 'plan_to_watch' or score == 0:
            continue
        scores[ID] = score
    return np.array([scores[ID] if ID in scores else np.nan for ID in ids])

def d1(v1, v2):
    non_zero_indices = (v1 > 0) & (v2 > 0)
    if sum(non_zero_indices) < 10:
        return np.inf
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    v1 = (v1 - np.mean(v1)) / np.std(v1)
    v2 = (v2 - np.mean(v2)) / np.std(v2)
    return np.mean(np.abs(v1 - v2))

def d2(v1, v2):
    non_zero_indices = (v1 > 0) & (v2 > 0)
    if sum(non_zero_indices) < 10:
        return np.inf
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    return np.mean(np.abs(v1 - v2))

def d3(v1, v2):
    common = sum((v1 > 0) & (v2 > 0))
    if common == 0:
        return 2
    return 1 / common

def d4(v1, v2):
    non_zero_indices = (v1 > 0) & (v2 > 0)
    if sum(non_zero_indices) < 10:
        return np.inf
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    return 1 - np.corrcoef(v1, v2)[0,1]

def d5(v1, v2):
    common = sum((v1 == 9) & (v2 == 9))
    if common == 0:
        return 2
    return 1 / common

def CF(user, d, k):
    vec = vector(user)
    distances = np.apply_along_axis(lambda row: d(vec, row), axis = 1, arr = score_matrix)
    neighbours = np.argsort(distances)[:k]
    neigh_array = score_matrix[neighbours]
    def eval_arr(arr):
        if (np.sum(np.isnan(arr))) >= min(0.9 * k, k - 1):
            return 0
        return np.nanmean(arr)
    predictions = np.apply_along_axis(lambda col: eval_arr(col), axis = 0, arr = neigh_array)
    recc = np.argsort(predictions)
    return [anime_dict[ids[int(i)]] for i in recc if not np.isnan(i) and np.isnan(vec[i])][-10:][::-1]

CF('Evan0', d4, 20)