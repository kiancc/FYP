from core.feature_extraction.bpm import extract_bpm_librosa, extract_bpm_essentia
from core.feature_extraction.key_scale import extract_essentia_key_scale
from core.feature_extraction.pipeline import FeaturePipeline

PIPELINE = FeaturePipeline([extract_bpm_librosa, extract_bpm_essentia, extract_essentia_key_scale])