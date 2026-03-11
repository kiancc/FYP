import pandas as pd
import json
import os

def convert_csv_to_config(csv_path, output_json_path):
    df = pd.read_csv(csv_path)
    
    input_columns = ['id', 'genre', 'task', 'target', 'prompt', 'filename']
    clean_df = df[input_columns]
    
    config_data = {
        "experiment_metadata": {
            "version": "1.0",
            "description": "Benchmark prompts for AI Music Evaluation",
        },
        "prompts": clean_df.to_dict('records')
    }
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    with open(output_json_path, 'w') as f:
        json.dump(config_data, f, indent=4)
    
    print(f"Successfully created: {output_json_path}")

convert_csv_to_config('master_prompts_v2.csv', 'prompts.json')