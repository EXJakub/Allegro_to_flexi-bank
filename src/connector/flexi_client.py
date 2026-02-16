from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .config import Settings


class FlexiClient:
    def __init__(self, settings: Settings):
        self._settings = settings

    def create_movement(self, payload: dict) -> None:
        url = f"{self._settings.flexi_base_url}{self._settings.flexi_movements_path}"
        req = Request(
            url=url,
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-API-Key": self._settings.flexi_api_key,
            },
        )
        with urlopen(req, timeout=30):
            return
