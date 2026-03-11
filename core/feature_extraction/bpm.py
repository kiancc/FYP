import librosa
import essentia.standard as es

def extract_bpm_librosa(audio, sr, file_idx):
    tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
    return {"file_idx": file_idx, "bpm_librosa": float(tempo), "beats_librosa": beats.tolist()}

def extract_bpm_essentia(audio, sr, file_idx):
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, confidence, _, _ = rhythm_extractor(audio)
    return {"file_idx": file_idx, "bpm_essentia": bpm, "beats_confidence": confidence, "beats_essentia": beats.tolist()}