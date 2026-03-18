import librosa
import numpy as np
import essentia.standard as es

def extract_bpm_librosa(audio, sr, file_id):
    tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
    return {"file_id": file_id, "bpm_librosa": float(np.atleast_1d(tempo)[0]), "beats_librosa": beats.tolist()}

def extract_bpm_essentia(audio, file_id):
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, confidence, _, _ = rhythm_extractor(audio)

    return {"file_id": file_id, "bpm_essentia": bpm, "beats_confidence": confidence, "beats_essentia": beats.tolist()}
