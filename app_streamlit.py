
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulador_combo import simular_intervalo_alunos

st.set_page_config(layout="wide")

st.title("Simulador de Custo - COMBO Plataforma A")

st.sidebar.header("Parâmetros")

min_alunos = st.sidebar.number_input("Quantidade mínima de alunos", 100, 5000, 100)
max_alunos = st.sidebar.number_input("Quantidade máxima de alunos", 1000, 20000, 10000)
step_alunos = st.sidebar.number_input("Intervalo", 50, 1000, 100)

def entrada_cliente(produto):
    st.subheader(f"{produto.upper()} - Cliente")
    tipo = st.radio(f"Tipo de contratação do cliente ({produto})", ['Licenciamento', 'Interno'], key=produto)
    if tipo == 'Interno':
        cf = st.number_input(f"CF {produto}", 0, 1_000_000, 120000, step=1000)
        if produto == 'avaliacao':
            qtd_q = st.number_input(f"Qtd. Questões", 0, 10000, 2000)
            custo_q = st.number_input(f"Custo por questão", 0.0, 100.0, 2.0)
            return {'modelo': 'interno', 'cf': cf, 'qtd_questoes': qtd_q, 'custo_questao': custo_q}
        return {'cf': cf}
    else:
        cv = st.number_input(f"CV {produto}", 0.0, 500.0, 20.0)
        taxa = st.number_input(f"Taxa {produto}", 0.0, 100000.0, 5000.0)
        return {'modelo': 'licenciamento', 'cv': cv, 'taxa': taxa}

def entrada_proposta(produto):
    st.subheader(f"{produto.upper()} - Proposta")
    cv = st.number_input(f"CV {produto} (proposta)", 0.0, 500.0, 20.0)
    taxa = st.number_input(f"Taxa {produto} (proposta)", 0.0, 100000.0, 5000.0)
    return {'cv': cv, 'taxa': taxa}

with st.expander("Configuração do Cliente", expanded=True):
    config_cliente = {
        'conteudo': entrada_cliente('conteudo'),
        'labs': entrada_cliente('labs'),
        'avaliacao': entrada_cliente('avaliacao'),
        'lms': entrada_cliente('lms'),
    }

with st.expander("Configuração da Proposta", expanded=True):
    config_proposta = {
        'conteudo': entrada_proposta('conteudo'),
        'labs': entrada_proposta('labs'),
        'avaliacao': entrada_proposta('avaliacao'),
        'lms': entrada_proposta('lms'),
    }

resultados = simular_intervalo_alunos(config_cliente, config_proposta, (min_alunos, max_alunos, step_alunos))
df = pd.DataFrame(resultados)

st.subheader("Comparativo de Investimento Total")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['alunos'], df['cliente'], label="Situação do Cliente", linestyle='--', marker='o')
ax.plot(df['alunos'], df['proposta'], label="Proposta COMBO", linestyle='-', marker='x')
ax.set_xlabel("Quantidade de Alunos")
ax.set_ylabel("Investimento Total (R$)")
ax.set_title("Curva de Custo: Cliente vs Proposta")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.subheader("Tabela de Resultados")
st.dataframe(df)
