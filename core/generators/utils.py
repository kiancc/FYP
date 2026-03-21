import random
import time
import requests

def exponential_backoff_request(method, url, *, max_retries=3, backoff_factor=1, timeout=10, **kwargs):
    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)

            if response.status_code not in {400, 429, 500, 502, 503, 504}:
                return response

        except requests.RequestException:
            if attempt == max_retries:
                raise

        if attempt == max_retries:
            return response

        sleep_s = backoff_factor * (2 ** attempt) + random.uniform(0, 0.3)
        time.sleep(sleep_s)

    return response