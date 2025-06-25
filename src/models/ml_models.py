import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import networkx as nx
from typing import List, Dict, Tuple
from shapely.geometry import Point

class DisasterPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, zone_data: List[Dict]) -> np.ndarray:
        features = []
        for zone in zone_data:
            feature_vector = [
                zone.get('population', 0),
                zone.get('infrastructure_damage', 0),
                zone.get('accessibility', 0),
                zone.get('critical_facilities', 0),
                zone.get('historical_risk', 0)
            ]
            features.append(feature_vector)
        return np.array(features)

    def train(self, historical_data: List[Dict]):
        X = self.prepare_features(historical_data)
        y = np.array([zone.get('damage_level', 0) for zone in historical_data])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        return self.model.score(self.scaler.transform(X_test), y_test)

    def predict(self, zone_data: List[Dict]) -> List[float]:
        if not self.is_trained:
            raise ValueError("Model needs to be trained before making predictions")
        
        X = self.prepare_features(zone_data)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

class RouteOptimizer:
    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, zones: List[Dict], resources: List[Dict]):
        self.graph.clear()
        
        for zone in zones:
            # Extrair coordenadas do centro do polígono
            center = zone.geometry.centroid
            self.graph.add_node(zone.id, 
                              pos=(center.x, center.y),
                              demand=zone.population,
                              damage=zone.damage_level)
        
        for i, zone1 in enumerate(zones):
            for zone2 in zones[i+1:]:
                center1 = zone1.geometry.centroid
                center2 = zone2.geometry.centroid
                distance = self._calculate_distance(
                    (center1.x, center1.y),
                    (center2.x, center2.y)
                )
                self.graph.add_edge(zone1.id, zone2.id, weight=distance)

    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        x1, y1 = point1
        x2, y2 = point2
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def find_optimal_route(self, start_zone_id: str, target_zone_id: str) -> List[str]:
        try:
            path = nx.shortest_path(self.graph, 
                                  source=start_zone_id,
                                  target=target_zone_id,
                                  weight='weight')
            return path
        except nx.NetworkXNoPath:
            return []

    def get_resource_allocation_route(self, 
                                    resource_location: str,
                                    target_zones: List[str]) -> List[str]:
        if not target_zones:
            return []
            
        current = resource_location
        route = [current]
        remaining = set(target_zones)
        
        while remaining:
            next_zone = min(remaining,
                          key=lambda x: self.graph[current][x]['weight'])
            route.append(next_zone)
            current = next_zone
            remaining.remove(next_zone)
            
        return route 