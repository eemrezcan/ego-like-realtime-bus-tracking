from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .data_loader import load_catalog
from .engine import SimulationEngine
from .publisher import build_publisher


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sentetik otobus simulatoru ve telemetri event ureticisi."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
        help="lines.json, stops.json ve routes.json dosyalarini iceren klasor.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=5,
        help="Kac iterasyon veri uretilecegi.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=3,
        help="Iterasyonlar arasi simule edilen sure.",
    )
    parser.add_argument(
        "--buses-per-line",
        type=int,
        default=3,
        help="Her hat icin kac otobus uretilecegi.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Deterministik simulasyon icin rastgelelik tohumu.",
    )
    parser.add_argument(
        "--topic",
        default="ego-sim/v1/bus/telemetry",
        help="Uretilecek MQTT topic degeri.",
    )
    parser.add_argument(
        "--output",
        choices=("stdout", "file", "mqtt"),
        default="stdout",
        help="Uretilen eventlerin nereye gidecegi.",
    )
    parser.add_argument(
        "--file-path",
        type=Path,
        help="output=file iken kullanilacak jsonl dosya yolu.",
    )
    parser.add_argument(
        "--broker-host",
        help="output=mqtt iken kullanilacak broker host.",
    )
    parser.add_argument(
        "--broker-port",
        type=int,
        default=1883,
        help="output=mqtt iken kullanilacak broker port.",
    )
    parser.add_argument(
        "--client-id",
        default="ego-sim-local",
        help="output=mqtt iken kullanilacak MQTT client id.",
    )
    parser.add_argument(
        "--mqtt-username",
        help="MQTT broker kullanici adi. Gerekliyse verilir.",
    )
    parser.add_argument(
        "--mqtt-password",
        help="MQTT broker sifresi. Gerekliyse verilir.",
    )
    parser.add_argument(
        "--tls",
        action="store_true",
        help="MQTT baglantisini TLS ile kur.",
    )
    parser.add_argument(
        "--ca-file",
        type=Path,
        help="TLS icin CA sertifikasi yolu.",
    )
    parser.add_argument(
        "--cert-file",
        type=Path,
        help="TLS icin istemci sertifikasi yolu.",
    )
    parser.add_argument(
        "--key-file",
        type=Path,
        help="TLS icin istemci private key yolu.",
    )
    parser.add_argument(
        "--no-sleep",
        action="store_true",
        help="Lokal testte iterasyonlar arasinda bekleme yapma.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    catalog = load_catalog(args.data_dir)
    engine = SimulationEngine(
        catalog=catalog,
        buses_per_line=args.buses_per_line,
        seed=args.seed,
    )
    publisher = build_publisher(
        output_mode=args.output,
        file_path=args.file_path,
        broker_host=args.broker_host,
        broker_port=args.broker_port,
        client_id=args.client_id,
        mqtt_username=args.mqtt_username,
        mqtt_password=args.mqtt_password,
        use_tls=args.tls,
        ca_file=args.ca_file,
        cert_file=args.cert_file,
        key_file=args.key_file,
    )

    print(
        (
            f"Simulator basladi: {len(engine.buses)} otobus, "
            f"{args.steps} adim, {args.interval_seconds}s aralik, "
            f"output={args.output}"
        ),
        file=sys.stderr,
    )

    simulated_time = datetime.now(timezone.utc)

    try:
        for step_index in range(args.steps):
            simulated_time += timedelta(seconds=args.interval_seconds)
            events = engine.step(
                observed_at=simulated_time,
                interval_seconds=args.interval_seconds,
            )
            for payload in events:
                publisher.publish(args.topic, payload)
            print(
                f"Adim {step_index + 1}/{args.steps}: {len(events)} event uretildi.",
                file=sys.stderr,
            )
            if not args.no_sleep and step_index < args.steps - 1:
                time.sleep(args.interval_seconds)
    finally:
        publisher.close()

    return 0
