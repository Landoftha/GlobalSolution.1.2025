import geopandas as gpd
import fiona
import random
from typing import Tuple, List
from shapely.geometry import Point, Polygon
from src.models.zone import Zone
from src.models.resource import Resource

def load_data() -> Tuple[List[Zone], List[Resource]]:
    """
    Carrega dados simulados otimizados para o sistema.
    
    Returns:
        Tupla contendo lista de zonas e lista de recursos
    """
    # Criar zonas de exemplo
    zones = []
    for i in range(1, 11):
        lat = random.uniform(-23.5, -23.6)
        lon = random.uniform(-46.6, -46.7)
        point = Point(lon, lat)
        polygon = point.buffer(0.01)  # Criar um polígono ao redor do ponto
        
        zone = Zone(
            id=f"zone_{i}",
            name=f"Zona {i}",
            geometry=polygon,
            population=random.randint(1000, 10000),
            damage_level=random.uniform(0, 1),
            infrastructure_damage=random.uniform(0, 1),
            accessibility=random.uniform(0, 1),
            critical_facilities=random.randint(0, 5),
            historical_risk=random.uniform(0, 1)
        )
        zone.calculate_priority()
        zones.append(zone)

    # Criar recursos de exemplo
    resources = []
    resource_types = ["Ambulância", "Bombeiros", "Equipe Médica", "Equipamento de Resgate"]
    
    for i in range(1, 6):
        resource_type = random.choice(resource_types)
        resource = Resource(
            id=f"resource_{i}",
            name=f"{resource_type} {i}",
            type=resource_type,
            capacity=random.randint(1, 5),
            location=Point(
                random.uniform(-46.7, -46.6),
                random.uniform(-23.6, -23.5)
            )
        )
        resources.append(resource)

    return zones, resources

def create_sample_resources() -> List[Resource]:
    """
    Cria recursos simulados otimizados para o sistema.
    
    Returns:
        Lista de recursos simulados
    """
    # Definição de recursos com capacidades balanceadas
    resource_definitions = [
        {
            "type": "Ambulância",
            "capacity": 5,
            "count": 10,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Equipe de Resgate",
            "capacity": 10,
            "count": 5,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Hospitais de Campanha",
            "capacity": 100,
            "count": 2,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Equipe de Engenharia",
            "capacity": 20,
            "count": 3,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Equipe de Suporte",
            "capacity": 30,
            "count": 4,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Veículos de Transporte",
            "capacity": 25,
            "count": 6,
            "location": Point(-44.1667, -19.9167)
        },
        {
            "type": "Equipe de Defesa Civil",
            "capacity": 15,
            "count": 4,
            "location": Point(-44.1667, -19.9167)
        }
    ]
    
    resources = []
    resource_id = 1
    
    for definition in resource_definitions:
        for i in range(definition["count"]):
            resource = Resource(
                id=f"R{resource_id}",
                type=definition["type"],
                capacity=definition["capacity"],
                location=definition["location"]
            )
            resources.append(resource)
            resource_id += 1
    
    return resources 