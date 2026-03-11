from abc import ABC, abstractmethod

class FeatureExtractor(ABC):

    @property
    @abstractmethod
    def feature_name(self) -> str:
        pass

    @abstractmethod
    def extract(self, audio, sr, file_idx: str) -> dict:
        """Returns a dict of features, must include 'file_idx'."""
        pass