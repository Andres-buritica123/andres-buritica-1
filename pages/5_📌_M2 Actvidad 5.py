
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 5")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una **introducción práctica a Python** y a las **estructuras de datos básicas**.  
Exploraremos los conceptos fundamentales del lenguaje y aprenderemos a utilizar:

- Variables
- Tipos de datos
- Operadores
- Estructuras de datos como listas, tuplas, diccionarios y conjuntos

El enfoque será práctico, con ejemplos reales y útiles para desarrollar una base sólida en programación.
""")

st.header("Objetivos de Aprendizaje")

st.markdown("""
- Comprender los tipos de datos básicos en Python  
- Aprender a utilizar variables y operadores  
- Dominar las estructuras de datos fundamentales  
- Aplicar estos conocimientos en ejemplos prácticos y ejercicios  
""")

st.header("Solución")

# Cargar datos
df = pd.read_csv("./pages/trata_de_personas.csv")

# --- Limpieza de datos ---
df.columns = df.columns.str.strip().str.upper()
df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], errors='coerce')
df['AÑO'] = df['FECHA HECHO'].dt.year

# --- Título ---
st.title("📊 Dashboard: Casos de Trata de Personas en Colombia")

# --- KPIs ---
total_casos = int(df['CANTIDAD'].sum())
total_departamentos = df['DEPARTAMENTO'].nunique()
total_municipios = df['MUNICIPIO'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total de Casos", f"{total_casos}")
col2.metric("Departamentos", f"{total_departamentos}")
col3.metric("Municipios", f"{total_municipios}")

# --- Filtros ---
st.subheader("Filtros")

fcol1, fcol2 = st.columns(2)

with fcol1:
    años = st.multiselect(
        "Selecciona Años", 
        options=sorted(df['AÑO'].dropna().unique()), 
        default=sorted(df['AÑO'].dropna().unique())
    )

with fcol2:
    deptos = st.multiselect(
        "Selecciona Departamentos", 
        options=sorted(df['DEPARTAMENTO'].dropna().unique()), 
        default=sorted(df['DEPARTAMENTO'].dropna().unique())
    )
# --- Aplicar filtros ---
df_filtrado = df[df['AÑO'].isin(años) & df['DEPARTAMENTO'].isin(deptos)]

# --- Gráfico de casos por año ---
st.subheader("Casos por Año")
casos_anuales = df_filtrado.groupby('AÑO')['CANTIDAD'].sum().reset_index()
fig1 = px.bar(casos_anuales, x='AÑO', y='CANTIDAD', labels={'CANTIDAD': 'Cantidad de Casos'})
st.plotly_chart(fig1)

# --- Gráfico por Departamento ---
st.subheader("Casos por Departamento")
casos_departamento = df_filtrado.groupby('DEPARTAMENTO')['CANTIDAD'].sum().reset_index().sort_values(by='CANTIDAD', ascending=False)
fig2 = px.bar(casos_departamento, x='CANTIDAD', y='DEPARTAMENTO', orientation='h', labels={'CANTIDAD': 'Cantidad de Casos'})
st.plotly_chart(fig2)

# --- Tabla de datos filtrados ---
st.subheader("Datos Filtrados")
st.dataframe(df_filtrado.sort_values(by='FECHA HECHO', ascending=False))