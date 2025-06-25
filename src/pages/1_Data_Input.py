import streamlit as st
from shapely.geometry import Point
from src.models.zone import Zone
from src.models.resource import Resource

st.set_page_config(page_title="Entrada de Dados - Salvus", layout="wide")

st.title("Entrada de Dados - Salvus")

# Dados pré-definidos para simulação
ZONE_DATA = {
    "Zona Central": {"lat": -19.9167, "lon": -44.1667, "pop": 50000, "damage": 4.0},
    "Zona Norte": {"lat": -19.9267, "lon": -44.1567, "pop": 35000, "damage": 3.0},
    "Zona Sul": {"lat": -19.9067, "lon": -44.1767, "pop": 25000, "damage": 2.0},
    "Zona Leste": {"lat": -19.9167, "lon": -44.1467, "pop": 40000, "damage": 3.5},
    "Zona Oeste": {"lat": -19.9167, "lon": -44.1867, "pop": 30000, "damage": 2.5}
}

RESOURCE_TYPES = {
    "Ambulância": {"capacity": 5, "count": 10},
    "Equipe de Resgate": {"capacity": 10, "count": 5},
    "Hospitais de Campanha": {"capacity": 100, "count": 2},
    "Equipe de Engenharia": {"capacity": 20, "count": 3},
    "Equipe de Suporte": {"capacity": 30, "count": 4},
    "Veículos de Transporte": {"capacity": 25, "count": 6},
    "Equipe de Defesa Civil": {"capacity": 15, "count": 4}
}

with st.form("disaster_data_form"):
    st.header("Informações do Desastre")
    
    col1, col2 = st.columns(2)
    with col1:
        disaster_type = st.selectbox(
            "Tipo de Desastre",
            ["Enchente", "Terremoto", "Furacão", "Incêndio Florestal", "Outro"],
            key="disaster_type"
        )
        disaster_date = st.date_input("Data do Desastre", format="DD/MM/YYYY", key="disaster_date")
    
    with col2:
        affected_area = st.number_input(
            "Área Total Afetada (km²)",
            min_value=0.0,
            value=50.0,
            key="affected_area"
        )
        estimated_population = st.number_input(
            "População Afetada Estimada",
            min_value=0,
            value=180000,
            key="estimated_population"
        )

    st.header("Informações das Zonas")
    
    # Seleção de zonas
    selected_zones = st.multiselect(
        "Selecione as Zonas Afetadas",
        options=list(ZONE_DATA.keys()),
        default=list(ZONE_DATA.keys())[:3],
        key="selected_zones"
    )
    
    zones = []
    for idx, zone_name in enumerate(selected_zones):
        with st.expander(f"Zona: {zone_name}"):
            col1, col2 = st.columns(2)
            with col1:
                population = st.number_input(
                    f"População {zone_name}",
                    min_value=0,
                    value=ZONE_DATA[zone_name]["pop"],
                    key=f"pop_{zone_name}"
                )
            with col2:
                damage_level = st.slider(
                    f"Nível de Dano {zone_name}",
                    0.0, 4.0, ZONE_DATA[zone_name]["damage"], 0.5,
                    key=f"damage_{zone_name}"
                )
            
            zone = Zone(
                id=str(idx),
                name=zone_name,
                geometry=Point(ZONE_DATA[zone_name]["lon"], ZONE_DATA[zone_name]["lat"]).buffer(0.05),
                population=population,
                damage_level=damage_level
            )
            zone.calculate_priority()
            zones.append(zone)

    st.header("Informações dos Recursos")
    
    # Seleção de recursos
    selected_resource_type = st.selectbox(
        "Tipo de Recurso",
        options=list(RESOURCE_TYPES.keys()),
        key="resource_type"
    )
    
    num_resources = st.number_input(
        "Número de Recursos",
        min_value=1,
        max_value=RESOURCE_TYPES[selected_resource_type]["count"],
        value=min(3, RESOURCE_TYPES[selected_resource_type]["count"]),
        key="num_resources"
    )
    
    resources = []
    for i in range(num_resources):
        with st.expander(f"Recurso {i+1}"):
            col1, col2 = st.columns(2)
            with col1:
                capacity = st.number_input(
                    f"Capacidade {i+1}",
                    min_value=1,
                    max_value=RESOURCE_TYPES[selected_resource_type]["capacity"] * 2,
                    value=RESOURCE_TYPES[selected_resource_type]["capacity"],
                    key=f"capacity_{i}"
                )
            with col2:
                base_lat = ZONE_DATA["Zona Central"]["lat"]
                base_lon = ZONE_DATA["Zona Central"]["lon"]
                lat = st.number_input(
                    f"Latitude do Recurso {i+1}",
                    -90.0, 90.0, base_lat,
                    key=f"lat_{i}"
                )
                lon = st.number_input(
                    f"Longitude do Recurso {i+1}",
                    -180.0, 180.0, base_lon,
                    key=f"lon_{i}"
                )
            
            resource = Resource(
                id=f"R{i+1}",
                type=selected_resource_type,
                capacity=capacity,
                location=Point(lon, lat)
            )
            resources.append(resource)

    submitted = st.form_submit_button("Enviar Dados")
    
    if submitted:
        if zones and resources:
            st.session_state.zones = zones
            st.session_state.resources = resources
            st.session_state.disaster_info = {
                "type": disaster_type,
                "date": disaster_date,
                "affected_area": affected_area,
                "estimated_population": estimated_population
            }
            st.success("Dados enviados com sucesso! Navegue até a página do Painel para visualizar a análise.")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.") 