from __future__ import annotations

import argparse
import time

from .allegro_client import AllegroClient
from .config import Settings
from .flexi_client import FlexiClient
from .state import StateStore
from .sync_service import SyncService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize Allegro seller account movements to Flexi"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run single synchronization and exit",
    )
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=60,
        help="Polling interval for continuous mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.from_env()

    state = StateStore(settings.sqlite_path)
    service = SyncService(
        allegro=AllegroClient(settings),
        flexi=FlexiClient(settings),
        state=state,
    )

    try:
        if args.once:
            count = service.sync_once()
            print(f"Synced {count} movement(s).")
            return

        while True:
            count = service.sync_once()
            print(f"Synced {count} movement(s).")
            time.sleep(args.interval_seconds)
    finally:
        state.close()


if __name__ == "__main__":
    main()
