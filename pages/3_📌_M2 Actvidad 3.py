import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Configuración de la página
st.set_page_config(page_icon="📌", layout="wide")

st.title("Momento 2 - Actividad 3")

# Introducción
st.header("Descripción de la actividad")
st.markdown("""
Esta actividad tiene como propósito familiarizar al estudiante con las estructuras de datos fundamentales en Python 
a través de un enfoque práctico y contextualizado. Se utiliza un conjunto de datos simulado 
que representa características de personas en diferentes regiones de Colombia, 
permitiendo aplicar filtros dinámicos mediante una interfaz interactiva creada con Streamlit. El estudiante podrá 
manipular datos, aplicar condiciones y observar resultados en tiempo real, fortaleciendo así su comprensión de listas, 
diccionarios, tipos de datos, operadores, y estructuras de control.
""")

st.header("Objetivos de aprendizaje")
st.markdown("""
- Comprender los tipos de datos básicos y su uso en Python.
- Identificar y aplicar estructuras de datos como listas, diccionarios y fechas.
- Utilizar condicionales y operaciones lógicas para filtrar y procesar información.
- Diseñar interfaces interactivas para la visualización de datos usando Streamlit.
- Interpretar y analizar datos simulados mediante filtros dinámicos.
""")

st.header("Solución")
st.title("Análisis de Estudiantes en Colombia")

# Enlace a Colab
st.subheader("Enlace al Notebook de Google Colab:")
colab_link = "https://colab.research.google.com/drive/1KMgNIzFmyDXsLEAhNAecdq3btaVF5iW0?usp=sharing"
st.markdown(f"[Haz clic aquí para acceder al Notebook de Google Colab]({colab_link})")

# Generación de datos simulados
nombres = ['Ana', 'Luis', 'Carlos', 'María', 'Pedro', 'Laura', 'Jorge', 'Sofía', 'Andrés', 'Valentina']
ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
ocupaciones = ['Estudiante', 'Empleado', 'Desempleado', 'Independiente', 'Docente', 'Ingeniero', 'Médico', 'Emprendedor', 'Pensionado']
viviendas = ['Propia', 'Arriendo', 'Familiar']
sectores = ['Salud', 'Educación', 'Tecnología', 'Comercio', 'Otro']
regiones = ['Andina', 'Caribe', 'Pacífica', 'Orinoquía', 'Amazonía']

datos = []
for _ in range(100):
    datos.append({
        'nombre_completo': random.choice(nombres),
        'municipio': random.choice(ciudades),
        'edad': random.randint(15, 75),
        'ocupacion': random.choice(ocupaciones),
        'tipo_vivienda': random.choice(viviendas),
        'sector': random.choice(sectores),
        'region': random.choice(regiones),
        'ingreso_mensual': None if random.random() < 0.05 else random.randint(800_000, 12_000_000),
        'acceso_internet': random.choice([True, False]),
        'fecha_nacimiento': pd.to_datetime(random.choice(pd.date_range("1949-01-01", "2009-12-31")))
    })

df = pd.DataFrame(datos)

# Interfaz en dos columnas
col1, col2 = st.columns([3, 1])

# Columna izquierda - Resultados
with col1:
    st.title("📊 Aplicación de Filtros Dinámicos")
    st.markdown("Filtra los datos usando los controles en la barra lateral.")
    df_filtrado = df.copy()

# Columna derecha - Filtros
with col2:
    st.header("🎛️ Filtros")

    # 1. Rango de edad
    if st.checkbox("Filtrar por rango de edad"):
        min_edad, max_edad = st.slider("Selecciona el rango de edad", 15, 75, (20, 60))
        df_filtrado = df_filtrado[df_filtrado["edad"].between(min_edad, max_edad)]

    # 2. Municipios
    if st.checkbox("Filtrar por municipios"):
        municipios = list(set(ciudades + ['Santa Marta', 'Tunja', 'Manizales', 'Quibdó', 'Buenaventura', 'Villavicencio', 'Yopal', 'Leticia', 'Puerto Inírida']))
        municipios.sort()
        municipios_seleccionados = st.multiselect("Selecciona municipios", municipios)
        if municipios_seleccionados:
            df_filtrado = df_filtrado[df_filtrado["municipio"].isin(municipios_seleccionados)]

    # 3. Ingreso mensual mínimo
    if st.checkbox("Filtrar por ingreso mensual mínimo"):
        ingreso_min = st.slider("Ingreso mínimo (COP)", 800_000, 12_000_000, 2_000_000, step=100_000)
        df_filtrado = df_filtrado[df_filtrado["ingreso_mensual"] > ingreso_min]

    # 4. Ocupación
    if st.checkbox("Filtrar por ocupación"):
        ocupaciones_sel = st.multiselect("Selecciona ocupaciones", ocupaciones)
        if ocupaciones_sel:
            df_filtrado = df_filtrado[df_filtrado["ocupacion"].isin(ocupaciones_sel)]

    # 5. No vivienda propia
    if st.checkbox("Filtrar personas sin vivienda propia"):
        df_filtrado = df_filtrado[df_filtrado["tipo_vivienda"] != "Propia"]

    # 6. Contiene en nombre
    if st.checkbox("Filtrar por nombre"):
        subcadena = st.text_input("Buscar en nombre")
        if subcadena:
            df_filtrado = df_filtrado[df_filtrado["nombre_completo"].str.contains(subcadena, case=False, na=False)]

    # 7. Año de nacimiento
    if st.checkbox("Filtrar por año de nacimiento"):
        año = st.selectbox("Selecciona el año", list(range(1949, 2010)))
        df_filtrado = df_filtrado[df_filtrado["fecha_nacimiento"].dt.year == año]

    # 8. Acceso a internet
    if st.checkbox("Filtrar por acceso a internet"):
        acceso = st.radio("¿Tiene acceso a internet?", ["Sí", "No"])
        df_filtrado = df_filtrado[df_filtrado["acceso_internet"] == (acceso == "Sí")]

    # 9. Ingreso mensual nulo
    if st.checkbox("Filtrar por ingresos nulos"):
        df_filtrado = df_filtrado[df_filtrado["ingreso_mensual"].isnull()]

    # 10. Rango de fechas nacimiento
    if st.checkbox("Filtrar por rango de fechas de nacimiento"):
        f1 = st.date_input("Fecha inicio", datetime(1950, 1, 1))
        f2 = st.date_input("Fecha fin", datetime(2009, 12, 31))
        f1 = pd.to_datetime(f1)  # Conversión clave
        f2 = pd.to_datetime(f2)
        df_filtrado = df_filtrado[df_filtrado["fecha_nacimiento"].between(f1, f2)]

# Mostrar resultados filtrados
with col1:
    st.markdown(f"### Resultados: {df_filtrado.shape[0]} registros encontrados")
    st.dataframe(df_filtrado)