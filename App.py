import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TG EQUIPAMENTOS", layout="centered")

# Estilo Visual (Logotipo Verde)
st.markdown("""
    <div style='background-color: #2e602f; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0; font-size: 24px;'>TG EQUIPAMENTOS</h2>
        <p style='color: #a5d6a7; margin: 0; font-size: 14px;'>CONTROLE DE ESTOQUE AVÍCOLA</p>
    </div>
""", unsafe_allow_html=True)

ARQUIVO = 'estoque_tg.csv'

# Inicializar arquivo
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp']).to_csv(ARQUIVO, index=False, sep=';')

# --- ENTRADA DE DADOS ---
with st.container():
    item = st.text_input("📦 Item:", placeholder="Ex: Parafuso 1/4")
    qtd = st.number_input("🔢 Qtd:", min_value=0, step=1)
    resp = st.text_input("👤 Resp:", placeholder="Seu nome")

    # Botões Lado a Lado (Estilo o seu print)
    col1, col2 = st.columns(2)
    
    with col1:
        btn_entrada = st.button("ENTRADA", type="primary", use_container_width=True)
    with col2:
        btn_saida = st.button("SAÍDA", type="secondary", use_container_width=True)

    # Lógica de Salvar
    if btn_entrada or btn_saida:
        tipo = "ENTRADA" if btn_entrada else "SAÍDA"
        if item and qtd > 0:
            data = datetime.now().strftime('%d/%m/%Y %H:%M')
            novo = pd.DataFrame([[data, item.upper(), qtd, tipo, resp.upper()]], columns=['Data', 'Item', 'Qtd', 'Tipo', 'Resp'])
            novo.to_csv(ARQUIVO, mode='a', header=False, index=False, sep=';')
            st.success(f"✅ {tipo} de {item.upper()} salva!")
            st.rerun()

st.divider()

# --- BOTÕES DE CONSULTA ---
col_hist, col_saldo = st.columns(2)
show_hist = col_hist.button("HISTÓRICO", use_container_width=True)
show_saldo = col_saldo.button("SALDO TOTAL", use_container_width=True)

df = pd.read_csv(ARQUIVO, sep=';')

if show_hist:
    st.subheader("📜 Últimos Lançamentos")
    st.dataframe(df.iloc[::-1], use_container_width=True)

if show_saldo:
    st.subheader("📊 Estoque Atual")
    df['Ajuste'] = df.apply(lambda x: x['Qtd'] if x['Tipo'] == 'ENTRADA' else -x['Qtd'], axis=1)
    saldo = df.groupby('Item')['Ajuste'].sum().reset_index()
    st.table(saldo)

st.divider()

# --- ÁREA DE EDIÇÃO (ESTILO O SEU PRINT) ---
st.markdown("### 🛠️ AJUSTES (POR ID)")
id_alvo = st.number_input("🆔 ID (Linha):", min_value=1, step=1)

col_edit, col_excluir = st.columns(2)

if col_edit.button("EDITAR", use_container_width=True):
    idx = id_alvo - 1
    if 0 <= idx < len(df):
        if item: df.loc[idx, 'Item'] = item.upper()
        if qtd > 0: df.loc[idx, 'Qtd'] = qtd
        df.to_csv(ARQUIVO, index=False, sep=';')
        st.success("Editado com sucesso!")
        st.rerun()
    else:
        st.error("❌ ID não encontrado!")

if col_excluir.button("EXCLUIR", type="primary", use_container_width=True):
    idx = id_alvo - 1
    if 0 <= idx < len(df):
        df = df.drop(idx)
        df.to_csv(ARQUIVO, index=False, sep=';')
        st.warning("Registro excluído!")
        st.rerun()
