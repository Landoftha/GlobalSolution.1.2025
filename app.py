import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import fiona
from src.models.zone import Zone
from src.models.resource import Resource
from src.models.allocation import ResourceAllocator
from src.visualization.map import DamageMap
from src.visualization.dashboard import Dashboard

def load_data():
    # Load municipality boundaries using fiona
    fiona.drvsupport.supported_drivers['KML'] = 'rw'
    
    try:
        # Read the first layer which contains municipality data
        municipalities = gpd.read_file(
            "Cadastro_e_Trajetos_Municipios_Afetados_MG/doc.kml",
            driver='KML',
            layer='Cadastro_Enderecos_Censo2010'
        )
        
        # Display the columns to help debug
        # st.write("Available columns:", municipalities.columns.tolist())
        
        # Limit to first 10 features
        municipalities = municipalities.head(10)
        
        # Create zones from municipalities
        zones = []
        for idx, row in municipalities.iterrows():
            # Use 'Name' instead of 'name' as it's the standard KML field
            zone_name = row.get('Name', f'Zone {idx}')
            
            zone = Zone(
                id=str(idx),
                name=zone_name,
                geometry=row['geometry'],
                population=1000,  # Placeholder - should be replaced with real data
                damage_level=2.0  # Placeholder - should be replaced with real data
            )
            zone.calculate_priority()
            zones.append(zone)

        
    except Exception as e:
        st.error(f"Erro ao carregar arquivo KML: {str(e)}")
        # Fallback: create sample data
        municipalities = gpd.GeoDataFrame({
            'Name': ['Brumadinho', 'Belo Horizonte', 'Betim'],
            'geometry': [
                Point(-44.1667, -19.9167).buffer(0.1),
                Point(-43.9388, -19.9167).buffer(0.1),
                Point(-44.1984, -19.9678).buffer(0.1)
            ]
        })
        
        # Create zones from sample data
        zones = []
        for idx, row in municipalities.iterrows():
            zone = Zone(
                id=str(idx),
                name=row['Name'],
                geometry=row['geometry'],
                population=1000,
                damage_level=2.0
            )
            zone.calculate_priority()
            zones.append(zone)
    
    # Create sample resources
    resources = []
    resource_types = ['Ambulância', 'Equipe de Resgate', 'Hospitais de Campanha']
    
    for i in range(10):
        resource = Resource(
            id=f"R{i+1}",
            type=resource_types[i % len(resource_types)],
            capacity=3.0,
            location=Point(-44.1667 + (i * 0.1), -19.9167 + (i * 0.1))
        )
        resources.append(resource)
    
    return zones, resources

def main():
    st.set_page_config(page_title="Sistema de Avaliação Rápida de Danos", layout="wide")
    
    # Initialize components
    dashboard = Dashboard()
    damage_map = DamageMap()
    resource_allocator = ResourceAllocator()
    
    # Load data
    zones, resources = load_data()
    
    # Update metrics
    dashboard.update_metrics(zones, resources)
    
    # Display dashboard
    dashboard.display_metrics()
    
    # Create two columns for map and charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create and display map
        if len(zones) < 500:
            m = damage_map.create_map(zones, resources)
            if m:
                st.components.v1.html(m._repr_html_(), height=600)
        else:
            st.warning("Too many zones to display on the map. Please filter or aggregate your data.")
    
    with col2:
        # Display charts
        dashboard.display_damage_distribution(zones)
        dashboard.display_resource_allocation(resources)
    
    # Add resource allocation controls
    st.sidebar.title("Controles de Alocação")
    
    if st.sidebar.button("Realocar Recursos"):
        allocation_plan = resource_allocator.allocate_resources(zones, resources)
        st.sidebar.success("Recursos realocados com sucesso!")
        
        # Update metrics and display
        dashboard.update_metrics(zones, resources)
        st.rerun()

if __name__ == "__main__":
    main() 