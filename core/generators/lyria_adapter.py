import base64
import google.auth
import google.auth.transport.requests
import logging
import requests

from core.generators.base import MusicGenerator
from config.api_config import LYRIA_MODEL
from core.generators.utils import exponential_backoff_request

logger = logging.getLogger(__name__)

class LyriaAdapter(MusicGenerator):
    
    def __init__(self):
        self.model_name = 'Lyria-002'
        self.music_model = LYRIA_MODEL # model is limited to 30 seconds

    def generate(self, prompt):
        prediction = self.generate_music(
            {"prompt": prompt}
        )

        audio_bytes = dict(prediction[0])["bytesBase64Encoded"] # use to be called bytes_b64
        # decoded_audio_data = base64.b64decode(bytes_b64)
        return audio_bytes
    
    # --- START OF THIRD-PARTY CODE ---
    # The following code is adapted from: https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/audio/music/getting-started/lyria2_music_generation.ipynb
    #
    # Copyright 2025 Google LLC
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at:
    #     https://www.apache.org/licenses/LICENSE-2.0
    # ---------------------------------
    def send_request_to_google_api(self, api_endpoint, data=None):
        """
        Sends an HTTP request to a Google API endpoint.

        Args:
            api_endpoint: The URL of the Google API endpoint.
            data: (Optional) Dictionary of data to send in the request body (for POST, PUT, etc.).

        Returns:
            The response from the Google API.
        """

        # Get access token calling API
        creds, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        access_token = creds.token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(api_endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                logger.error("Google API 400: %s", e.response.text)
            return None

    def generate_music(self, request: dict):
        req = {"instances": [request], "parameters": {}}
        resp = self.send_request_to_google_api(self.music_model, req)
        if not resp:
            return None
        return resp["predictions"]

    # --- END OF THIRD-PARTY CODE ---
