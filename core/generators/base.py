from abc import ABC, abstractmethod
import base64, os

class MusicGenerator(ABC):

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Returns base64-encoded audio bytes."""
        pass

    def save(self, audio_b64: str, out_path: str) -> None:
        """Decodes base64 audio and writes to disk."""
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(audio_b64))