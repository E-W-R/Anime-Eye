import pandas as pd
import numpy as np
import requests
import json
import sys
import os
from openai import OpenAI

def main(user):

    df = pd.read_csv('list_data.csv')
    df = df.pivot_table(index = 'user', columns = 'id', values = 'score', aggfunc = 'max')
    ids = list(df.columns)
    score_matrix = df.values

    an_df = pd.read_csv('anime_data.csv')
    anime_dict = an_df[['id', 'title']].set_index('id')['title'].to_dict()

    pr_df = pd.read_csv('more_anime_data.csv')
    prequel_dict = pr_df[['id', 'prequel']].set_index('id')['prequel'].to_dict()
    img_dict = pr_df[['id', 'picture']].set_index('id')['picture'].to_dict()
    eng_dict = pr_df[['id', 'title']].set_index('id')['title'].to_dict()

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
                score = row['list_status']['score']
            except:
                continue
            if status == 'plan_to_watch':
                continue
            scores[ID] = score
        return np.array([scores[ID] if ID in scores else np.nan for ID in ids])

    vec = vector(user)

    score_matrix = score_matrix[:, vec > 0]
    small_vec = vec[vec > 0]
    small_vec = (small_vec - np.mean(small_vec)) / np.std(small_vec)
    n_watched = len(small_vec)

    def d(v1, v2):
        non_zero_indices = (v2 > 0)
        v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
        if sum(non_zero_indices) == 0:
            return np.inf
        v2 = (v2 - np.mean(v2)) / (np.std(v2) + 0.01)
        if sum(non_zero_indices) < 0.4 * n_watched:
            return 100 + np.mean(np.abs(v1 - v2))
        return np.mean(np.abs(v1 - v2))

    def CF(small_vec, vec, d, k, n_reccs):
        distances = np.apply_along_axis(lambda row: d(small_vec, row), axis = 1, arr = score_matrix)
        neighbours = np.argsort(distances)[:k]
        neigh_array = df.values[neighbours]
        neighbours = [df.index[n] for n in neighbours]
        def eval_arr(arr):
            if (np.sum(np.isnan(arr))) >= min(0.5 * k, k - 2):
                return 0
            return np.nanmean(arr)
        predictions = np.apply_along_axis(lambda col: eval_arr(col), axis = 0, arr = neigh_array)
        recc = np.argsort(predictions)
        recc_ids = [ids[int(i)] for i in recc if not np.isnan(i) and np.isnan(vec[i])]
        recc_ids = [i for i in recc_ids if i in prequel_dict and prequel_dict[i] == False][::-1]
        recc = [eng_dict[i] for i in recc_ids][:n_reccs]
        pics = [img_dict[i] for i in recc_ids][:n_reccs]
        return (neighbours, recc_ids[:n_reccs], recc, pics)

    neighbours1, ids1, recommendations1, pictures1 = CF(small_vec, vec, d, 50, 8)
    neighbours2, ids2, recommendations2, pictures2 = CF(small_vec, vec, d, 7, 16)
    pictures2 = [p for p in pictures2 if p not in pictures1][:8]
    ids2 = [i for i in ids2 if i not in ids1][:8]

    
    os.environ["OPENAI_API_KEY"] = ...

    client = OpenAI()

    tens = [eng_dict[ids[i]] for i in range(len(ids)) if vec[i] == 10]
    nines = [eng_dict[ids[i]] for i in range(len(ids)) if vec[i] == 9]
    if len(tens) >= 10:
        fav = tens
    else:
        fav = tens + nines
    fav = fav[:min(20, len(fav) - 1)]

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a wise, all seeing, all knowing being. Your job is to make fun of people for their tastes in anime. Be creative and deliver a short paragraph of quippy and snarky roasts. Don't reference any anime, just make fun of the general trends in their tastes. Be personal, very clever and relevant."},
        {"role": "user", "content": "Here are my favourite anime, roast me. " + ", ".join(fav)}
    ]
    )

    message = completion.choices[0].message.content

    return (pictures1, pictures2, ids1, ids2, message)