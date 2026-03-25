import os
import shutil
from pathlib import Path
import pandas as pd
import utils

def padded_track_id(value):
    track_id = int(str(value).strip())
    return f"{track_id:06d}"

def match_csv(input_csv, output_csv, audio_dir, out_dir):
    df = pd.read_csv(input_csv)

    df["track_id"] = df["track_id"].astype(int)
    df["track_id_padded"] = df["track_id"].apply(padded_track_id)

    df["audio_path"] = df["track_id"].apply(
        lambda tid: str(Path(utils.get_audio_path(str(audio_dir), int(tid))))
    )

    os.makedirs(out_dir, exist_ok=True)
    for src in df["audio_path"]:
        src_path = Path(src)
        if src_path.exists():
            shutil.copy2(src_path, Path(out_dir) / src_path.name)

    df.to_csv(output_csv, index=False)

def main():
    script_dir = Path(__file__).resolve().parent
    audio_dir = os.path.join(script_dir, "fma_medium", "fma_medium")
    out_dir = os.path.join(script_dir, "audio_files")

    jobs = [
        (
            "target_genres_bpm_sampled.csv",
            "target_genres_bpm_sampled_with_audio_paths.csv",
        ),
        (
            "target_genres_key_mode_sampled.csv",
            "target_genres_key_mode_sampled_with_audio_paths.csv",
        ),
    ]

    for input_csv, output_csv in jobs:
        match_csv(input_csv, output_csv, audio_dir, out_dir)

if __name__ == "__main__":
    main()