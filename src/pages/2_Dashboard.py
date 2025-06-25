import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from src.visualization.dashboard import Dashboard
from src.visualization.map import DamageMap
from src.models.allocation import ResourceAllocator

st.set_page_config(page_title="Painel - Avaliação de Danos", layout="wide")

if 'zones' not in st.session_state or 'resources' not in st.session_state:
    st.warning("Por favor, vá para a página de Entrada de Dados e envie as informações primeiro.")
    st.stop()

zones = st.session_state.zones
resources = st.session_state.resources
disaster_info = st.session_state.disaster_info

st.title("Painel de Avaliação de Danos")

# Initialize components
dashboard = Dashboard()
damage_map = DamageMap()
resource_allocator = ResourceAllocator()

# Update metrics
dashboard.update_metrics(zones, resources)

# Disaster Overview Section
st.header("Visão Geral do Desastre")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tipo de Desastre", disaster_info["type"])
with col2:
    st.metric("Data", disaster_info["date"].strftime("%d/%m/%Y") if disaster_info["date"] else "Não definida")
with col3:
    st.metric("Área Afetada", f"{disaster_info['affected_area']} km²")
with col4:
    st.metric("População Estimada", f"{disaster_info['estimated_population']:,}")

# Main Metrics
st.header("Métricas Principais")
dashboard.display_metrics()

# Map and Charts Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa de Danos")
    m = damage_map.create_map(zones, resources)
    if m:
        st.components.v1.html(m._repr_html_(), height=600)

with col2:
    st.subheader("Distribuição de Danos")
    dashboard.display_damage_distribution(zones)
    
    st.subheader("Alocação de Recursos")
    dashboard.display_resource_allocation(resources)

# Resource Allocation Section
st.header("Alocação de Recursos")
if st.button("Otimizar Alocação de Recursos"):
    allocation_plan = resource_allocator.allocate_resources(zones, resources)
    st.session_state.allocation_plan = allocation_plan
    st.success("Recursos alocados com sucesso!")
    st.rerun()

if 'allocation_plan' in st.session_state:
    st.subheader("Plano de Alocação")
    
    # Create allocation matrix
    allocation_data = []
    for zone in zones:
        allocated_resources = st.session_state.allocation_plan.get(zone.id, [])
        resource_types = [r.type for r in resources if r.id in allocated_resources]
        allocation_data.append({
            "Zona": zone.name,
            "Nível de Dano": zone.damage_level,
            "Pontuação de Prioridade": zone.priority_score,
            "Recursos Alocados": ", ".join(resource_types) if resource_types else "Nenhum"
        })
    
    df = pd.DataFrame(allocation_data)
    st.dataframe(df)

# Time Series Analysis
st.header("Análise Temporal")
col1, col2 = st.columns(2)

with col1:
    # Simulated damage progression
    dates = pd.date_range(start=disaster_info["date"], periods=7, freq='D')
    damage_progression = [sum(z.damage_level for z in zones) * (1 - i/7) for i in range(7)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=damage_progression,
        mode='lines+markers',
        name='Nível de Dano'
    ))
    fig.update_layout(
        title='Progressão do Nível de Dano',
        xaxis_title='Data',
        yaxis_title='Nível Total de Dano'
    )
    st.plotly_chart(fig)

with col2:
    # Simulated resource utilization
    resource_utilization = {
        'Ambulância': [0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0],
        'Equipe de Resgate': [0.2, 0.4, 0.6, 0.75, 0.85, 0.9, 0.95],
        'Hospitais de Campanha': [0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.85]
    }
    
    fig = go.Figure()
    for resource_type, utilization in resource_utilization.items():
        fig.add_trace(go.Scatter(
            x=dates,
            y=utilization,
            mode='lines+markers',
            name=resource_type
        ))
    fig.update_layout(
        title='Utilização de Recursos ao Longo do Tempo',
        xaxis_title='Data',
        yaxis_title='Taxa de Utilização'
    )
    st.plotly_chart(fig)

# Priority Analysis
st.header("Análise de Prioridades")
priority_data = [{
    "Zona": zone.name,
    "Nível de Dano": zone.damage_level,
    "População": zone.population,
    "Pontuação de Prioridade": zone.priority_score
} for zone in zones]

df_priority = pd.DataFrame(priority_data)
fig = px.scatter(
    df_priority,
    x="Nível de Dano",
    y="População",
    size="Pontuação de Prioridade",
    hover_data=["Zona"],
    title="Análise de Prioridade por Zona"
)
st.plotly_chart(fig) 