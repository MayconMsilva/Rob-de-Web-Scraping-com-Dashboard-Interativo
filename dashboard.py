import streamlit as st
import sqlite3
import pandas as pd

# Título da Página

st.title("Dashboard de Livros(Web Scraping)")

# Conexão com banco de dados

conn = sqlite3.connect("dados.db")
df = pd.read_sql_query("SELECT*FROM livros", conn)

# Filtros
st.sidebar.header("Filtros")

# Filtro por palavra-chave no título
palavra_chave = st.sidebar.text_input("Buscar por título:")

# Filtro por preço minimo
preco_min = st.sidebar.number_input(
    "Preço Mínimo (£):", min_value=0.0, step=0.5)

# Filtro por preço máximo
preco_max = st.sidebar.number_input(
    "Preço Máximo (£):", min_value=0.0, step=0.5, value=100.0)

# Limpeza do campo de preço e conversão para float
df['preco_float'] = (
    df['preco']
    .str.encode('ascii', 'ignore')  # remove caracteres não ASCII como Â
    .str.decode('ascii')            # converte de volta para string
    .str.replace('£', '')           # remove o símbolo de libra (opcional)
    .str.replace(',', '')           # remove vírgulas, se houver
    .astype(float)                  # converte para float
)


# Aplicando filtros

df_filtrado = df[
    df['titulo'].str.contains(palavra_chave, case=False, na=False) &
    (df['preco_float'] >= preco_min) &
    (df['preco_float'] <= preco_max)
]

# Exibir total de livros encontrados
st.write(f"Livros encontrados: {df_filtrado.shape[0]}")

# Tabela de dados

st.dataframe(df_filtrado[['titulo', 'preco']])

# Botão para exportar os dados filtrados

csv = df_filtrado.to_csv(index=False)
st.download_button("Baixar CSV", data=csv,
                   file_name="livros_filtrados.csv", mime="text/csv")
