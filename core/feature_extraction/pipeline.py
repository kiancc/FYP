import os
import librosa
import essentia.standard as es
import pandas as pd

class FeaturePipeline:
    def __init__(self, extractors):
        # extractors: list of (audio_type, fn) tuples
        # audio_type is 'librosa' or 'essentia'
        self.extractors = extractors

    def process_file(self, file_path, file_id):
        librosa_audio, sr = librosa.load(file_path, sr=None, mono=True)
        essentia_audio = es.MonoLoader(filename=file_path)()
        row = {}

        for audio_type, extractor in self.extractors:
            if audio_type == 'librosa':
                row.update(extractor(librosa_audio, sr, file_id))
            elif audio_type == 'essentia':
                row.update(extractor(essentia_audio, file_id))
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