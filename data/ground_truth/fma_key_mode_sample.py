# Adapted from https://github.com/mdeff/fma/blob/master/usage.ipynb
import numpy as np
import utils
from fma_prompt_utils import (
    TARGET_GENRES,
    SAMPLES_PER_GENRE,
    RANDOM_SEED,
    build_minimal_prompt_record,
    write_prompt_records_json,
    padded_track_id,
)
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
target_genres = TARGET_GENRES

# Keep only rows in those genres
filtered = joined[
    joined[("track", "genre_top")].isin(target_genres)
].dropna(subset=[("track", "genre_top")])


# Take up to 5 random songs per selected genre.
# This avoids pandas groupby.apply column-dropping behavior across versions.
rng = np.random.default_rng(RANDOM_SEED)
sample_5_per_genre = (
    filtered
    .assign(_rand=rng.random(len(filtered)))
    .sort_values([("track", "genre_top"), "_rand"])
    .groupby(("track", "genre_top"), group_keys=False)
    .head(SAMPLES_PER_GENRE)
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
output_df["track_id"] = output_df["track_id"].astype(int)
output_df["track_id"] = output_df["track_id"].apply(padded_track_id)

output_file = "ground_truth_fma_key-mode.csv"
output_df.to_csv(output_file, index=False)

json_output_file = "ground_truth_fma_key-mode.json"
json_records = [
    build_minimal_prompt_record(
        genre=row["genre"],
        task="key",
        target=row["key_and_mode"],
        track_id=row["track_id"],
    )
    for _, row in output_df.iterrows()
]

write_prompt_records_json(json_records, json_output_file)

print("\nUp to 5 random songs per genre:")
print(output_df)
print("\nSaved", len(output_df), "rows to", output_file)
print("Saved", len(json_records), "rows to", json_output_file)