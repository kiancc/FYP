from core.feature_extraction.bpm import BpmLibrosaExtractor, BpmEssentiaExtractor
from core.feature_extraction.key_scale import KeyScaleExtractor
from core.feature_extraction.pipeline import FeaturePipeline

PIPELINE = FeaturePipeline([
    BpmLibrosaExtractor(),
    BpmEssentiaExtractor(),
    KeyScaleExtractor(),
])