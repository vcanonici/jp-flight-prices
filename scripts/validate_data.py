from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path

CSV_PATH = Path("data/flight_prices.csv")
EXPECTED_COLUMNS = [
    "checked_at",
    "origin",
    "destination",
    "trip_type",
    "price_eur",
    "outbound_date",
    "return_date",
    "airports",
    "stops",
    "airlines",
    "source",
    "source_url",
    "notes",
]
ALLOWED_ORIGINS = {"LIS", "OPO"}
ALLOWED_DESTINATIONS = {"Tokyo", "Osaka"}


def parse_iso_date(value: str, field: str, row_number: int) -> None:
    if not value:
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"row {row_number}: invalid {field}: {value}") from exc


def main() -> int:
    if not CSV_PATH.exists():
        print(f"missing file: {CSV_PATH}", file=sys.stderr)
        return 1

    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != EXPECTED_COLUMNS:
            print("invalid CSV schema", file=sys.stderr)
            print(f"expected: {EXPECTED_COLUMNS}", file=sys.stderr)
            print(f"actual:   {reader.fieldnames}", file=sys.stderr)
            return 1

        seen = set()
        rows = 0
        for row_number, row in enumerate(reader, start=2):
            rows += 1
            if row["origin"] not in ALLOWED_ORIGINS:
                raise ValueError(f"row {row_number}: invalid origin {row['origin']}")
            if row["destination"] not in ALLOWED_DESTINATIONS:
                raise ValueError(f"row {row_number}: invalid destination {row['destination']}")
            if row["trip_type"] != "round_trip":
                raise ValueError(f"row {row_number}: trip_type must be round_trip")

            try:
                price = float(row["price_eur"])
            except ValueError as exc:
                raise ValueError(f"row {row_number}: invalid price_eur") from exc
            if price <= 0:
                raise ValueError(f"row {row_number}: price_eur must be > 0")

            parse_iso_date(row["checked_at"], "checked_at", row_number)
            parse_iso_date(row["outbound_date"], "outbound_date", row_number)
            parse_iso_date(row["return_date"], "return_date", row_number)

            key = (
                row["checked_at"],
                row["origin"],
                row["destination"],
                row["price_eur"],
                row["source_url"],
            )
            if key in seen:
                raise ValueError(f"row {row_number}: duplicate observation")
            seen.add(key)

    print(f"OK: validated {rows} observations")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
