import librosa
import essentia.standard as es
from core.feature_extraction.base import FeatureExtractor

class BpmLibrosaExtractor(FeatureExtractor):
    @property
    def feature_name(self): return "bpm_librosa"

    def extract(self, audio, sr, file_idx):
        tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
        return {"file_idx": file_idx, "bpm": float(tempo), "beats": beats.tolist()}

class BpmEssentiaExtractor(FeatureExtractor):
    @property
    def feature_name(self): return "bpm_essentia"

    def extract(self, audio, sr, file_idx):
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, confidence, _, _ = rhythm_extractor(audio)
        return {"file_idx": file_idx, "bpm": bpm, "beats_confidence": confidence, "beats": beats.tolist()}