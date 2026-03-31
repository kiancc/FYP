import numpy as np

def extract_bpm_change(bpm, beats, window_size=15):
    # diff gets the time between each beat tick
    intervals = np.diff(beats)
    
    # onvert intervals to instantaneous BPM
    # BPM = 60 / seconds_between_beats
    ibi_bpms = 60.0 / intervals

    # calculate Windowed Medians
    start_bpm = np.median(ibi_bpms[:window_size])
    end_bpm = np.median(ibi_bpms[-window_size:])

    # Using a small buffer (3.0) prevents "false increases" from jitter
    increased = end_bpm > (start_bpm + 3.0)

    return {
        "global_bpm": bpm,
        "start_bpm": round(start_bpm, 2),
        "end_bpm": round(end_bpm, 2),
        "tempo_increased": bool(increased)
    }