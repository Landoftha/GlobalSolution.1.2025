import streamlit as st
import time
from src.visualization.dashboard import Dashboard
from src.visualization.map import DamageMap
from src.models.zone import Zone
from src.models.resource import Resource
from src.utils.data_loader import load_data
from src.utils.resource_allocator import ResourceAllocator
from src.models.ml_models import DisasterPredictor, RouteOptimizer

# Configuração da página
st.set_page_config(
    page_title="Salvus - Sistema de Avaliação Rápida de Danos",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do estado da sessão
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'retry_count' not in st.session_state:
    st.session_state.retry_count = 0

def load_data_with_retry():
    """Tenta carregar os dados com retry em caso de erro"""
    max_retries = 3
    retry_delay = 2  # segundos
    
    while st.session_state.retry_count < max_retries:
        try:
            zones, resources = load_data()
            if zones and resources:
                st.session_state.data_loaded = True
                st.session_state.retry_count = 0
                return zones, resources
        except Exception as e:
            st.session_state.retry_count += 1
            if st.session_state.retry_count < max_retries:
                time.sleep(retry_delay)
                continue
            else:
                st.error(f"Erro ao carregar dados após {max_retries} tentativas: {str(e)}")
                return None, None

def main():
    try:
        st.title("Salvus - Sistema de Avaliação Rápida de Danos")
        
        # Sidebar com informações do projeto
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 2rem;'>
                <h1 style='color: #1f77b4; margin: 0;'>SALVUS</h1>
                <p style='color: #666; margin: 0;'>Sistema de Avaliação Rápida de Danos</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
                <h3 style='color: #1f77b4; margin-top: 0;'>Sobre o Sistema</h3>
                <p style='color: #666; line-height: 1.6;'>O Salvus é uma plataforma inteligente para avaliação rápida de danos e alocação eficiente de recursos em situações de desastre.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;'>
                <h3 style='color: #1f77b4; margin-top: 0;'>Funcionalidades</h3>
                <ul style='color: #666; line-height: 1.6; padding-left: 1.2rem;'>
                    <li>Simulação de cenários de desastre</li>
                    <li>Classificação de severidade</li>
                    <li>Priorização inteligente</li>
                    <li>Alocação otimizada de recursos</li>
                    <li>Visualização interativa</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #1f77b4; margin-top: 0;'>Navegação</h3>
                <div style='color: #666; line-height: 1.6;'>
                    <p style='margin-bottom: 0.5rem;'><strong>1. Entrada de Dados</strong><br>Configure o cenário de desastre</p>
                    <p style='margin-bottom: 0;'><strong>2. Dashboard</strong><br>Visualize análises e métricas</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Carregar dados com retry
        if not st.session_state.data_loaded:
            with st.spinner("Carregando dados..."):
                zones, resources = load_data_with_retry()
        else:
            zones, resources = load_data()

        if not zones or not resources:
            st.warning("Nenhum dado disponível. Por favor, vá para a página de Entrada de Dados para configurar o cenário.")
            return

        # Inicializar componentes
        dashboard = Dashboard()
        damage_map = DamageMap()
        resource_allocator = ResourceAllocator()
        disaster_predictor = DisasterPredictor()
        route_optimizer = RouteOptimizer()

        # Atualizar métricas
        dashboard.update_metrics(zones, resources)

        # Exibir métricas
        dashboard.display_metrics()

        # Criar abas para diferentes visualizações
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Mapa de Danos", 
            "Análise de Dados", 
            "Alocação de Recursos",
            "Previsão de Desastres",
            "Otimização de Rotas"
        ])

        with tab1:
            st.header("Mapa de Danos e Alocação de Recursos")
            try:
                # Criar e exibir mapa
                map_obj = damage_map.create_map(zones, resources)
                if map_obj:
                    st.components.v1.html(map_obj._repr_html_(), height=600)
                else:
                    st.error("Não foi possível criar o mapa.")
            except Exception as e:
                st.error(f"Erro ao exibir o mapa: {str(e)}")

        with tab2:
            st.header("Análise de Dados")
            col1, col2 = st.columns(2)
            
            try:
                with col1:
                    dashboard.display_damage_distribution(zones)
                
                with col2:
                    dashboard.display_resource_allocation(resources)
            except Exception as e:
                st.error(f"Erro ao exibir análises: {str(e)}")

        with tab3:
            st.header("Alocação de Recursos")
            try:
                # Alocar recursos
                allocated_resources = resource_allocator.allocate_resources(zones, resources)
                
                # Exibir resultados da alocação
                st.subheader("Resultado da Alocação")
                for zone in zones:
                    with st.expander(f"Zona: {zone.name}"):
                        st.write(f"Nível de Dano: {zone.damage_level}")
                        st.write(f"População: {zone.population}")
                        st.write(f"Pontuação de Prioridade: {zone.priority_score:.2f}")
                        
                        if zone.resources_allocated:
                            st.write("Recursos Alocados:")
                            for resource in zone.resources_allocated:
                                st.write(f"- {resource.type} (Capacidade: {resource.capacity})")
                        else:
                            st.write("Nenhum recurso alocado")
            except Exception as e:
                st.error(f"Erro ao exibir alocação de recursos: {str(e)}")

        with tab4:
            st.header("Previsão de Desastres")
            try:
                if st.button("Gerar Previsões"):
                    with st.spinner("Gerando previsões..."):
                        # Converter dados para formato adequado
                        zone_data = [
                            {
                                'population': zone.population,
                                'infrastructure_damage': zone.infrastructure_damage,
                                'accessibility': zone.accessibility,
                                'critical_facilities': zone.critical_facilities,
                                'historical_risk': zone.historical_risk,
                                'damage_level': zone.damage_level
                            }
                            for zone in zones
                        ]
                        
                        # Treinar modelo (em produção, isso seria feito com dados históricos)
                        accuracy = disaster_predictor.train(zone_data)
                        st.success(f"Modelo treinado com R² score de {accuracy:.2%}")
                        
                        # Fazer previsões
                        predictions = disaster_predictor.predict(zone_data)
                        
                        # Exibir resultados
                        st.subheader("Previsão de Danos por Zona")
                        for zone, pred in zip(zones, predictions):
                            # Garantir que a previsão esteja entre 0 e 1
                            pred = max(0.0, min(1.0, pred))
                            st.metric(
                                label=f"Zona {zone.name}",
                                value=f"{pred:.1%}",
                                delta=f"{pred - zone.damage_level:.1%}"
                            )
                            
                        # Adicionar visualização de tendências
                        st.subheader("Análise de Tendências")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("Fatores de Risco por Zona")
                            risk_data = {
                                'Zona': [zone.name for zone in zones],
                                'Risco Histórico': [zone.historical_risk for zone in zones],
                                'Danos na Infraestrutura': [zone.infrastructure_damage for zone in zones],
                                'Acessibilidade': [zone.accessibility for zone in zones]
                            }
                            st.bar_chart(risk_data)
                        
                        with col2:
                            st.write("Correlação entre Fatores")
                            correlation_data = {
                                'População': [zone.population for zone in zones],
                                'Danos Atuais': [zone.damage_level for zone in zones],
                                'Previsão': predictions
                            }
                            st.line_chart(correlation_data)
                            
            except Exception as e:
                st.error(f"Erro ao gerar previsões: {str(e)}")

        with tab5:
            st.header("Otimização de Rotas")
            try:
                route_optimizer.build_graph(zones, resources)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Rota entre Zonas")
                    start_zone = st.selectbox(
                        "Zona de Origem",
                        options=[zone.name for zone in zones],
                        key="start_zone"
                    )
                    end_zone = st.selectbox(
                        "Zona de Destino",
                        options=[zone.name for zone in zones],
                        key="end_zone"
                    )
                    
                    if st.button("Calcular Rota"):
                        start_id = next(z.id for z in zones if z.name == start_zone)
                        end_id = next(z.id for z in zones if z.name == end_zone)
                        
                        route = route_optimizer.find_optimal_route(start_id, end_id)
                        if route:
                            st.success("Rota encontrada!")
                            st.write("Sequência de zonas:", " → ".join(route))
                        else:
                            st.warning("Não foi possível encontrar uma rota.")
                
                with col2:
                    st.subheader("Rota de Alocação de Recursos")
                    resource = st.selectbox(
                        "Recurso",
                        options=[r.name for r in resources],
                        key="resource"
                    )
                    
                    if st.button("Calcular Rota de Alocação"):
                        resource_id = next(r.id for r in resources if r.name == resource)
                        target_zones = [z.id for z in zones if z.damage_level > 0.5]
                        
                        route = route_optimizer.get_resource_allocation_route(
                            resource_id,
                            target_zones
                        )
                        
                        if route:
                            st.success("Rota de alocação encontrada!")
                            st.write("Sequência de zonas:", " → ".join(route))
                        else:
                            st.warning("Não foi possível encontrar uma rota de alocação.")
            
            except Exception as e:
                st.error(f"Erro ao calcular rotas: {str(e)}")

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {str(e)}")
        st.info("Por favor, tente recarregar a página.")

if __name__ == "__main__":
    main() 