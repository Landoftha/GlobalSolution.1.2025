# Sistema de Avaliação Rápida de Danos

Sistema para avaliação rápida de danos e otimização de alocação de recursos pós-desastre.

## Funcionalidades

- Visualização de áreas afetadas em mapa interativo
- Classificação de severidade de danos por área
- Otimização de alocação de recursos
- Dashboard com métricas e estatísticas
- Visualização de distribuição de danos
- Monitoramento de alocação de recursos

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

Para iniciar o sistema:
```bash
streamlit run src/app.py
```

## Estrutura do Projeto

```
src/
├── data/
│   ├── raw/           # Dados originais
│   └── processed/     # Dados processados
├── models/           # Algoritmos de otimização
├── visualization/    # Componentes de visualização
└── utils/           # Funções auxiliares
```

## Tecnologias Utilizadas

- Python
- Streamlit
- Folium
- Plotly
- GeoPandas
- Shapely

