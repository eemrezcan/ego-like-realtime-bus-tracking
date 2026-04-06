from __future__ import annotations


STOP_TYPE_ALIGHTING_RATIO = {
    "hub": 0.18,
    "transfer": 0.16,
    "terminal": 0.55,
    "business": 0.12,
    "residential": 0.09,
    "civic": 0.11,
    "education": 0.14,
    "university": 0.20,
    "campus": 0.24,
}


def estimate_alighting_count(
    previous_occupancy: int,
    boarding_count: int,
    stop_type: str,
    stop_position_index: int,
    total_stops: int,
) -> int:
    if previous_occupancy <= 0:
        return 0

    progress_ratio = stop_position_index / max(1, total_stops - 1)
    base_ratio = STOP_TYPE_ALIGHTING_RATIO.get(stop_type, 0.10)
    progress_factor = 0.65 + (progress_ratio * 0.9)

    estimated = previous_occupancy * base_ratio * progress_factor
    if stop_type in {"hub", "transfer"}:
        estimated += min(2, boarding_count)

    return min(previous_occupancy, max(0, int(round(estimated))))


def compute_occupancy_score(
    previous_occupancy: int,
    boarding_count: int,
    estimated_alighting_count: int,
    vehicle_capacity: int,
) -> int:
    raw_score = previous_occupancy + boarding_count - estimated_alighting_count
    return max(0, min(vehicle_capacity, raw_score))


def classify_occupancy_level(occupancy_score: int, vehicle_capacity: int) -> str:
    if vehicle_capacity <= 0:
        return "dusuk"

    ratio = occupancy_score / vehicle_capacity
    if ratio <= 0.35:
        return "dusuk"
    if ratio <= 0.70:
        return "orta"
    return "yuksek"

