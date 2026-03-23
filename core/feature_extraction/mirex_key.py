import os
import csv
import essentia.standard as es

def get_mirex_score(t_key, t_mode, p_key, p_mode):
    note_map = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
                'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
    
    t_val, p_val = note_map.get(t_key), note_map.get(p_key)
    if t_val is None or p_val is None: return 0.0
    
    dist = (p_val - t_val) % 12
    t_mode, p_mode = t_mode.lower(), p_mode.lower()

    if dist == 0 and t_mode == p_mode: return 1.0 # Same
    if dist == 7 and t_mode == p_mode: return 0.5 # 5th
    if t_mode == 'major' and p_mode == 'minor' and dist == 9: return 0.3 # Rel
    if t_mode == 'minor' and p_mode == 'major' and dist == 3: return 0.3 # Rel
    if dist == 0 and t_mode != p_mode: return 0.2 # Parallel
    return 0.0

def mirex_key(target_key, target_mode, detected_key, detected_scale, strength):

    score = get_mirex_score(target_key, target_mode, detected_key, detected_scale)
    return {
        'Mirex Target': f"{target_key} {target_mode}",
        'Mirex Detected': f"{detected_key} {detected_scale}",
        'Mirex Score': score,
        'Mirex Confidence': round(strength, 3)
    }