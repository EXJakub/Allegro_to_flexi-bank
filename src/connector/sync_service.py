from __future__ import annotations

from .allegro_client import AllegroClient
from .flexi_client import FlexiClient
from .mapping import MovementMapper
from .state import StateStore


class SyncService:
    def __init__(self, allegro: AllegroClient, flexi: FlexiClient, state: StateStore):
        self._allegro = allegro
        self._flexi = flexi
        self._state = state

    def sync_once(self) -> int:
        cursor = self._state.get_cursor()
        movements = self._allegro.fetch_movements(cursor)

        processed_count = 0
        sorted_movements = sorted(
            movements,
            key=lambda movement: (movement.get("occurredAt", ""), movement.get("id", "")),
        )

        for movement in sorted_movements:
            movement_id = movement.get("id")
            occurred_at = movement.get("occurredAt")
            if not movement_id or not occurred_at:
                continue
            if self._state.was_processed(movement_id):
                self._state.save_cursor(occurred_at, movement_id)
                continue

            payload = MovementMapper.to_flexi_payload(movement)
            self._flexi.create_movement(payload)
            self._state.mark_processed(movement_id, occurred_at)
            self._state.save_cursor(occurred_at, movement_id)
            processed_count += 1

        return processed_count
