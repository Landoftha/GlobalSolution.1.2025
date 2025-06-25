import streamlit as st
import plotly.express as px
from typing import List
from src.models.zone import Zone
from src.models.resource import Resource

class Dashboard:
    def __init__(self):
        self.metrics = {
            'total_zones': 0,
            'affected_zones': 0,
            'total_resources': 0,
            'allocated_resources': 0,
            'average_damage': 0.0,
            'total_population': 0
        }

    def update_metrics(self, zones: List[Zone], resources: List[Resource]) -> None:
        if not zones or not resources:
            return

        self.metrics['total_zones'] = len(zones)
        self.metrics['affected_zones'] = sum(1 for z in zones if z.damage_level > 0)
        self.metrics['total_resources'] = len(resources)
        self.metrics['allocated_resources'] = sum(1 for r in resources if getattr(r, 'assigned_zones', None))
        self.metrics['average_damage'] = sum(z.damage_level for z in zones) / len(zones)
        self.metrics['total_population'] = sum(z.population for z in zones)

    def display_metrics(self) -> None:
        st.title("Sistema de Avaliação Rápida de Danos")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Zonas", self.metrics['total_zones'])
            st.metric("Zonas Afetadas", self.metrics['affected_zones'])
        with col2:
            st.metric("Total de Recursos", self.metrics['total_resources'])
            st.metric("Recursos Alocados", self.metrics['allocated_resources'])
        with col3:
            st.metric("Dano Médio", f"{self.metrics['average_damage']:.2f}")
            st.metric("População Total", self.metrics['total_population'])

    def display_damage_distribution(self, zones: List[Zone]) -> None:
        if not zones:
            return
        damage_levels = [int(z.damage_level) for z in zones]
        damage_counts = {level: damage_levels.count(level) for level in range(5)}
        fig = px.bar(
            x=list(damage_counts.keys()),
            y=list(damage_counts.values()),
            labels={'x': 'Nível de Dano', 'y': 'Número de Zonas'},
            title='Distribuição de Níveis de Dano'
        )
        st.plotly_chart(fig)

    def display_resource_allocation(self, resources: List[Resource]) -> None:
        if not resources:
            return
        resource_types = {}
        for resource in resources:
            if resource.type not in resource_types:
                resource_types[resource.type] = {'total': 0, 'allocated': 0}
            resource_types[resource.type]['total'] += 1
            if getattr(resource, 'assigned_zones', None):
                resource_types[resource.type]['allocated'] += 1
        types = list(resource_types.keys())
        total = [resource_types[t]['total'] for t in types]
        allocated = [resource_types[t]['allocated'] for t in types]
        df = {
            "Tipo": types,
            "Total": total,
            "Alocados": allocated
        }
        fig = px.bar(
            df,
            x="Tipo",
            y=["Total", "Alocados"],
            barmode="group",
            title="Alocação de Recursos por Tipo"
        )
        st.plotly_chart(fig)

 