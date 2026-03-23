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
            # this hackyness is because the audio file generated my each model is {model_name}_{file_id}
            # i.e. Lyria-002_Pop_tempo_100_80d685f3b5a24783b91ac231d61a3b4a.wav.
            # Due to the directory structure we can just have the file_id without risk of colliding filenames
            # but for sake of speed will just do this as this requires change and this hacky logic is already
            # coupled in other code ffs
            file_id = '_'.join(os.path.splitext(filename)[0].split('_')[1:])
            
            if file_id in processed_files:
                print(f'File already processed: {filename}')
                continue

            if '.mp3' in filename or '.wav' in filename:
                try:
                    rows.append(self.process_file(os.path.join(dir_path, filename), file_id))
                except Exception as e:
                    print(f"Failed on {filename}: {e}")
        return pd.DataFrame(rows)