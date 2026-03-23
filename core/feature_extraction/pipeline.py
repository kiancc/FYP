import os
import librosa
import essentia.standard as es
import pandas as pd

from core.feature_extraction.bpm import extract_bpm_librosa, extract_bpm_essentia
from core.feature_extraction.key_scale import extract_essentia_key_scale
from core.feature_extraction.bpm_change import extract_bpm_change
from core.feature_extraction.mirex_key import mirex_key

class FeaturePipeline:

    def process_file(self, file_path, file_id):
        row = {}

        audio, sr = librosa.load(file_path, sr=44100, mono=True)

        row.update(extract_bpm_essentia(audio, file_id))
        row.update(extract_bpm_librosa(audio, sr, file_id))
        row.update(extract_essentia_key_scale(audio, file_id))
        row.update(extract_bpm_change(row.get('bpm_essentia'), row.get('beats_essentia_raw')))

        print(f'Extracted features for {file_path}')
        return row

    def process_directory(self, dir_path, processed_files):
        rows = []
        for filename in os.listdir(dir_path):
            file_id = os.path.splitext(filename)[0]
            if file_id in processed_files:
                print(f'File already processed: {filename}')
                continue

            if '.mp3' in filename or '.wav' in filename:
                try:
                    rows.append(self.process_file(os.path.join(dir_path, filename), file_id))
                except Exception as e:
                    print(f"Failed on {filename}: {e}")
        return pd.DataFrame(rows)