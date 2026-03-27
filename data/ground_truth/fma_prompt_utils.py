import json
from pathlib import Path

TARGET_GENRES = [
    "Pop",
    "Rock",
    "Jazz",
    "Electronic",
    "Hip-Hop",
    "Classical",
    "Country",
    "Blues",
]

SAMPLES_PER_GENRE = 5
RANDOM_SEED = 42


def normalize_genre(genre):
    return str(genre)

def build_minimal_prompt_record(genre, task, target, track_id):
    target_str = str(target)
    return {
        "file_id": f"{int(track_id):06d}",
        "genre": normalize_genre(genre),
        "task": task,
        "target": target_str,
        "prompt": None,
    }

def padded_track_id(value):
    track_id = int(str(value).strip())
    return f"{track_id:06d}"
    
def write_prompt_records_json(records, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)
