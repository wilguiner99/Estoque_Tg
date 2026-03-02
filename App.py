import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TG EQUIPAMENTOS", layout="centered")

# Estilo Visual (Logotipo Verde Escuro)
st.markdown("""
    <div style='background-color: #1b5e20; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='color: white; margin: 0; font-family: sans-serif;'>TG EQUIPAMENTOS</h1>
        <p style='color: #a5d6a7; margin: 0; font-weight: bold;'>CONTROLE DE ESTOQUE AVÍCOLA</p>
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
    df = pd.read_csv(ARQUIVO, sep=';')
    df.index = df.index + 1
    st.dataframe(df.tail(15), use_container_width=True)

with tab2:
    df['Ajuste'] = df.apply(lambda x: x['Qtd'] if x['Tipo'] == 'ENTRADA' else -x['Qtd'], axis=1)
    saldo = df.groupby('Item')['Ajuste'].sum().reset_index()
    saldo.columns = ['Item', 'Qtd em Estoque']
    saldo['Status'] = saldo['Qtd em Estoque'].apply(lambda x: '✅ OK' if x >= 10 else '⚠️ REPOR')
    st.table(saldo)

with tab3:
    st.write("Digite o ID (número à esquerda no histórico) para modificar:")
    id_alvo = st.number_input("🆔 ID para Modificar:", min_value=1, step=1)
    
    col_ed, col_ex = st.columns(2)
    with col_ed:
        if st.button("EDITAR POR ID", type="secondary", use_container_width=True):
            df = pd.read_csv(ARQUIVO, sep=';')
            idx = id_alvo - 1
            if 0 <= idx < len(df):
                if item: df.loc[idx, 'Item'] = item.upper()
                if qtd > 0: df.loc[idx, 'Qtd'] = qtd
                df.to_csv(ARQUIVO, index=False, sep=';')
                st.success(f"✅ ID {id_alvo} editado!")
                st.rerun()
    with col_ex:
        if st.button("EXCLUIR POR ID", type="primary", use_container_width=True):
            df = pd.read_csv(ARQUIVO, sep=';')
            idx = id_alvo - 1
            if 0 <= idx < len(df):
                df = df.drop(idx)
                df.to_csv(ARQUIVO, index=False, sep=';')
                st.warning(f"🗑️ Registro {id_alvo} removido!")
                st.rerun()
