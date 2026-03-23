from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from config.api_config import ELEVEN_LABS_API_KEY

client = ElevenLabs(
    api_key=ELEVEN_LABS_API_KEY
)

audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)