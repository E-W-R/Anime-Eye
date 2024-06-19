import pandas as pd
import numpy as np

animes = pd.read_csv('short_anime_data.csv')
ids = [str(ID) for ID in list(set(animes["main_anime"]))]

df = pd.DataFrame().astype(pd.SparseDtype("float", 0))
for i in range(1, 129):
    print(i)
    ndf = pd.read_csv("/Users/evanrossiter/Documents/Code/Anime-Eye/users/%s.csv" % i, index_col = 0)
    ndf = ndf.astype(pd.SparseDtype("float", 0))
    df = pd.concat([df, ndf], ignore_index=True)

ids = list(set(ids) & set(df.columns))
df = df[ids]

n_cols = len(ids)
def cosine(v1, v2):
    b1, b2 = v1 > 0, v2 > 0
    non_zero_indices = (b1) & (b2)
    if np.sum(non_zero_indices) < 50:
        return 0
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    similarity = dot_product / (norm_v1 * norm_v2)
    return similarity

def common(v1, v2):
    b1, b2 = v1 > 0, v2 > 0
    non_zero_indices = (b1) & (b2)
    return np.sum(non_zero_indices) / min(np.sum(b1), np.sum(b2))

def mad(v1, v2):
    b1, b2 = v1 > 0, v2 > 0
    non_zero_indices = (b1) & (b2)
    if np.sum(non_zero_indices) < 50:
        return 0
    v1, v2 = v1[non_zero_indices], v2[non_zero_indices]
    return 1 - np.mean(np.abs(v1 - v2)) / 10

distance_matrix = np.zeros((n_cols, n_cols))
for i in range(n_cols):
    print(i)
    ID = ids[i]
    vec = df[ID]
    distances = df.apply(lambda col: mad(vec, col), axis = 0)
    distance_matrix[i, :] = distances

out = pd.DataFrame(distance_matrix)
out.index = ids
out.columns = ids
out.to_csv("similarities.csv", index = True)