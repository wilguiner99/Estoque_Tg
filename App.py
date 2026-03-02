import streamlit as st
import pandas as pd
from datetime import datetime
import os

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="TG ESTOQUE", layout="wide")

# Estilo para botões e visual
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    div.stButton > button { width: 100%; height: 60px; font-weight: bold; font-size: 20px; border-radius: 10px; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# LOGIN SIMPLES
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔐 ACESSO TG")
    user = st.text_input("Usuário")
    pw = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if user == "Admin" and pw == "1234":
            st.session_state['auth'] = True
            st.rerun()
        else: st.error("Incorreto")
    st.stop()

# BANCO DE DADOS
ARQUIVO = 'estoque_tg.csv'
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp']).to_csv(ARQUIVO, index=False, sep=';')

# CABEÇALHO GIGANTE
st.markdown("<h1 style='text-align: center; color: #1b5e20;'>🚜 TG EQUIPAMENTOS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>CONTROLE DE ESTOQUE RÁPIDO</p>", unsafe_allow_html=True)

# ÁREA DE DIGITAÇÃO
with st.container():
    item = st.text_input("📦 O QUE ESTÁ MOVIMENTANDO?", placeholder="Ex: Parafuso, Bucha...")
    col_q, col_r = st.columns(2)
    qtd = col_q.number_input("QUANTIDADE:", min_value=1, step=1)
    resp = col_r.text_input("QUEM É VOCÊ?", placeholder="Seu nome")

    st.write("---")
    c1, c2 = st.columns(2)
    
    # Botão de ENTRADA (Verde)
    if c1.button("📥 ENTRADA", type="primary"):
        if item and resp:
            data = datetime.now().strftime('%d/%m %H:%M')
            novo = pd.DataFrame([[data, item.upper(), qtd, "ENTRADA", resp.upper()]], columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp'])
            novo.to_csv(ARQUIVO, mode='a', header=False, index=False, sep=';')
            st.success("REGISTRADO!")
            st.rerun()

    # Botão de SAÍDA (Vermelho)
    if c2.button("📤 SAÍDA"):
        if item and resp:
            data = datetime.now().strftime('%d/%m %H:%M')
            novo = pd.DataFrame([[data, item.upper(), qtd, "SAÍDA", resp.upper()]], columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp'])
            novo.to_csv(ARQUIVO, mode='a', header=False, index=False, sep=';')
            st.warning("SAÍDA REGISTRADA!")
            st.rerun()

st.write("### 📋 PLANILHA DE MOVIMENTAÇÃO")
# MOSTRAR A PLANILHA SEMPRE
try:
    df = pd.read_csv(ARQUIVO, sep=';')
    if not df.empty:
        # Mostra os últimos 20 registros primeiro
        st.dataframe(df.iloc[::-1].head(20), use_container_width=True, hide_index=True)
        
        # BOTÃO PARA LIMPAR TUDO (CUIDADO)
        if st.expander("🗑️ OPÇÕES AVANÇADAS"):
            if st.button("LIMPAR TODA A PLANILHA"):
                pd.DataFrame(columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp']).to_csv(ARQUIVO, index=False, sep=';')
                st.rerun()
    else:
        st.info("A planilha está vazia. Faça o primeiro lançamento acima!")
except:
    st.error("Erro ao ler a planilha. Tente limpar os dados.")
