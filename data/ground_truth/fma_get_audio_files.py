import pandas as pd

target_genres = 'target_genres_bpm_sampled.csv'

target_bpms = 'target_genres_key_mode_sampled.csv'


df_genres = pd.read_csv(target_genres)
df_bpms = pd.read_csv(target_bpms)

combined = pd.concat([df_genres, df_bpms]).drop_duplicates(subset=['track_id'])
combined = combined.sort_values('track_id')

for track_id in combined['track_id']:
    print(track_id)