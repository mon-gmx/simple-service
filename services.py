import logging
import uuid

import requests

log = logging.getLogger("app_logger")


def get_random(remote_url: str) -> dict:
    """Return a dictionary with the response of a downstream"""
    remote_data = str(uuid.uuid4())
    try:
        data = requests.get(f"{remote_url}")
        if data.status_code == 200:
            json_data = data.json()
            log.info(f"Received remote data: {json_data}")
            remote_data = json_data
    except (requests.HTTPError, Exception) as error:
        log.error(f"Request to downstream {remote_url} failed: {error}")
    return remote_data
