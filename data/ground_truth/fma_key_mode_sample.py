# Adapted from https://github.com/mdeff/fma/blob/master/usage.ipynb
import numpy as np
import utils
# okay so first is to load data, then we join echonest and genres, then we find our genre and bpm
# this will be used for creating the BPM tests

tracks = utils.load('fma_metadata/tracks.csv')
# genres = utils.load('fma_metadata/genres.csv')
# features = utils.load('fma_metadata/features.csv')
# echonest = utils.load('fma_metadata/echonest.csv')

# then need to do the same but with FMA K, we just use that dataset then the FMA API to 
# download the test songs, then run essentia etc

# Adapted from https://github.com/stellaywong/fma_keys/blob/master/keys.ipynb
tracks = utils.load("fma_metadata/tracks.csv")
tracks = tracks[tracks['set', 'subset'] <= 'medium']
keys = utils.load("fma_metadata/keys.csv")
# print("Number of tracks with key and mode: %d" % len(keys))
joined = tracks.join(keys, how="inner")
# print("Number of unique keys and modes: %d" % joined[("key_and_mode", "key_and_mode")].nunique())
joined["key_and_mode"].groupby(["key_and_mode"])["key_and_mode"].size().sort_values(ascending=False)
# print(joined["track"].groupby(["genre_top"])["genre_top"].size().sort_values(ascending=False))


# Genres you want to allow
target_genres = ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip-Hop', 'Classical', 'Country', 'Blues'] # missing metal, will need to find other example tracks

# Keep only rows in those genres
filtered = joined[
    joined[("track", "genre_top")].isin(target_genres)
].dropna(subset=[("track", "genre_top")])


# Take up to 5 random songs per selected genre.
# This avoids pandas groupby.apply column-dropping behavior across versions.
rng = np.random.default_rng(42)
sample_5_per_genre = (
    filtered
    .assign(_rand=rng.random(len(filtered)))
    .sort_values([("track", "genre_top"), "_rand"])
    .groupby(("track", "genre_top"), group_keys=False)
    .head(5)
    .drop(columns=["_rand"])
)

output_df = sample_5_per_genre[[
    ("track", "title"),
    ("track", "genre_top"),
    ("key_and_mode", "key_and_mode"),
]].copy()
output_df.columns = ["title", "genre", "key_and_mode"]
output_df.insert(0, "track_id", sample_5_per_genre.index)
output_df = output_df.reset_index(drop=True)

output_file = "target_genres_key_mode_sampled.csv"
output_df.to_csv(output_file, index=False)

print("\nUp to 5 random songs per genre:")
print(output_df)
print("\nSaved", len(output_df), "rows to", output_file)