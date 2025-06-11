import streamlit as st
from google import genai
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import json
import google.generativeai as genai

# ✅ Configuración de la página (esto debe ir al principio)
st.set_page_config(
    page_title="Momento 2 - Actividad 5",
    page_icon="📌",
    layout="wide"
)

# -----------------------------
# 🧩 Parte 1: Estructuras de Datos
# -----------------------------
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

# --- Cargar y limpiar datos ---
df = pd.read_csv("./pages/trata_de_personas.csv")
df.columns = df.columns.str.strip().str.upper()
df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], errors='coerce')
df['AÑO'] = df['FECHA HECHO'].dt.year

# --- KPIs ---
st.title("📊 Dashboard: Casos de Trata de Personas en Colombia")
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

df_filtrado = df[df['AÑO'].isin(años) & df['DEPARTAMENTO'].isin(deptos)]

# --- Gráficos ---
st.subheader("Casos por Año")
casos_anuales = df_filtrado.groupby('AÑO')['CANTIDAD'].sum().reset_index()
fig1 = px.bar(casos_anuales, x='AÑO', y='CANTIDAD', labels={'CANTIDAD': 'Cantidad de Casos'})
st.plotly_chart(fig1)

st.subheader("Casos por Departamento")
casos_departamento = df_filtrado.groupby('DEPARTAMENTO')['CANTIDAD'].sum().reset_index().sort_values(by='CANTIDAD', ascending=False)
fig2 = px.bar(casos_departamento, x='CANTIDAD', y='DEPARTAMENTO', orientation='h', labels={'CANTIDAD': 'Cantidad de Casos'})
st.plotly_chart(fig2)

st.subheader("Datos Filtrados")
st.dataframe(df_filtrado.sort_values(by='FECHA HECHO', ascending=False))

# -----------------------------
# 🧩 Parte 2: API REST - Usuarios
# -----------------------------
st.header("Descripción de la Actividad")
st.markdown("""
Esta actividad consiste en el desarrollo de una **aplicación web con Streamlit** que consume datos desde una **API REST gratuita en la nube**.  
El objetivo principal es consultar, visualizar y exportar datos de usuarios, utilizando herramientas del ecosistema Python como:

- `requests` para realizar solicitudes HTTP  
- `pandas` para el procesamiento de datos en formato JSON  
- `Streamlit` para construir una interfaz web interactiva  

La app permite mostrar todos los registros obtenidos y descargar los datos como archivo CSV para su análisis posterior.
""")

st.header("Objetivos de Aprendizaje")
st.markdown("""
- Comprender cómo consumir una API REST desde Python  
- Aprender a procesar y normalizar datos JSON usando pandas  
- Desarrollar interfaces web simples con Streamlit  
- Mostrar y exportar datos en tablas dinámicas  
- Aplicar buenas prácticas en el manejo de errores durante solicitudes web  
""")

st.header("Solución")
st.title("📊 Consulta de usuarios desde API en la nube")

url = "https://api-b56e.onrender.com/users"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data:
        df = pd.json_normalize(data)
        st.subheader("✅ Todos los usuarios recibidos:")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Descargar todos los datos como CSV",
            data=csv,
            file_name='usuarios_api.csv',
            mime='text/csv'
        )
    else:
        st.warning("⚠️ La respuesta JSON está vacía.")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Error durante la solicitud: {e}")
except ValueError as e:
    st.error(f"❌ Error al procesar JSON: {e}")
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")

# ------------------------------
# 🔐 Configurar clave directamente (bajo tu propio riesgo)
# ------------------------------
genai.configure(api_key="AIzaSyBwfPpP1jSHoTr6vaISCm9jHcCT-4ShQss")  # 👈 Puedes ocultarla con st.secrets si quieres

# ------------------------------
# 🧠 Función de contexto para Gemini
# ------------------------------
def construir_contexto(df):
    resumen = f"Tengo {len(df)} registros de trata de personas en Colombia.\n"
    resumen += f"Columnas: {', '.join(df.columns)}.\n"
    resumen += f"Departamentos únicos: {', '.join(df['departamento'].dropna().unique()[:5])}...\n"
    return resumen

# ------------------------------
# ✨ Generar respuesta desde Gemini
# ------------------------------
def generar_respuesta(prompt):
    contexto = construir_contexto(df)
    full_prompt = contexto + "\n\nPregunta del usuario:\n" + prompt
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Error al generar respuesta: {str(e)}"

# ------------------------------
# 📊 Interfaz principal Streamlit
# ------------------------------
st.title("💬 Chat con Gemini y datos de Trata de Personas")
st.markdown("Haz preguntas como: *'¿Cuántos casos hubo en Bogotá en 2006?'* o *'¿Qué departamentos tienen más casos?'*")

# Cargar CSV
try:
    df = pd.read_csv("./pages/trata_de_personas.csv")
    df.columns = df.columns.str.lower()
    df['FECHA HECHO'] = pd.to_datetime(df['fecha hecho'], errors='coerce')
except Exception as e:
    st.error(f"❌ No se pudo cargar el archivo: {e}")
    st.stop()

# Mostrar todo el DataFrame
with st.expander("📋 Ver todos los datos"):
    st.dataframe(df)

# Entrada del usuario
pregunta = st.text_input("✍️ Escribe tu pregunta:", placeholder="¿Cuántos casos hubo en Antioquia en 2020?")
if st.button("Generar respuesta") and pregunta:
    with st.spinner("⏳ Consultando a Gemini..."):
        respuesta = generar_respuesta(pregunta)
        st.subheader("🧾 Respuesta de Gemini:")
        st.markdown(respuesta)
