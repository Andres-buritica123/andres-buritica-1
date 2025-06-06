import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
import openai

# Configuración de la página
st.set_page_config(page_icon="📌", layout="wide")

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
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data:
        df = pd.json_normalize(data)

        st.subheader("✅ Tabla de Usuarios")
        st.dataframe(df, use_container_width=True)

        # Descargar CSV
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Descargar todos los datos como CSV",
            data=csv,
            file_name='usuarios_api.csv',
            mime='text/csv'
        )

        # Filtros si existen las columnas necesarias
        if 'genero' in df.columns:
            generos = df['genero'].dropna().unique().tolist()
            genero_filtrado = st.multiselect("🔘 Filtrar por género:", generos, default=generos)
            df = df[df['genero'].isin(genero_filtrado)]

        if 'edad' in df.columns:
            edad_min = int(df['edad'].min())
            edad_max = int(df['edad'].max())
            edad_range = st.slider("📏 Rango de edad:", min_value=edad_min, max_value=edad_max,
                                   value=(edad_min, edad_max))
            df = df[(df['edad'] >= edad_range[0]) & (df['edad'] <= edad_range[1])]

        st.markdown("---")

        # Columnas para mostrar múltiples gráficos en una fila
        col1, col2 = st.columns(2)

        # 📊 Gráfico de barras por género
        if 'genero' in df.columns:
            with col1:
                st.subheader("👥 Usuarios por Género")
                fig_gen = px.bar(
                    df['genero'].value_counts().reset_index(),
                    x='index',
                    y='genero',
                    labels={'index': 'Género', 'genero': 'Cantidad'},
                    color='index',
                    title='Distribución de Géneros'
                )
                st.plotly_chart(fig_gen, use_container_width=True)

        # 🥧 Pie chart de género
        if 'genero' in df.columns:
            with col2:
                st.subheader("🧁 Porcentaje por Género")
                fig_pie = px.pie(
                    df,
                    names='genero',
                    title='Porcentaje de Usuarios por Género',
                    hole=0.4
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # 📈 Histograma de edades
        if 'edad' in df.columns:
            st.subheader("📈 Histograma de Edades")
            fig_hist = px.histogram(
                df,
                x='edad',
                nbins=10,
                title='Distribución de Edades',
                labels={'edad': 'Edad'},
                color_discrete_sequence=['#00BFC4']
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        # 🌐 Dispersión edad vs. fecha (si hay campo fecha)
        fecha_col = None
        for col in df.columns:
            if 'fecha' in col.lower():
                fecha_col = col
                break

        if fecha_col:
            try:
                df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
                df_fecha = df[df[fecha_col].notna()]

                if not df_fecha.empty:
                    st.subheader(f"🕒 Edad vs. {fecha_col}")
                    fig_scatter = px.scatter(
                        df_fecha,
                        x=fecha_col,
                        y='edad',
                        color='genero' if 'genero' in df.columns else None,
                        title='Relación entre Edad y Fecha',
                        labels={'edad': 'Edad', fecha_col: 'Fecha'}
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.warning(f"La columna '{fecha_col}' no contiene fechas válidas para graficar.")
            except Exception:
                st.warning(f"No se pudo procesar la columna de fecha: {fecha_col}")

    else:
        st.warning("⚠️ La respuesta JSON está vacía.")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Error durante la solicitud: {e}")
except ValueError as e:
    st.error(f"❌ Error al procesar JSON: {e}")
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")

st.header("Descripción de la Actividad")

st.markdown("""
Esta actividad consiste en el desarrollo de una **aplicación web con Streamlit** que interactúa con el modelo de lenguaje **ChatGPT (OpenAI API)**.  
El objetivo principal es permitir que los usuarios ingresen preguntas o temas y reciban respuestas generadas automáticamente por la inteligencia artificial de OpenAI.  
Se emplean herramientas del ecosistema Python para integrar servicios de IA en una interfaz web amigable:

- `openai` para la comunicación con la API de OpenAI  
- `Streamlit` para crear una interfaz interactiva sin necesidad de conocimientos avanzados de desarrollo web  
""")

st.header("Objetivos de Aprendizaje")

st.markdown("""
- Comprender cómo interactuar con un modelo de lenguaje de IA usando la API de OpenAI  
- Aprender a construir una aplicación web funcional y ligera con Streamlit  
- Gestionar entradas del usuario y mostrar respuestas generadas dinámicamente  
- Aplicar buenas prácticas en el manejo de claves API y errores en llamadas a servicios externos  
- Explorar el potencial del procesamiento de lenguaje natural en aplicaciones reales  
""")

st.header("Solución")

# Configuración de la página
st.title("💬 Chat con ChatGPT")
st.markdown("Ingresa un tema o pregunta y obtén una respuesta generada por la IA de OpenAI.")

# Campo para la clave de API
api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI:", type="password")

# Campo de entrada del usuario
prompt = st.text_input("✍️ Escribe tu pregunta o tema:", placeholder="Ej. ¿Cómo funciona la inteligencia artificial?")
enviar = st.button("Generar Respuesta")

# Función para generar respuesta con OpenAI
def generar_respuesta(prompt, api_key):
    if not prompt:
        return "Por favor, escribe una pregunta o tema."
    if not api_key:
        return "Debes ingresar tu API key."

    try:
        openai.api_key = api_key
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Mostrar respuesta si se presiona el botón
if enviar and prompt:
    with st.spinner("🔄 Generando respuesta..."):
        respuesta = generar_respuesta(prompt, api_key)
        st.subheader("📢 Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Escribe una pregunta y haz clic en Generar Respuesta.")
