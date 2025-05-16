import streamlit as st
import io
import pandas as pd


# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 2")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad tiene como propósito realizar un análisis exploratorio de datos sobre estudiantes en Colombia 
utilizando Pandas y Streamlit. A partir de un archivo CSV, se carga información de estudiantes y 
se ofrece una interfaz interactiva para visualizar, filtrar y explorar distintos aspectos del conjunto de datos, 
como sus promedios, edades y nombres. La aplicación también permite generar resúmenes estadísticos y 
estructurales del dataset, favoreciendo la comprensión y el análisis de los datos.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Importar y visualizar datos desde archivos CSV con Pandas en una app interactiva.
- Aplicar filtros dinámicos para seleccionar columnas específicas y filtrar por valores como el promedio académico.
-Utilizar st.expander, st.dataframe, st.slider y otros elementos de Streamlit para mejorar la experiencia de análisis.
- AInterpretar resúmenes estadísticos y estructurales de un conjunto de datos.
- Fomentar habilidades básicas en análisis de datos exploratorio (EDA) usando Python y herramientas modernas de visualización.
""")

st.header("Solución")

st.title("Análisis de Estudiantes en Colombia")
@st.cache_data

def cargar_datos():
    try:
        df = pd.read_csv("./pages/estudiantes_colombia.csv")
        df["nombre"] = df["nombre"].astype(str)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.subheader("Primeras 5 filas del dataset")
    st.dataframe(df.head())

    st.subheader("Últimas 5 filas del dataset")
    st.dataframe(df.tail())

    with st.expander("📋 Resumen de estructura"):
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.code(buffer.getvalue(), language="text")

    with st.expander("📊 Resumen estadístico"):
        st.dataframe(df.describe(include='all'), use_container_width=True)

    st.subheader("Seleccionar columnas específicas")
    columnas = st.multiselect("Selecciona las columnas que deseas visualizar:", df.columns.tolist(), default=["nombre", "edad", "promedio"])
    if columnas:
        st.dataframe(df[columnas])

    st.subheader("Filtrar estudiantes por promedio mínimo")
    min_promedio = st.slider("Promedio mínimo:", min_value=0.0, max_value=5.0, step=0.1, value=4.0)
    filtro_df = df[df["promedio"] >= min_promedio]
    st.write(f"Estudiantes con promedio mayor o igual a {min_promedio}:")
    st.dataframe(filtro_df)
else:
    st.warning("No se pudieron cargar los datos.")