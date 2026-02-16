from __future__ import annotations


class MovementMapper:
    """Maps Allegro movement object into the expected Flexi movement payload."""

    @staticmethod
    def to_flexi_payload(movement: dict) -> dict:
        # Adjust this payload to your exact Flexi API schema if needed.
        value = movement.get("value", {})
        return {
            "externalId": movement.get("id"),
            "source": "allegro",
            "occurredAt": movement.get("occurredAt"),
            "type": movement.get("type"),
            "group": movement.get("group"),
            "marketplace": movement.get("marketplace", {}).get("id"),
            "value": {
                "amount": value.get("amount"),
                "currency": value.get("currency"),
            },
            "details": movement,
        }
