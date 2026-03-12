import pandas as pd
import json
import os

def convert_csv_to_config(csv_path, output_json_path):
    df = pd.read_csv(csv_path)
    
    input_columns = ['id', 'genre', 'task', 'target', 'prompt', 'file_id']
    clean_df = df[input_columns]
    
    config_data = clean_df.to_dict('records')
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    with open(output_json_path, 'w') as f:
        json.dump(config_data, f, indent=4)
    
    print(f"Successfully created: {output_json_path}")

prompts_dir = os.path.dirname(os.path.abspath(__file__))

convert_csv_to_config(
    os.path.join(prompts_dir, 'master_prompts_v2.csv'),
    os.path.join(prompts_dir, 'prompts.json')
)