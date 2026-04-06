from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import EventProcessor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ham telemetri eventlerini lokalde zenginlestirmek icin yardimci arac."
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        required=True,
        help="Tek JSON veya JSONL dosyasi. Simulator output wrapper'i varsa payload otomatik ayiklanir.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
        help="Hat, durak ve rota veri klasoru.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        help="Verilirse zenginlestirilmis eventleri JSONL dosyasina yazar.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    processor = EventProcessor(data_dir=args.data_dir)
    events = _load_events(args.input_file)
    output_handle = None

    if args.output_file is not None:
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        output_handle = args.output_file.open("w", encoding="utf-8")

    try:
        for item in events:
            enriched = processor.process_payload(item)
            rendered = json.dumps(enriched, ensure_ascii=True)
            print(rendered)
            if output_handle is not None:
                output_handle.write(f"{rendered}\n")
    finally:
        if output_handle is not None:
            output_handle.close()

    return 0


def _load_events(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if path.suffix.lower() == ".json":
        parsed = json.loads(text)
        return _normalize_loaded_json(parsed)

    events: list[dict[str, object]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        events.extend(_normalize_loaded_json(json.loads(line)))
    return events


def _normalize_loaded_json(parsed: object) -> list[dict[str, object]]:
    if isinstance(parsed, list):
        result: list[dict[str, object]] = []
        for item in parsed:
            result.extend(_normalize_loaded_json(item))
        return result

    if not isinstance(parsed, dict):
        raise ValueError("Input JSON dict veya liste olmali.")

    if "payload" in parsed and isinstance(parsed["payload"], dict):
        return [parsed["payload"]]

    return [parsed]
