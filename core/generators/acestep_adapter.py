import os, time, json, datetime
import pandas as pd
from acestep.pipeline_ace_step import ACEStepPipeline
from core.generators.base import MusicGenerator

csv_path = "/content/master_prompts_v2.csv"   # path to your CSV in Colab
checkpoint_dir = None                         # None => auto-download to cache, or "/path/to/checkpoints"
outputs_dir = "/content/drive/MyDrive/AceStep_Output"
audio_duration = 180.0                         # seconds (default)
infer_steps = 360
guidance_scale = 15.0
device_id = 0
torch_compile = False
cpu_offload = False

class AceStepAdapter(MusicGenerator):

    def __init__(self):
        self.model_name = 'AceStep-1.5'
        self.model = ACEStepPipeline(
            checkpoint_dir=checkpoint_dir,
            device_id=device_id,
            dtype="bfloat16",
            torch_compile=torch_compile,
            cpu_offload=cpu_offload
        )

    def generate(self, prompt):
        return audio_bytes