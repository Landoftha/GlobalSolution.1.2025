import folium
from typing import List, Dict
from shapely.geometry import mapping
from src.models.zone import Zone
from src.models.resource import Resource

class DamageMap:
    def __init__(self):
        self.map = None
        self.colors = {
            0: '#00ff00',  # Sem dano
            1: '#ffff00',  # Dano leve
            2: '#ffa500',  # Dano moderado
            3: '#ff4500',  # Dano severo
            4: '#800000'   # Destruição total
        }

    def create_map(self, zones: List[Zone], resources: List[Resource], center: List[float] = None) -> folium.Map:
        if not zones:
            return None

        # Calcular centro se não fornecido
        if not center:
            center = self._calculate_center(zones)

        # Criar mapa base
        self.map = folium.Map(
            location=center,
            zoom_start=8,
            tiles='CartoDB positron'
        )

        # Adicionar camada de municípios
        folium.TileLayer(
            'CartoDB positron',
            name='Mapa Base'
        ).add_to(self.map)

        # Adicionar zonas
        for zone in zones:
            self._add_zone(zone)

        # Adicionar recursos
        for resource in resources:
            self._add_resource(resource)

        # Adicionar controle de camadas
        folium.LayerControl().add_to(self.map)

        return self.map

    def _calculate_center(self, zones: List[Zone]) -> List[float]:
        if not zones:
            return [-19.9167, -44.1667]  # Coordenadas de Brumadinho

        # Calcular centroide de todas as zonas
        total_lat = 0
        total_lon = 0
        count = 0

        for zone in zones:
            centroid = zone.geometry.centroid
            total_lat += centroid.y
            total_lon += centroid.x
            count += 1

        return [total_lat / count, total_lon / count]

    def _add_zone(self, zone: Zone) -> None:
        if not self.map:
            return

        # Converter geometria para GeoJSON
        geojson = mapping(zone.geometry)

        # Criar conteúdo do popup
        popup_content = f"""
        <b>{zone.name}</b><br>
        Nível de Dano: {zone.damage_level}<br>
        População: {zone.population:,}<br>
        Pontuação de Prioridade: {zone.priority_score:.2f}<br>
        Recursos Alocados: {len(zone.resources_allocated)}
        """

        # Adicionar zona ao mapa
        folium.GeoJson(
            geojson,
            style_function=lambda x: {
                'fillColor': self.colors.get(int(zone.damage_level), '#808080'),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            popup=folium.Popup(popup_content, max_width=300),
            name=f"Zona: {zone.name}"
        ).add_to(self.map)

    def _add_resource(self, resource: Resource) -> None:
        if not self.map:
            return

        # Definir ícones por tipo de recurso
        icon_map = {
            'Ambulância': 'ambulance',
            'Equipe de Resgate': 'user-md',
            'Hospitais de Campanha': 'hospital',
            'Equipe de Engenharia': 'wrench',
            'Equipe de Suporte': 'users',
            'Veículos de Transporte': 'truck',
            'Equipe de Defesa Civil': 'shield'
        }

        # Criar conteúdo do popup
        popup_content = f"""
        <b>Recurso {resource.id}</b><br>
        Tipo: {resource.type}<br>
        Capacidade: {resource.capacity}<br>
        Zonas Atendidas: {len(resource.assigned_zones)}
        """

        # Adicionar marcador de recurso
        folium.Marker(
            location=[resource.location.y, resource.location.x],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(
                color='red',
                icon=icon_map.get(resource.type, 'info-sign'),
                prefix='fa'
            ),
            name=f"Recurso: {resource.type} {resource.id}"
        ).add_to(self.map) 