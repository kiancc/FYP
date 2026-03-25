# Adapted from https://github.com/mdeff/fma/blob/master/usage.ipynb
import pandas as pd
import utils
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

target_genres = ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip-Hop', 'Classical', 'Country', 'Blues'] # missing metal, will need to find other example tracks


final_df = merged_data.dropna()
final_df = final_df[final_df['genre'].isin(target_genres)]
final_df = final_df.reset_index().rename(columns={'index': 'track_id'})

samples_per_genre = 5
random_seed = 42

sampled_df = (
	final_df.sample(frac=1, random_state=random_seed)
	.groupby('genre', group_keys=False)
	.head(samples_per_genre)
	.reset_index(drop=True)
)

output_file = 'target_genres_bpm_sampled.csv'
sampled_df.to_csv(output_file, index=False)

print(sampled_df.head())
print('\nSamples per genre:')
print(sampled_df['genre'].value_counts().sort_index())
print(f'\nSaved {len(sampled_df)} rows to {output_file}')