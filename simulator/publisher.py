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
    def __init__(
        self,
        host: str,
        port: int,
        client_id: str,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool = False,
        ca_file: Path | None = None,
        cert_file: Path | None = None,
        key_file: Path | None = None,
    ) -> None:
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError(
                "MQTT output icin paho-mqtt paketinin kurulu olmasi gerekiyor."
            ) from exc

        self._client = mqtt.Client(client_id=client_id)
        if username:
            self._client.username_pw_set(username=username, password=password)
        if use_tls or ca_file or cert_file or key_file:
            self._client.tls_set(
                ca_certs=str(ca_file) if ca_file else None,
                certfile=str(cert_file) if cert_file else None,
                keyfile=str(key_file) if key_file else None,
            )
        self._client.connect(host, port, keepalive=60)
        self._client.loop_start()

    def publish(self, topic: str, payload: dict[str, object]) -> None:
        body = json.dumps(payload, separators=(",", ":"))
        result = self._client.publish(topic, body, qos=1)
        result.wait_for_publish()
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
    mqtt_username: str | None = None,
    mqtt_password: str | None = None,
    use_tls: bool = False,
    ca_file: Path | None = None,
    cert_file: Path | None = None,
    key_file: Path | None = None,
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
        return MqttPublisher(
            host=broker_host,
            port=broker_port,
            client_id=client_id,
            username=mqtt_username,
            password=mqtt_password,
            use_tls=use_tls,
            ca_file=ca_file,
            cert_file=cert_file,
            key_file=key_file,
        )

    raise ValueError(f"Desteklenmeyen output modu: {output_mode}")
