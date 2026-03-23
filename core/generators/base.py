from abc import ABC, abstractmethod
import base64, os

class MusicGenerator(ABC):

    # if you wajt to add more models, just make a new adapter file and inherit this method
    @abstractmethod
    def generate(self, prompt, out_path, **kwargs):
        pass