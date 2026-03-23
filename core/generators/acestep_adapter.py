from acestep.pipeline_ace_step import ACEStepPipeline
from core.generators.base import MusicGenerator

csv_path = "/content/master_prompts_v2.csv"   # path to your CSV in Colab
checkpoint_dir = None                         # None => auto-download to cache, or "/path/to/checkpoints"
outputs_dir = "/content/drive/MyDrive/AceStep_Output"

class AceStepAdapter(MusicGenerator):

    def __init__(self):
        self.model_name = 'AceStep-1.5'
        self.audio_duration = 180.0 # find reference on best duration window from docs, max is 180
        self.infer_steps = 360
        self.guidance_scale = 15.0
        self.device_id = 0
        self.torch_compile = False
        self.cpu_offload = False
        self.model = ACEStepPipeline(
            checkpoint_dir=checkpoint_dir,
            device_id=self.device_id,
            dtype="bfloat16",
            torch_compile=self.torch_compile,
            cpu_offload=self.cpu_offload
        )

    def generate(self, prompt, out_path):
        return self.model(
            audio_duration=float(self.audio_duration),
            prompt=prompt,
            lyrics='[Instrumental]',
            infer_step=int(self.infer_steps),
            guidance_scale=float(self.guidance_scale),
            save_path=out_path
        )
        