import pandas as pd
import random
import uuid

class GeneratePrompts:

    def __init__(self, seed=16):
        random.seed(seed)
        self.genres = ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip Hop', 'Classical', 'Metal', 'Country', 'Blues']
        self.constraints = {
            'time_signature': ['4/4', '3/4', '5/4'],
            'tempo': [(60, 90), (100, 130), (140, 180)],
            'tempo_change': [0.25, -0.25, 0.5, -0.5],
            'tonic': ['C','D','F','B','C#','F#'],
            'mode': ['Major', 'Minor'],
            'modulation': ['to the fifth degree', 'to the relative Minor', 'to the relative Major', 'to the parallel Minor', 'to the parallel Major']
        }

        self.data = []

    def generate_prompts(self):
        for genre in self.genres:
            self.generate_tempo_prompt(genre)
            self.generate_key_prompt(genre)
            self.generate_key_modulation_prompt(genre)
            self.generate_tempo_change_prompt(genre)
            self.generate_time_signature_prompt(genre)

        df = pd.DataFrame(self.data)

        print(df['task'].value_counts())

        df.to_excel('master_prompts.xlsx', index=False)
        print('Generated Prompts')

    def add_record(self, genre, task, target, prompt):
        uid = uuid.uuid4().hex
        filename = f'{genre}_{task}_{target}_{uid}.wav'.replace(' ', '-')

        self.data.append({
            'id': uid,
            'genre': genre,
            'task': task,
            'target': target,
            'prompt': prompt,
            'filename': filename,
            'status': 'pending'
        })

    def generate_tempo_prompt(self, genre):
        samples = 4
        generated_bpms = set()

        for low_bpm, high_bpm in self.constraints['tempo']:
            for _ in range(samples):
                bpm = random.randint(low_bpm, high_bpm)
                while bpm in generated_bpms:
                    bpm = random.randint(low_bpm, high_bpm)
                generated_bpms.add(bpm)
                prompt = f'Generate a {genre} song at {bpm} BPM.'
                self.add_record(genre, 'tempo', bpm, prompt)
        
    def generate_key_prompt(self, genre):
        for tonic in self.constraints['tonic']:
            for mode in self.constraints['mode']:
                prompt = f'Generate a {genre} song in {tonic} {mode}.'
                self.add_record(genre, 'key', tonic + ' ' + mode, prompt)

    def generate_key_modulation_prompt(self, genre):

        for key_mod in self.constraints['modulation']:
            valid_starts = []
            for tonic in self.constraints['tonic']:
                for mode in self.constraints['mode']:
                    if ('Minor' in key_mod and 'Minor' in mode) or ('Major' in key_mod and 'Major' in mode):
                        continue
                    valid_starts.append((tonic, mode))
            
            random.shuffle(valid_starts)
            selected = valid_starts[:2]

            for tonic, mode in selected:
                prompt = f'Generate a {genre} song in {tonic} {mode} that modulates {key_mod}.'
                self.add_record(genre, 'key modulation', key_mod, prompt)

    def generate_tempo_change_prompt(self, genre):
        generated_bpms = set()
        
        for tempo_mod in self.constraints['tempo_change']:
            direction = 'increases' if tempo_mod > 0 else 'decreases'
            for low_bpm, high_bpm in self.constraints['tempo']:
                start_bpm = random.randint(low_bpm, high_bpm)
                target_bpm = int(start_bpm + (tempo_mod * start_bpm))
                while (start_bpm, target_bpm) in generated_bpms:
                    start_bpm = random.randint(low_bpm, high_bpm)
                    target_bpm = int(start_bpm + (tempo_mod * start_bpm))
                prompt = f'Generate a {genre} song at {start_bpm} BPM that {direction} to {target_bpm}.'
                target_str = f"{tempo_mod} ({start_bpm} to {target_bpm})"
                self.add_record(genre, 'tempo change', target_str, prompt)

    def generate_time_signature_prompt(self, genre):

        for time_sig in self.constraints['time_signature']:
            for low_bpm, high_bpm in self.constraints['tempo']:
                bpm = random.randint(low_bpm, high_bpm)
                prompt = f'Generate a {genre} song with a {time_sig} time signature at {bpm} BPM.'
                self.add_record(genre, 'time signature', time_sig, prompt)

# prompt_generator = GeneratePrompts()
# prompt_generator.generate_prompts()
