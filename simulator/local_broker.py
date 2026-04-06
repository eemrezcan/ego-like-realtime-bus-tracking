from __future__ import annotations

import argparse
import asyncio
import logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Venv icinde calisan lokal MQTT broker."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Broker bind adresi.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=1883,
        help="Broker bind portu.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Daha ayrintili broker loglari ac.",
    )
    return parser


async def run_broker(host: str, port: int) -> None:
    from amqtt.broker import Broker

    config = {
        "listeners": {
            "default": {
                "type": "tcp",
                "bind": f"{host}:{port}",
            }
        },
        "plugins": {
            "amqtt.plugins.authentication.AnonymousAuthPlugin": {
                "allow_anonymous": True
            },
            "amqtt.plugins.sys.broker.BrokerSysPlugin": {"sys_interval": 20},
        },
    }

    broker = Broker(config)
    await broker.start()
    print(f"Lokal MQTT broker calisiyor: mqtt://{host}:{port}")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await broker.shutdown()
        raise


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    )

    try:
        asyncio.run(run_broker(args.host, args.port))
    except KeyboardInterrupt:
        print("Broker kapatildi.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

