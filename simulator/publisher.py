from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol


class Publisher(Protocol):
    def publish(self, topic: str, payload: dict[str, object]) -> None:
        ...

    def close(self) -> None:
        ...


class StdoutPublisher:
    def publish(self, topic: str, payload: dict[str, object]) -> None:
        print(json.dumps({"topic": topic, "payload": payload}, separators=(",", ":")))

    def close(self) -> None:
        return None


class JsonlFilePublisher:
    def __init__(self, file_path: Path) -> None:
        self._path = file_path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self._path.open("w", encoding="utf-8")

    def publish(self, topic: str, payload: dict[str, object]) -> None:
        line = json.dumps({"topic": topic, "payload": payload}, separators=(",", ":"))
        self._handle.write(f"{line}\n")
        self._handle.flush()

    def close(self) -> None:
        self._handle.close()


class MqttPublisher:
    def __init__(self, host: str, port: int, client_id: str) -> None:
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError(
                "MQTT output icin paho-mqtt paketinin kurulu olmasi gerekiyor."
            ) from exc

        self._client = mqtt.Client(client_id=client_id)
        self._client.connect(host, port, keepalive=60)
        self._client.loop_start()

    def publish(self, topic: str, payload: dict[str, object]) -> None:
        body = json.dumps(payload, separators=(",", ":"))
        result = self._client.publish(topic, body, qos=0)
        if result.rc != 0:
            raise RuntimeError(f"MQTT publish basarisiz oldu. rc={result.rc}")

    def close(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()


def build_publisher(
    output_mode: str,
    file_path: Path | None = None,
    broker_host: str | None = None,
    broker_port: int = 1883,
    client_id: str = "ego-sim-local",
) -> Publisher:
    if output_mode == "stdout":
        return StdoutPublisher()
    if output_mode == "file":
        if file_path is None:
            raise ValueError("File output icin dosya yolu verilmelidir.")
        return JsonlFilePublisher(file_path)
    if output_mode == "mqtt":
        if broker_host is None:
            raise ValueError("MQTT output icin broker host verilmelidir.")
        return MqttPublisher(broker_host, broker_port, client_id)

    raise ValueError(f"Desteklenmeyen output modu: {output_mode}")
