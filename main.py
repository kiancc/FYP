import os
import pandas as pd
from core.generators.lyria_adapter import LyriaAdapter
from core.generators.acestep_adapter import AceStepAdapter
from core.feature_extraction.pipeline import FeaturePipeline

def run_generation(output_dir, prompt_csv):
    if not os.path.exists(prompt_csv):
        raise FileNotFoundError(f"Prompt file not found at {prompt_csv}")

    prompt_tasks_df = pd.read_csv(prompt_csv, dtype=str)
    
    
    generators = [LyriaAdapter(), AceStepAdapter()]

    for generator in generators:
        model_path = os.path.join(output_dir, generator.model_name)
        os.makedirs(model_path, exist_ok=True)

        existing_files = set(os.listdir(model_path))

        for _, row in prompt_tasks_df.iterrows():
            file_id = row["file_id"]
            prompt_text = row['prompt'].strip()
            out_name = f"{generator.model_name}_{file_id}.wav"
            out_path = os.path.join(model_path, out_name)
            
            if out_name in existing_files:
                print(f"Already exists: {out_name}")
                continue
                
            print(f"Generating [{generator.model_name}]: {prompt_text[:30]}...")
            audio_b64 = generator.generate(prompt_text)
            generator.save(audio_b64, out_path)

def run_feature_extraction(audio_dir):
    pipeline = FeaturePipeline()
    parent_dir = os.path.dirname(audio_dir)
    features_out_dir = os.path.join(parent_dir, "features")
    os.makedirs(features_out_dir, exist_ok=True)

    for model_name in os.listdir(audio_dir):
        model_path = os.path.join(audio_dir, model_name)
        if not os.path.isdir(model_path):
            continue
            
        print(f"Extracting features for model: {model_name}")
        df = pipeline.process_directory(model_path)
        
        output_file = os.path.join(features_out_dir, f"{model_name}_features.csv")
        df.to_csv(output_file, index=False)
        print(f"Saved features to {output_file}")

if __name__ == "__main__":
    # Local defaults for when running main.py directly
    LOCAL_AUDIO = 'data/audio_files'
    LOCAL_PROMPTS = 'data/prompts/master_prompts_v2.csv'
    
    run_generation(LOCAL_AUDIO, LOCAL_PROMPTS)
    run_feature_extraction(LOCAL_AUDIO)