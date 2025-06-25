from typing import List, Dict
from .zone import Zone
from .resource import Resource

class ResourceAllocator:
    def __init__(self):
        self.allocation_history = []

    def allocate_resources(self, zones: List[Zone], resources: List[Resource]) -> Dict[str, List[str]]:
        allocation_plan = {}
        
        # Sort zones by priority score
        sorted_zones = sorted(zones, key=lambda x: x.priority_score, reverse=True)
        
        # Sort resources by capacity
        sorted_resources = sorted(resources, key=lambda x: x.capacity, reverse=True)
        
        for zone in sorted_zones:
            allocation_plan[zone.id] = []
            
            # Find available resources
            available_resources = [r for r in sorted_resources if not r.is_fully_allocated()]
            
            if not available_resources:
                continue
                
            # Assign resources to zone
            for resource in available_resources:
                if resource.assign_to_zone(zone.id):
                    zone.add_resource(resource.id)
                    allocation_plan[zone.id].append(resource.id)
                    
                    if resource.is_fully_allocated():
                        resource.is_available = False
                    
                    # Record allocation
                    self.allocation_history.append({
                        'zone_id': zone.id,
                        'resource_id': resource.id,
                        'priority_score': zone.priority_score
                    })
                    
                    if len(allocation_plan[zone.id]) >= 3:  # Limit resources per zone
                        break
        
        return allocation_plan

    def get_allocation_metrics(self) -> Dict:
        if not self.allocation_history:
            return {
                'total_allocations': 0,
                'average_priority': 0,
                'zones_covered': 0
            }
            
        return {
            'total_allocations': len(self.allocation_history),
            'average_priority': sum(h['priority_score'] for h in self.allocation_history) / len(self.allocation_history),
            'zones_covered': len(set(h['zone_id'] for h in self.allocation_history))
        } 