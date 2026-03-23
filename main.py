import os
import pandas as pd
from core.generators.lyria_adapter import LyriaAdapter
# from core.generators.acestep_adapter import AceStepAdapter
from core.feature_extraction.pipeline import FeaturePipeline

generation_outputs_dir_cloud = "/content/drive/MyDrive/fyp_audio" # for google cloud
prompt_tasks_path_cloud = "/content/master_prompts_v2.csv"

generation_outputs_dir_local = 'data/audio_files' # for package
prompt_tasks_path_local = "data/prompts/master_prompts_v2.csv"

# TODO:  run generation
def run_generation(generation_outputs_dir, prompt_tasks):
    prompt_tasks_df = pd.read_csv(prompt_tasks, dtype=str)

    # generate songs by iterating over adapters, should abstract this to just call a master adapter
    # and pass the audio file director path to check if already processed
    for generator in [LyriaAdapter()]:
        already_processed = set()

        for root, dirs, files in os.walk(generation_outputs_dir):
            for file_ in files:
                already_processed.add(file_)

        for i, row in prompt_tasks_df.iterrows():
            file_id = row["file_id"]
            file_id = row["file_id"]
            prompt_text = row['prompt'].strip()
            out_name = f"{generator.model_name}_{file_id}.wav"
            out_path = os.path.join(generation_outputs_dir, generator.model_name, out_name)
            
            if out_name in already_processed:
                print('File already exists')
            else:
                print(f'Generating audio for {generator.model_name}')
                audio_b64 = generator.generate(prompt_text)
                generator.save(audio_b64, out_path)
                print(f'Generated {out_name}')

# TODO:  run feature extraction
def run_feature_extraction(generation_outputs_dir):
    feature_pipeline = FeaturePipeline()

    for subdir in os.listdir(generation_outputs_dir):
        subdir_path = os.path.join(generation_outputs_dir, subdir)
        root = subdir_path.split('/')[0]
        
        outdir = os.path.join(root, f'features')

        if not os.path.isdir(subdir_path):
            continue

        df = feature_pipeline.process_directory(subdir_path)
        df.to_csv(os.path.join(outdir, f"{subdir}_features.csv"), index=False)
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
    # run_generation(generation_outputs_dir_local, prompt_tasks_path_local)
    run_feature_extraction(generation_outputs_dir_local)
    # run_plotting_analysis()
    # run_feature_extraction(generation_outputs_dir_local)

    pass


main()