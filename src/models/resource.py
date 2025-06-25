from dataclasses import dataclass
from typing import List, Optional
from shapely.geometry import Point

@dataclass
class Resource:
    id: str
    name: str
    type: str
    capacity: int
    location: Point
    assigned_zones: List[str] = None
    is_available: bool = True

    def __post_init__(self):
        if self.assigned_zones is None:
            self.assigned_zones = []

    def assign_to_zone(self, zone_id: str) -> bool:
        if self.is_available and zone_id not in self.assigned_zones:
            self.assigned_zones.append(zone_id)
            return True
        return False

    def remove_from_zone(self, zone_id: str) -> bool:
        if zone_id in self.assigned_zones:
            self.assigned_zones.remove(zone_id)
            return True
        return False

    def get_remaining_capacity(self) -> float:
        return self.capacity - len(self.assigned_zones)

    def is_fully_allocated(self) -> bool:
        return len(self.assigned_zones) >= self.capacity 