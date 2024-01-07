import pandas as pd
import numpy as np
import requests
import json
import sys

df = pd.read_csv('list_data.csv')
ids = list(df.columns)
score_matrix = df.values

an_df = pd.read_csv('anime_data.csv')
anime_dict = an_df[['id', 'title']].set_index('id')['title'].to_dict()

pr_df = pd.read_csv('more_anime_data.csv')
prequel_dict = pr_df[['id', 'prequel']].set_index('id')['prequel'].to_dict()
img_dict = pr_df[['id', 'picture']].set_index('id')['picture'].to_dict()
eng_dict = pr_df[['id', 'title']].set_index('id')['title'].to_dict()

n_cols = score_matrix.shape[1]
def cosine(v1, v2):
    non_zero_indices = (v1 > 0) & (v2 > 0)
    if np.sum(non_zero_indices) < 300:
        return 1
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    similarity = dot_product / (norm_v1 * norm_v2)
    return 1 - similarity

row_list = []
for i in range(n_cols):
    vec = score_matrix[:, i]
    distances = np.apply_along_axis(lambda col: cosine(vec, col), axis = 0, arr = score_matrix)
    recc = np.argsort(distances)
    recc_ids = [int(ids[int(i)]) for i in recc if not np.isnan(i)]
    recc_ids = [i for i in recc_ids if i in prequel_dict and prequel_dict[i] == False]
    recc = [eng_dict[i] for i in recc_ids][:10]
    pics = [img_dict[i] for i in recc_ids][:10]
    row_list.append({'ids': recc_ids[:10], 'recommendations': recc, 'pictures': pics})
    print(i)

for i in range(len(row_list)):
    row_list[i]['id'] = int(ids[i])
df = pd.DataFrame(row_list)
df.to_csv("item_neighbours.csv", index = False)