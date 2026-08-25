#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path

CSV_PATH = Path("data/flight_prices.csv")
README_PATH = Path("README.md")
START = "<!-- PRICE_HISTORY_START -->"
END = "<!-- PRICE_HISTORY_END -->"

ROUTES = [
    ("LIS", "Tokyo", "LIS → Tóquio"),
    ("OPO", "Tokyo", "OPO → Tóquio"),
    ("LIS", "Osaka", "LIS → Osaka"),
    ("OPO", "Osaka", "OPO → Osaka"),
]


def normalize_destination(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"tokyo", "tóquio", "tyo", "hnd", "nrt"}:
        return "Tokyo"
    if value in {"osaka", "osa", "kix"}:
        return "Osaka"
    return (value or "").strip()


def load_daily_minima():
    daily = defaultdict(dict)
    if not CSV_PATH.exists():
        return daily

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            day = (row.get("checked_at") or "").strip()[:10]
            origin = (row.get("origin") or "").strip().upper()
            destination = normalize_destination(row.get("destination") or "")
            raw_price = (row.get("price_eur") or "").strip()
            if not day or not raw_price:
                continue
            try:
                price = float(raw_price.replace(",", "."))
            except ValueError:
                continue
            key = (origin, destination)
            current = daily[day].get(key)
            if current is None or price < current:
                daily[day][key] = price
    return daily


def eur(value):
    if value is None:
        return "—"
    if float(value).is_integer():
        return f"€{int(value)}"
    return f"€{value:.2f}"


def render_history():
    daily = load_daily_minima()
    lines = [
        START,
        "## Histórico de preços",
        "",
        "Menor tarifa de ida e volta encontrada em cada execução diária.",
        "",
        "| Dia | LIS → Tóquio | OPO → Tóquio | LIS → Osaka | OPO → Osaka |",
        "|---|---:|---:|---:|---:|",
    ]

    if not daily:
        lines.append("| sem dados | — | — | — | — |")
    else:
        for day in sorted(daily.keys(), reverse=True):
            values = []
            for origin, destination, _ in ROUTES:
                values.append(eur(daily[day].get((origin, destination))))
            lines.append(f"| {day} | " + " | ".join(values) + " |")

    lines += ["", "_Gerado automaticamente a partir de `data/flight_prices.csv`._", END]
    return "\n".join(lines)


def main():
    readme = README_PATH.read_text(encoding="utf-8")
    block = render_history()

    if START in readme and END in readme:
        before = readme.split(START, 1)[0].rstrip()
        after = readme.split(END, 1)[1].lstrip("\n")
        output = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        output = readme.rstrip() + "\n\n" + block + "\n"

    README_PATH.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
