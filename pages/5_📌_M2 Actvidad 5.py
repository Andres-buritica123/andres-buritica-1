import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

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

# URL de la API
url = "https://api-b56e.onrender.com/users"

try:
    # Realizamos la solicitud GET
    response = requests.get(url)
    response.raise_for_status()

    # Procesamos la respuesta
    data = response.json()
    if data:
        # Normalizamos los datos (por si hay campos anidados)
        df = pd.json_normalize(data)
        
        # Mostramos todos los datos en una tabla
        st.subheader("✅ Todos los usuarios recibidos:")
        st.dataframe(df, use_container_width=True)

        # Botón para descargar el CSV completo
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

# Sección 3: Gemini IA (solo sobre trata de personas)

st.header("🤖 Asistente IA sobre Trata de Personas (usando Gemini)")

api_key = st.text_input("AIzaSyCC36tvjh-iJIsyOUur4d1o78O_Cj1W8ig", type="password")
user_question = st.text_area("🧠 Pregunta sobre los datos de trata de personas:")

# Leer el archivo CSV como texto
try:
    with open("./pages/trata_de_personas.csv", "r", encoding="utf-8") as f:
        csv_data = f.read()
except FileNotFoundError:
    st.error("❌ Archivo de datos no encontrado.")
    csv_data = None

# Función para llamar a Gemini
def consultar_gemini(api_key, pregunta, contexto):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""
Eres un asistente experto en analizar datos de trata de personas en Colombia.
Solo puedes responder preguntas basándote estrictamente en los siguientes datos CSV:
---INICIO DE DATOS---
{contexto[:15000]}
---FIN DE DATOS---

Pregunta del usuario: {pregunta}
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0:generateContent"

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ Error al consultar Gemini: {e}"

# Ejecutar consulta a Gemini
consultar = st.button("Consultar IA")

if consultar and api_key and user_question and csv_data:
    with st.spinner("Consultando a Gemini..."):
        respuesta = consultar_gemini(api_key, user_question, csv_data)
        st.markdown("### 💬 Respuesta de Gemini:")
        st.markdown(respuesta)
elif consultar:
    st.warning("⚠️ Debes ingresar la clave API, una pregunta y tener el archivo CSV disponible.")
