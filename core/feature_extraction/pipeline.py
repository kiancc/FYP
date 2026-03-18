import os
import librosa
import essentia.standard as es
import pandas as pd

from core.feature_extraction.bpm import extract_bpm_librosa, extract_bpm_essentia
from core.feature_extraction.key_scale import extract_essentia_key_scale

class FeaturePipeline:

    def process_file(self, file_path, file_id):
        row = {}

        librosa_audio, sr = librosa.load(file_path, sr=None, mono=True)
        essentia_audio = es.MonoLoader(filename=file_path)()
        row.update(extract_bpm_essentia(librosa_audio, file_id))
        row.update(extract_bpm_librosa(essentia_audio, sr, file_id))
        row.update(extract_essentia_key_scale(essentia_audio, file_id))

        print(f'Extracted features for {file_path}')
        return row

    def process_directory(self, dir_path):
        rows = []
        for filename in os.listdir(dir_path):
            file_id = os.path.splitext(filename)[0]
            try:
                rows.append(self.process_file(os.path.join(dir_path, filename), file_id))
            except Exception as e:
                print(f"Failed on {filename}: {e}")
        return pd.DataFrame(rows)