from __future__ import annotations

import math


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def estimate_eta_seconds(
    distance_remaining_km: float,
    current_speed_kmh: float,
    planned_remaining_seconds: int,
) -> int:
    if distance_remaining_km <= 0.03:
        return max(15, min(planned_remaining_seconds, 30))

    if current_speed_kmh >= 8:
        speed_based_seconds = int(math.ceil((distance_remaining_km / current_speed_kmh) * 3600))
        return max(20, min(speed_based_seconds, int(planned_remaining_seconds * 2.5)))

    return max(35, planned_remaining_seconds)


def estimate_planned_remaining_seconds(
    distance_remaining_km: float,
    segment_distance_km: float,
    segment_planned_seconds: int,
) -> int:
    if segment_distance_km <= 0:
        return segment_planned_seconds

    ratio = max(0.05, min(1.0, distance_remaining_km / segment_distance_km))
    return max(20, int(math.ceil(segment_planned_seconds * ratio)))

