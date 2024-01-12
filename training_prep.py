import pandas as pd
import numpy as np

df = pd.read_csv('list_data.csv')
anime_df = pd.read_csv('more_anime_data.csv')

training_df = pd.DataFrame()
for index, row in df.iterrows():

    watched = [int(df.columns[i]) for i in range(df.shape[1]) if not np.isnan(row[i])]
    scores = [row[i] for i in range(df.shape[1]) if not np.isnan(row[i])]

    row_list = []
    for i in range(len(watched)):
        ID = watched[i]
        R = {}
        row_info = anime_df[anime_df['id'] == ID]
        try:
            for col in ['start_date', 'media_type', 'mean', 'num_list_users',
            'num_episodes', 'rating', 'title', 'genre1', 'genre2', 'genre3', 'genre4', 'genre5']:
                R[col] = row_info.iloc[0][col]
            R['score'] = scores[i]
            row_list.append(R)
        except:
            continue

    try:
        user_df = pd.DataFrame(row_list)
        user_df['start_date'] = [int(date[:4]) for date in user_df['start_date']]
        user_df['title'] = [len(title.split(" ")) for title in user_df['title']]

        for col in ['start_date', 'mean', 'num_list_users', 'num_episodes', 'title']:
            user_df['avg_' + col] = np.sum(user_df[col] * user_df['score']) / np.sum(user_df['score'])
        user_df['avg_score'] = np.sum(user_df['score'])
        user_df['std_score'] = np.std(user_df['score'])
        user_df['total_tv'] = np.sum(user_df['media_type'] == 'tv')
        user_df['total_movie'] = np.sum(user_df['media_type'] == 'movie')
        user_df['total_pg'] = np.sum(user_df['rating'] == 'pg_13')
        user_df['total_r'] = np.sum(user_df['rating'] == 'r')
    except:
        continue

    training_df = pd.concat([training_df, user_df], ignore_index = True)
    print(index)

training_df.to_csv('training.csv', index = False)