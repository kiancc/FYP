import os
import pandas as pd
from core.generators.lyria_adapter import LyriaAdapter
# from core.generators.acestep_adapter import AceStepAdapter
from core.feature_extraction import PIPELINE

generation_outputs_dir_cloud = "/content/drive/MyDrive" # for google cloud
generation_outputs_dir_local = 'data/audio_files' # for package

# TODO:  run generation
# def run_generation():
#     prompt_tasks_path = "/content/master_prompts_v2.csv" # need to make this not hardcoded
#     prompt_tasks_df = pd.read_csv(prompt_tasks_path, dtype=str)

#     # generate songs
#     for generator in [LyriaAdapter(), AceStepAdapter()]:
#         already_processed = set()

#         for root, dirs, files in os.walk(generation_outputs_dir):
#             for file_ in files:
#                 already_processed.add(file_)

#         print(f'Generating audio for {generator.model_name}')
#         for i, row in prompt_tasks_df.iterrows():
#             file_idx = row["file_idx"]
#             file_idx = row["file_idx"]
#             prompt_text = row['prompt'].strip()
#             out_name = f"{generator.model_name}_{file_idx}.wav"
#             out_path = os.path.join(generation_outputs_dir, generator.model_name, out_name)
#             if out_name in already_processed:
#                 print('File already existss')
#             else:
#                 audio_b64 = generator.generate(prompt_text)
#                 generator.save(audio_b64, out_path)
#                 print(f'Generated {out_name}')

# TODO:  run feature extraction
def run_feature_extraction(generation_outputs_dir):
    for subdir in os.listdir(generation_outputs_dir):
        subdir_path = os.path.join(generation_outputs_dir, subdir)
        print(subdir_path)
        if not os.path.isdir(subdir_path):
            continue
        # df = PIPELINE.process_directory(subdir_path)
        # df.to_csv(os.path.join(generation_outputs_dir, f"{subdir}_features.csv"), index=False)
# audio_models = {
#     'acestep': {'base_path': '/content/drive/MyDrive/AceStep_Output',},
#     'lyria': {'base_path': '/content/drive/MyDrive/Lyria_Output'}
# }
# master_prompts = '/content/master_prompts_v2.csv'

# master_prompts = '/content/master_prompts_v2.csv'

# for audio_model_name  in audio_models:
#     audio_model_info = audio_models[audio_model_name]
#     base_dir = f'{audio_model_info['base_path']}/'
#     # prompt_data = pd.read_csv(master_prompts).to_dict('records')
#     audio_files = []

#     for filename in os.listdir(base_dir):
#         if filename.endswith('.wav') and filename:
#             audio_files.append((base_dir + filename, filename))

#     print(f'Found {len(audio_files)} audio files for {audio_model_name}')

#     get_essentia_key_scale(base_dir, audio_model_name)
#     get_bpm_essentia(base_dir, audio_model_name)
#     get_bpm_librosa(base_dir, audio_model_name)


# TODO:  run feature plotting and exporting data




def main():
    # run_generation()
    # run_feature_extraction()
    # run_plotting_analysis()
    run_feature_extraction(generation_outputs_dir_local)

    pass


main()