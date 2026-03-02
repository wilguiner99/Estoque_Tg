import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TG EQUIPAMENTOS", layout="centered")

# Estilo Visual Ajustado para Celular (Fonte menor para não quebrar)
st.markdown("""
    <div style='background-color: #1b5e20; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0; font-family: sans-serif; font-size: 22px;'>TG EQUIPAMENTOS</h2>
        <p style='color: #a5d6a7; margin: 0; font-weight: bold; font-size: 13px;'>CONTROLE DE ESTOQUE AVÍCOLA</p>
    </div>
""", unsafe_allow_html=True)

ARQUIVO = 'estoque_tg.csv'

# Inicializar arquivo se não existir
if not os.path.exists(ARQUIVO):
    df_init = pd.DataFrame(columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp'])
    df_init.to_csv(ARQUIVO, index=False, sep=';')

# --- ENTRADA DE DADOS ---
with st.expander("📝 NOVO LANÇAMENTO", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("📦 Item:", placeholder="Ex: Parafuso 1/4")
        qtd = st.number_input("🔢 Qtd:", min_value=0, step=1)
    with col2:
        resp = st.text_input("👤 Resp:", placeholder="Seu nome")
        tipo = st.selectbox("Operação:", ["ENTRADA", "SAÍDA"])
    
    if st.button("SALVAR REGISTRO", use_container_width=True):
        if item and qtd > 0:
            data = datetime.now().strftime('%d/%m/%Y %H:%M')
            novo_dado = pd.DataFrame([[data, item.upper(), qtd, tipo, resp.upper()]], 
                                     columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp'])
            novo_dado.to_csv(ARQUIVO, mode='a', header=False, index=False, sep=';')
            st.success(f"✅ {tipo} de {item.upper()} registrada!")
            st.rerun()
        else:
            st.error("⚠️ Preencha o item e a quantidade!")

st.divider()

# --- ABAS DE CONSULTA E AJUSTES ---
tab1, tab2, tab3 = st.tabs(["📜 Histórico", "📊 Saldo Total", "🛠️ Ajustes (ID)"])

with tab1:
    try:
        df = pd.read_csv(ARQUIVO, sep=';')
        if not df.empty:
            df_show = df.iloc[::-1].copy()
            st.dataframe(df_show, use_container_width=True)
        else:
            st.info("Nenhum lançamento ainda.")
    except:
        st.info("Iniciando banco de dados...")

with tab2:
    try:
        df = pd.read_csv(ARQUIVO, sep=';')
        if not df.empty:
            df['Ajuste'] = df.apply(lambda x: x['Qtd'] if x['Tipo'] == 'ENTRADA' else -x['Qtd'], axis=1)
            saldo = df.groupby('Item')['Ajuste'].sum().reset_index()
            saldo.columns = ['Item', 'Qtd em Estoque']
            st.table(saldo)
    except:
        st.write("Sem dados para exibir.")

with tab3:
    st.write("Para excluir ou editar, use o computador ou me peça ajuda para criar um botão de limpar tudo.")
