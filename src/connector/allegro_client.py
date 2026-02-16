from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .config import Settings
from .state import Cursor


class AllegroClient:
    def __init__(self, settings: Settings):
        self._settings = settings

    def fetch_movements(self, cursor: Cursor | None) -> list[dict]:
        if cursor:
            from_ts = cursor.occurred_at
        else:
            from_ts = (
                datetime.now(timezone.utc) - timedelta(hours=self._settings.sync_lookback_hours)
            ).isoformat()

        params = {
            "limit": self._settings.sync_batch_size,
            "occurredAt.gte": from_ts,
            "sort": "occurredAt",
        }
        if self._settings.allegro_account_id:
            params["account.id"] = self._settings.allegro_account_id

        url = f"{self._settings.allegro_base_url}/billing/balance?{urlencode(params)}"
        req = Request(
            url=url,
            method="GET",
            headers={
                "Authorization": f"Bearer {self._settings.allegro_access_token}",
                "Accept": "application/vnd.allegro.public.v1+json",
            },
        )
        with urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload.get("balanceOperations", [])
