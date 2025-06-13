from PIL import Image
import streamlit as st
from google import genai
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import json
import matplotlib.pyplot as plt
import google.generativeai as genai

# ✅ Configuración de la página (esto debe ir al principio)
st.set_page_config(
    page_title="Poryecto Integrador",
    page_icon="⚙️",
    layout="wide"
)
# -----------------------------
# 🧩 Parte 1: Estructuras de Datos
# -----------------------------
st.title("Proyecto Integrador")
st.title("Actividad 1")

st.header("Descripción de la actividad")
st.markdown("""
Actividad para construir un **dashboard interactivo** en Streamlit que:
- Carga y limpia un CSV con casos de trata de personas.
- Transforma fechas y extrae el **año**.
- Genera métricas (casos totales, departamentos, municipios).
- Aplica filtros dinámicos por **año** y **departamento**.
- Muestra gráficos y tabla actualizada de los datos.
""")

st.header("Objetivos de Aprendizaje")
st.markdown("""
- Cargar y transformar datos con **Pandas** (fechas, filtros).
- Calcular métricas clave con agrupaciones.
- Implementar filtros interactivos en **Streamlit**.
- Visualizar datos con **Plotly**.
- Exponer datos limpios en formato de tabla.
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
st.title("Actividad 2")

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

st.title("📊 Visualización de Casos de Trata de Personas por Departamento")

# Cargar CSV con columnas en mayúscula
try:
    df = pd.read_csv("./pages/trata_de_personas.csv")
    df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], errors='coerce')
    df['CANTIDAD'] = pd.to_numeric(df['CANTIDAD'], errors='coerce').fillna(0).astype(int)
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].astype(str).str.upper()
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")
    st.stop()

# Filtrado dinámico por año
anios_disponibles = sorted(df['FECHA HECHO'].dt.year.dropna().unique())
anio_seleccionado = st.selectbox("📅 Selecciona un año", anios_disponibles)

df_filtrado = df[df['FECHA HECHO'].dt.year == anio_seleccionado]

# Agrupación por departamento
casos_por_departamento = df_filtrado.groupby("DEPARTAMENTO")["CANTIDAD"].sum().sort_values(ascending=False)

# Mostrar gráfico circular con los 5 principales
top_5 = casos_por_departamento.head(5)
otros = pd.Series([casos_por_departamento[5:].sum()], index=["OTROS"])
casos_final = pd.concat([top_5, otros])

fig, ax = plt.subplots()
ax.pie(casos_final, labels=casos_final.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')

st.subheader(f"🧩 Distribución de casos por departamento en {anio_seleccionado}")
st.pyplot(fig)
    
# -----------------------------
# 🧩 Parte 3: API DE GEMINI AI  
# -----------------------------
st.title("Actividad 3")

st.header("Descripción de la actividad")
st.markdown("""
Actividad para crear un **chat interactivo en Streamlit** que:
- Carga un CSV desde una URL fija (local o pública).
- Muestra la tabla con los datos.
- Permite al usuario escribir una pregunta.
- Envía tanto la pregunta como un extracto del CSV a **Gemini**.
- Devuelve y muestra la respuesta del modelo basada en los datos.
""")

st.header("Objetivos de Aprendizaje")
st.markdown("""
- Aprender a **cargar y mostrar** datos desde una URL o ruta fija.
- Implementar entrada de texto y botones para **interacción del usuario**.
- Construir un **prompt dinámico** que combine datos tabulares y preguntas.
- Conectar con un modelo de IA (Gemini) para **generar respuestas contextuales**.
- Presentar la respuesta dentro de la interfaz web.
""")

genai.configure(api_key="AIzaSyBwfPpP1jSHoTr6vaISCm9jHcCT-4ShQss") # Reemplaza con tu clave real

st.title("💬 Chat con Gemini y CSV de URL Fija")
st.markdown("Pregunta sobre los datos de un CSV cargado desde una URL predefinida.")

# --- Parte 1: Definir la URL del CSV internamente ---
# Reemplaza esta URL con la de tu propio archivo CSV
csv_url_fija = "./pages/trata_de_personas.csv" # Ejemplo de un CSV público

df = None # Inicializa df
st.subheader("1. Cargando CSV desde URL fija...")
try:
    df = pd.read_csv(csv_url_fija)
    st.success(f"CSV cargado exitosamente desde: {csv_url_fija}")
    st.write("Información del archivo:")
    st.dataframe(df)
except Exception as e:
    st.error(f"Error al cargar el CSV desde la URL fija: {e}. Asegúrate de que la URL es correcta y el archivo es accesible.")
    df = pd.DataFrame() # Asegurarse de que df esté definido
# --- Parte 2: Interacción con Gemini ---
st.subheader("2. Haz tu pregunta a Gemini")
prompt_usuario = st.text_input("Escribe tu pregunta o tema:", placeholder="Ej. ¿Que casos hubieron en 2008?")
enviar = st.button("Generar Respuesta")

# Función para interactuar con Gemini (la misma que antes)
def generar_respuesta_con_contexto(prompt_usuario, dataframe):
    if not prompt_usuario:
        return "Por favor, ingresa un tema o pregunta."

    contexto_csv = ""
    if not dataframe.empty:
        contexto_csv = "A continuación, se presenta un fragmento de un archivo CSV:\n\n"
        contexto_csv += dataframe.to_markdown(index=False)
        contexto_csv += "\n\nBasándote en esta información y en tus conocimientos, responde a la siguiente pregunta:"

    full_prompt = f"{contexto_csv}\n\nPregunta: {prompt_usuario}"

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error al comunicarse con Gemini: {str(e)}"

# Lógica principal
if enviar and prompt_usuario:
    if not df.empty:
        with st.spinner("Generando respuesta..."):
            respuesta = generar_respuesta_con_contexto(prompt_usuario, df)
            st.subheader("Respuesta de Gemini:")
            st.markdown(respuesta)
    else:
        st.warning("No se pudo cargar el CSV desde la URL fija.")
else:
    st.info("Escribe un tema o pregunta y haz clic en Generar Respuesta.")

st.title("Integrantes: ")

# Definir el alto deseado para todas las imágenes
ALTO_DESEADO = 200

# Listado de (ruta, nombre) por estudiante
datos_estudiantes = [
    ("assets/foto3.jpg", "Andrés Buritica"),
    ("assets/foto2.jpg", "Andrés Buritica"),
    ("assets/foto1.jpg", "Andrés Buritica"),
    ("assets/foto4.jpg", "Andrés Buritica"),
    ("assets/foto5.jpg", "Andrés Buritica")
]

cols = st.columns(len(datos_estudiantes))

for col, (ruta, nombre) in zip(cols, datos_estudiantes):
    with col:
        img = Image.open(ruta)
        w, h = img.size
        nuevo_ancho = int(w * (ALTO_DESEADO / h))
        img_resized = img.resize((nuevo_ancho, ALTO_DESEADO), Image.LANCZOS)
        st.image(img_resized, caption=nombre)
