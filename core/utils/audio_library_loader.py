import librosa
import essentia as es

def load_essentia_audio(audio_file):
    return es.MonoLoader(filename=audio_file)

def load_librosa_audio(audio_file):
    y, sr = librosa.load(audio_file, sr=None) # y is audio, sr is sample rate
    return y, sr