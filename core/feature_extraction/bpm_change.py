import numpy as np

def extract_bpm_change(self, audio, window_size=15):
    """
    Analyzes the audio to see if tempo increased from start to finish.
    """
    # Initialize Essentia's Rhythm Extractor
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    
    # bpm: Global average BPM
    # ticks: The exact time (in seconds) of every detected beat
    bpm, beats, confidence, estimates, bpm_intervals = rhythm_extractor(audio)

    # If the algorithm failed to find enough beats, return fail state
    if len(beats) < (window_size * 2):
        return {
            "tempo_detected": False,
            "start_bpm": 0,
            "end_bpm": 0,
            "tempo_increased": False
        }

    # Calculate Inter-Beat Intervals (IBIs)
    # diff gets the time between each beat tick
    intervals = np.diff(beats)
    
    # Convert intervals to instantaneous BPM
    # BPM = 60 / seconds_between_beats
    ibi_bpms = 60.0 / intervals

    # Filter out extreme outliers (e.g., jumps above 300 or below 40) 
    # which are usually errors in beat tracking
    ibi_bpms = ibi_bpms[(ibi_bpms > 40) & (ibi_bpms < 300)]

    # Calculate Windowed Medians
    start_bpm = np.median(ibi_bpms[:window_size])
    end_bpm = np.median(ibi_bpms[-window_size:])

    # Binary check: Did it increase by at least 3 BPM?
    # Using a small buffer (3.0) prevents "false increases" from jitter
    increased = end_bpm > (start_bpm + 3.0)

    return {
        "global_bpm": bpm,
        "start_bpm": round(start_bpm, 2),
        "end_bpm": round(end_bpm, 2),
        "tempo_increased": bool(increased),
        "rhythm_confidence": confidence
    }