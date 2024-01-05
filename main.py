import pandas as pd
import numpy as np
import requests
import json
import sys
import os
from openai import OpenAI


def vector(user, df):

    with open('token.json') as f:
        data = json.load(f)
        access_token = data['access_token']
    
    def url(user):
        return f'https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&limit=1000'
    
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

    ids = [int(ID[1:]) for ID in list(df.columns)]
    return np.array([scores[ID] if ID in scores else np.nan for ID in ids])


def user_cf(vec, df):

    ids = [int(ID[1:]) for ID in list(df.columns)]
    score_matrix = df.values

    pr_df = pd.read_csv('more_anime_data.csv')
    prequel_dict = pr_df[['id', 'prequel']].set_index('id')['prequel'].to_dict()
    img_dict = pr_df[['id', 'picture']].set_index('id')['picture'].to_dict()
    eng_dict = pr_df[['id', 'title']].set_index('id')['title'].to_dict()

    score_matrix = score_matrix[:, vec > 0]
    small_vec = vec[vec > 0]
    small_vec = (small_vec - np.mean(small_vec)) / np.std(small_vec)
    n_watched = len(small_vec)

    def d(v1, v2):
        non_zero_indices = (v2 > 0)
        v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
        n_common = np.sum(non_zero_indices)
        if n_common == 0:
            return np.inf
        v2 = (v2 - np.mean(v2)) / (np.std(v2) + 0.01)
        if n_common < 0.5 * n_watched:
            return 100 + np.mean(np.abs(v1 - v2))
        return np.mean(np.abs(v1 - v2))

    def CF(small_vec, vec, d, k, n_reccs):
        distances = np.apply_along_axis(lambda row: d(small_vec, row), axis = 1, arr = score_matrix)
        neighbours = np.argsort(distances)[:k]
        neigh_array = df.values[neighbours]
        neighbours = [df.index[n] for n in neighbours]
        def eval_arr(arr):
            if (np.sum(np.isnan(arr))) >= min(0.8 * k, k - 2):
                return 0
            return np.nanmean(arr)
        predictions = np.apply_along_axis(eval_arr, axis = 0, arr = neigh_array)
        recc = np.argsort(predictions)
        recc_ids = [ids[int(i)] for i in recc if not np.isnan(i) and np.isnan(vec[i])]
        recc_ids = [i for i in recc_ids if i in prequel_dict and prequel_dict[i] == False][::-1]
        recc = [eng_dict[i] for i in recc_ids][:n_reccs]
        pics = [img_dict[i] for i in recc_ids][:n_reccs]
        return (neighbours, recc_ids[:n_reccs], recc, pics)

    neighbours1, ids1, recommendations1, pictures1 = CF(small_vec, vec, d, 35, 8)
    neighbours2, ids2, recommendations2, pictures2 = CF(small_vec, vec, d, 7, 16)
    pictures2 = [p for p in pictures2 if p not in pictures1][:8]
    ids2 = [i for i in ids2 if i not in ids1][:8]

    return (pictures1, pictures2, ids1, ids2)


def item_cf(vec, df):
    
    ids = [int(ID[1:]) for ID in list(df.columns)]
    vec = [-1 if np.isnan(val) else val for val in vec]
    watched = set([ids[i] for i in range(len(vec)) if vec[i] != -1])
    favourites = [ids[i] for i in np.argsort(vec)[::-1][:min(len(vec), 30)]]

    pr_df = pd.read_csv('more_anime_data.csv')
    type_dict = pr_df[['id', 'media_type']].set_index('id')['media_type'].to_dict()

    item_neighbours = pd.read_csv('item_neighbours.csv')
    recc_ids = []
    recc = []
    pics = []
    for favourite in favourites:
        if len(recc_ids) == 16:
            break
        i = 0
        row = item_neighbours[item_neighbours['id'] == favourite]
        neighbour_ids = [int(name.strip('\'')) for name in row['ids'].values[0][1:-1].split(', ')]
        curr_id = neighbour_ids[i]
        while i < 10 and (curr_id in watched or curr_id in recc_ids or type_dict[curr_id] == 'ova'):
            i += 1
            curr_id = neighbour_ids[i % 10]
        if i == 10:
            continue
        recc_ids.append(neighbour_ids[i])
        neighbour_pics = [name.strip('\'') for name in row['pictures'].values[0][1:-1].split(', ')]
        pics.append(neighbour_pics[i])
    
    return (pics[:8], pics[8:], recc_ids[:8], recc_ids[8:])


def message(vec, df):

    ids = [int(ID[1:]) for ID in list(df.columns)]
    pr_df = pd.read_csv('more_anime_data.csv')
    eng_dict = pr_df[['id', 'title']].set_index('id')['title'].to_dict()

    os.environ["OPENAI_API_KEY"] = "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"

    client = OpenAI()

    tens = [eng_dict[ids[i]] for i in range(len(ids)) if vec[i] == 10]
    nines = [eng_dict[ids[i]] for i in range(len(ids)) if vec[i] == 9]
    if len(tens) >= 10:
        fav = tens
    else:
        fav = tens + nines
    fav = fav[:min(20, len(fav))]

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Your job is to make fun of people for their tastes in anime. Be creative and deliver a paragraph of quippy and snarky roasts. DO NOT reference any specific anime in your reply. Be personal, clever, relevant, and short."},
        {"role": "user", "content": "Here are my favourite anime, roast me. Do not refer to any of the anime in your reply. Be rude, clever, and don't hold back.\n" + ", ".join(fav)}
    ]
    )

    message = completion.choices[0].message.content

    return message