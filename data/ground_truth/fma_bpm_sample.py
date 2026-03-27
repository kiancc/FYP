# Adapted from https://github.com/mdeff/fma/blob/master/usage.ipynb
import pandas as pd
import utils
from fma_prompt_utils import (
	TARGET_GENRES,
	SAMPLES_PER_GENRE,
	RANDOM_SEED,
	build_minimal_prompt_record,
	write_prompt_records_json,
)
# okay so first is to load data, then we join echonest and genres, then we find our genre and bpm
# this will be used for creating the BPM tests

# genres = utils.load('fma_metadata/genres.csv')
# features = utils.load('fma_metadata/features.csv')


# then need to do the same but with FMA K, we just use that dataset then the FMA API to 
# download the test songs, then run essentia etc

# Adapted from https://github.com/stellaywong/fma_keys/blob/master/keys.ipynb
tracks = utils.load("fma_metadata/tracks.csv")
tracks = tracks[tracks['set', 'subset'] <= 'medium']
echonest = utils.load('fma_metadata/echonest.csv')
genres = tracks[('track', 'genre_top')]
bpms = echonest[('echonest', 'audio_features', 'tempo')]

merged_data = pd.concat([genres, bpms], axis=1)
merged_data.columns = ['genre', 'bpm']

target_genres = TARGET_GENRES


final_df = merged_data.dropna()
final_df = final_df[final_df['genre'].isin(target_genres)]
final_df = final_df.reset_index().rename(columns={'index': 'track_id'})

samples_per_genre = SAMPLES_PER_GENRE
random_seed = RANDOM_SEED

sampled_df = (
	final_df.sample(frac=1, random_state=random_seed)
	.groupby('genre', group_keys=False)
	.head(samples_per_genre)
	.reset_index(drop=True)
)

output_file = 'ground_truth_fma_bpm.csv'
sampled_df.to_csv(output_file, index=False)

json_output_file = 'ground_truth_fma_bpm.json'
json_records = [
	build_minimal_prompt_record(
		genre=row['genre'],
		task='tempo',
		target=int(round(row['bpm'])),
		track_id=row['track_id'],
	)
	for _, row in sampled_df.iterrows()
]

write_prompt_records_json(json_records, json_output_file)

print(sampled_df.head())
print(f'\nSaved {len(sampled_df)} rows to {output_file}')
print(f'Saved {len(json_records)} rows to {json_output_file}')