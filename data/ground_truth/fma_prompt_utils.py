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


def track_stem_from_id(track_id):
    return f"{int(track_id):06d}"


def build_file_id(track_id=None, file_path=None, prefix=None):
    if file_path is not None:
        base = Path(str(file_path)).stem
    elif track_id is not None:
        base = track_stem_from_id(track_id)
    else:
        raise ValueError("Either track_id or file_path must be provided")

    if prefix:
        return f"{prefix}{base}"
    return base


def build_minimal_prompt_record(genre, task, target, track_id=None, file_path=None, prefix=None):
    target_str = str(target)
    return {
        "file_id": build_file_id(track_id=track_id, file_path=file_path, prefix=prefix),
        "genre": normalize_genre(genre),
        "task": task,
        "target": target_str,
        "prompt": None,
    }


def write_prompt_records_json(records, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)
