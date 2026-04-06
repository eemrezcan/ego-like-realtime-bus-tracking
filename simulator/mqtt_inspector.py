from __future__ import annotations

import argparse
import json
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lokal MQTT akisini terminalden izlemek icin basit inspector."
    )
    parser.add_argument(
        "--broker-host",
        default="localhost",
        help="Baglanilacak MQTT broker host degeri.",
    )
    parser.add_argument(
        "--broker-port",
        type=int,
        default=1883,
        help="Baglanilacak MQTT broker port degeri.",
    )
    parser.add_argument(
        "--topic",
        default="ego-sim/v1/bus/telemetry",
        help="Abone olunacak topic.",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=0,
        help="0 ise sinirsiz dinler, aksi halde belirtilen adet mesaji alip cikar.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise RuntimeError(
            "MQTT inspector icin paho-mqtt paketinin kurulu olmasi gerekiyor."
        ) from exc

    state = {"count": 0}

    def on_connect(client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any) -> None:
        print(
            f"Broker baglantisi kuruldu: host={args.broker_host} port={args.broker_port} topic={args.topic}"
        )
        client.subscribe(args.topic)

    def on_message(client: mqtt.Client, _userdata: Any, message: mqtt.MQTTMessage) -> None:
        state["count"] += 1
        raw_payload = message.payload.decode("utf-8")
        try:
            decoded = json.loads(raw_payload)
            rendered = json.dumps(decoded, indent=2, ensure_ascii=True)
        except json.JSONDecodeError:
            rendered = raw_payload

        print(f"\n[{state['count']}] topic={message.topic}")
        print(rendered)

        if args.max_messages and state["count"] >= args.max_messages:
            client.disconnect()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.broker_host, args.broker_port, keepalive=60)
    client.loop_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

