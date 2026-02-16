from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    allegro_base_url: str
    allegro_access_token: str
    allegro_account_id: str | None
    flexi_base_url: str
    flexi_api_key: str
    flexi_movements_path: str
    sqlite_path: str
    sync_batch_size: int
    sync_lookback_hours: int

    @staticmethod
    def from_env() -> "Settings":
        allegro_access_token = os.getenv("ALLEGRO_ACCESS_TOKEN")
        flexi_base_url = os.getenv("FLEXI_BASE_URL")
        flexi_api_key = os.getenv("FLEXI_API_KEY")

        missing = [
            name
            for name, value in [
                ("ALLEGRO_ACCESS_TOKEN", allegro_access_token),
                ("FLEXI_BASE_URL", flexi_base_url),
                ("FLEXI_API_KEY", flexi_api_key),
            ]
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return Settings(
            allegro_base_url=os.getenv("ALLEGRO_BASE_URL", "https://api.allegro.pl").rstrip("/"),
            allegro_access_token=allegro_access_token,
            allegro_account_id=os.getenv("ALLEGRO_ACCOUNT_ID"),
            flexi_base_url=flexi_base_url.rstrip("/"),
            flexi_api_key=flexi_api_key,
            flexi_movements_path=os.getenv("FLEXI_MOVEMENTS_PATH", "/api/movements"),
            sqlite_path=os.getenv("SQLITE_PATH", "./connector_state.db"),
            sync_batch_size=int(os.getenv("SYNC_BATCH_SIZE", "100")),
            sync_lookback_hours=int(os.getenv("SYNC_LOOKBACK_HOURS", "24")),
        )
