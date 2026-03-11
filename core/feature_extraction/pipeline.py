import os
import librosa
import pandas as pd

class FeaturePipeline:
    def __init__(self, extractors):
        self.extractors = extractors

    def process_file(self, file_path, file_idx):
        audio, sr = librosa.load(file_path, sr=None, mono=True)
        row = {}
        for extractor in self.extractors:
            row.update(extractor(audio, sr, file_idx))
        return row

    def process_directory(self, dir_path):
        rows = []
        for filename in os.listdir(dir_path):
            if not filename.endswith(".wav"):
                continue
            file_idx = os.path.splitext(filename)[0]
            try:
                rows.append(self.process_file(os.path.join(dir_path, filename), file_idx))
            except Exception as e:
                print(f"Failed on {filename}: {e}")
        return pd.DataFrame(rows)