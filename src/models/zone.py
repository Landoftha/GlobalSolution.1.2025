from dataclasses import dataclass
from typing import List, Optional
from shapely.geometry import Polygon

@dataclass
class Zone:
    id: str
    name: str
    geometry: Polygon
    population: int
    damage_level: float
    infrastructure_damage: float = 0.0
    accessibility: float = 0.0
    critical_facilities: int = 0
    historical_risk: float = 0.0
    priority_score: float = 0.0
    resources_allocated: List[str] = None

    def __post_init__(self):
        if self.resources_allocated is None:
            self.resources_allocated = []

    def calculate_priority(self, damage_weight: float = 0.6, population_weight: float = 0.4) -> float:
        normalized_damage = self.damage_level / 4.0
        normalized_population = min(self.population / 10000, 1.0)
        
        self.priority_score = (
            damage_weight * normalized_damage +
            population_weight * normalized_population
        )
        return self.priority_score

    def add_resource(self, resource_id: str) -> None:
        if resource_id not in self.resources_allocated:
            self.resources_allocated.append(resource_id)

    def remove_resource(self, resource_id: str) -> None:
        if resource_id in self.resources_allocated:
            self.resources_allocated.remove(resource_id) 