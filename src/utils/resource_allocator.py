from typing import List, Dict
from src.models.zone import Zone
from src.models.resource import Resource

class ResourceAllocator:
    def __init__(self):
        self.allocation_history = []

    def allocate_resources(self, zones: List[Zone], resources: List[Resource]) -> Dict[str, List[Resource]]:
        """
        Aloca recursos para zonas usando um algoritmo guloso baseado na pontuação de prioridade.
        
        Args:
            zones: Lista de zonas afetadas
            resources: Lista de recursos disponíveis
            
        Returns:
            Dicionário com a alocação de recursos por zona
        """
        # Ordenar zonas por prioridade (maior para menor)
        sorted_zones = sorted(zones, key=lambda x: x.priority_score, reverse=True)
        
        # Ordenar recursos por capacidade (maior para menor)
        sorted_resources = sorted(resources, key=lambda x: x.capacity, reverse=True)
        
        # Inicializar dicionário de alocação
        allocation = {zone.id: [] for zone in zones}
        
        # Alocar recursos para cada zona
        for zone in sorted_zones:
            remaining_capacity = zone.population  # Capacidade necessária baseada na população
            
            while remaining_capacity > 0 and sorted_resources:
                # Encontrar o melhor recurso disponível
                best_resource = None
                best_resource_index = -1
                
                for i, resource in enumerate(sorted_resources):
                    if resource.capacity <= remaining_capacity and not resource.assigned_zones:
                        best_resource = resource
                        best_resource_index = i
                        break
                
                if best_resource is None:
                    break
                
                # Alocar o recurso
                allocation[zone.id].append(best_resource)
                best_resource.assigned_zones.append(zone)
                zone.resources_allocated.append(best_resource)
                remaining_capacity -= best_resource.capacity
                
                # Remover recurso da lista de disponíveis
                sorted_resources.pop(best_resource_index)
                
                # Registrar alocação no histórico
                self.allocation_history.append({
                    'zone_id': zone.id,
                    'zone_name': zone.name,
                    'resource_id': best_resource.id,
                    'resource_type': best_resource.type,
                    'capacity_allocated': best_resource.capacity
                })
        
        return allocation

    def get_allocation_history(self) -> List[Dict]:
        """
        Retorna o histórico de alocações realizadas.
        
        Returns:
            Lista de dicionários com informações sobre cada alocação
        """
        return self.allocation_history

    def calculate_allocation_metrics(self, zones: List[Zone], resources: List[Resource]) -> Dict:
        """
        Calcula métricas sobre a alocação de recursos.
        
        Args:
            zones: Lista de zonas afetadas
            resources: Lista de recursos disponíveis
            
        Returns:
            Dicionário com métricas de alocação
        """
        total_resources = len(resources)
        allocated_resources = sum(1 for r in resources if r.assigned_zones)
        total_zones = len(zones)
        zones_with_resources = sum(1 for z in zones if z.resources_allocated)
        
        return {
            'total_resources': total_resources,
            'allocated_resources': allocated_resources,
            'allocation_rate': allocated_resources / total_resources if total_resources > 0 else 0,
            'total_zones': total_zones,
            'zones_with_resources': zones_with_resources,
            'coverage_rate': zones_with_resources / total_zones if total_zones > 0 else 0
        } 