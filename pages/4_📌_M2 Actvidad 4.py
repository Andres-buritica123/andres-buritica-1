import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 4")

st.header("Descripción de la actividad")
st.markdown("""
En esta actividad, el estudiante explorará el uso de los métodos .loc y .iloc de pandas para acceder, 
filtrar y modificar datos dentro de un DataFrame. Utilizando un conjunto de datos de películas, 
se desarrollará una interfaz interactiva con Streamlit que permitirá seleccionar filas y columnas, 
aplicar filtros por año, y actualizar valores dinámicamente. Este ejercicio fortalece habilidades fundamentales en 
análisis de datos y programación orientada a la manipulación estructurada de información.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender la diferencia entre .loc y .iloc para la selección de datos en pandas.
- Aprender a acceder a filas y columnas por etiquetas o posiciones.
- Aplicar filtros condicionales en DataFrames usando expresiones lógicas.
- Modificar valores dentro de un DataFrame de forma controlada.
- Desarrollar una interfaz visual que permita explorar y editar datos de manera interactiva.
""")

st.header("Solución")

# --- Cargar datos de ejemplo ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Título': ['Inception', 'Titanic', 'The Matrix', 'Avengers', 'Interstellar'],
        'Año': [2010, 1997, 1999, 2012, 2014],
        'Director': ['Christopher Nolan', 'James Cameron', 'Lana Wachowski', 'Joss Whedon', 'Christopher Nolan'],
        'Puntuación': [8.8, 7.8, 8.7, 8.0, 8.6]
    })

df = load_data()

st.title("🎬 Explorador de Películas con .loc y .iloc")

# --- Ver DataFrame completo ---
if st.checkbox("Mostrar todos los datos"):
    st.dataframe(df)

# --- Selección de fila por índice usando iloc ---
st.subheader("🔢 Seleccionar una fila con .iloc")
row_idx = st.number_input("Índice de fila (0 a {})".format(len(df)-1), min_value=0, max_value=len(df)-1, step=1)
st.write("Fila seleccionada:")
st.write(df.iloc[row_idx])

# --- Selección de columnas por nombre con .loc ---
st.subheader("📌 Seleccionar columnas específicas con .loc")
selected_columns = st.multiselect("Selecciona las columnas a mostrar", df.columns.tolist(), default=df.columns.tolist())
st.write(df.loc[:, selected_columns])

# --- Filtro personalizado con .loc ---
st.subheader("🔍 Filtrar películas por año con .loc")
year_min = st.slider("Año mínimo", min_value=df['Año'].min(), max_value=df['Año'].max(), value=df['Año'].min())
year_max = st.slider("Año máximo", min_value=year_min, max_value=df['Año'].max(), value=df['Año'].max())
filtered_df = df.loc[(df['Año'] >= year_min) & (df['Año'] <= year_max)]
st.write(f"Películas entre {year_min} y {year_max}:")
st.dataframe(filtered_df)

# --- Modificar un valor con .loc ---
st.subheader("✏️ Modificar puntuación de una película")
movie_to_edit = st.selectbox("Selecciona película", df['Título'])
new_score = st.slider("Nueva puntuación", 0.0, 10.0, 5.0, step=0.1)

if st.button("Actualizar puntuación"):
    idx = df.loc[df['Título'] == movie_to_edit].index[0]
    df.loc[idx, 'Puntuación'] = new_score
    st.success(f"Puntuación de '{movie_to_edit}' actualizada a {new_score}")
    st.dataframe(df)