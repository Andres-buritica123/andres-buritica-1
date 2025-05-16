import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 1")

st.header("Descripción de la actividad")
st.markdown("""
En esta actividad, se exploran múltiples fuentes de datos y se transforman en DataFrames de Pandas,
que luego se visualizan utilizando la biblioteca Streamlit. Se trabaja con estructuras como listas, 
diccionarios, archivos locales (CSV, Excel, JSON), bases de datos (SQLite y Firebase), así como datos remotos
y arrays de NumPy. El propósito es familiarizarse con distintas formas de estructurar, importar y 
mostrar datos dentro de una interfaz interactiva.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender la estructura y utilidad de un DataFrame como contenedor de datos tabulares en Pandas.
- Crear DataFrames desde diferentes fuentes: listas, diccionarios, archivos, APIs y bases de datos.
- Integrar bases de datos como SQLite y Firebase para recuperación y visualización de datos.
- Manejar errores comunes al cargar archivos o conectarse a servicios externos.
- Usar Streamlit como herramienta de visualización y exploración de datos en tiempo real.
- Fomentar buenas prácticas de manipulación y visualización de datos en Python.
""")

st.header("Solución")
st.title("Actividad 1 - Creación de DataFrames")
st.write("Objetivo: Familiarizarse con la creación de DataFrames en Pandas y mostrarlos usando Streamlit.")

# Diccionario
st.header("1. DataFrame de Libros")
libros = {
    "título": ["1984", "Cien Años de Soledad", "Don Quijote", "El Principito"],
    "autor": ["George Orwell", "Gabriel García Márquez", "Miguel de Cervantes", "Antoine de Saint-Exupéry"],
    "año de publicación": [1949, 1967, 1605, 1943],
    "género": ["Distopía", "Realismo Mágico", "Novela", "Fábula"]
}
df_libros = pd.DataFrame(libros)
st.dataframe(df_libros)

# Lista de diccionarios
st.header("2. Información de Ciudades")
ciudades = [
    {"nombre": "Tokio", "población": 37400068, "país": "Japón"},
    {"nombre": "Delhi", "población": 28514000, "país": "India"},
    {"nombre": "Shanghái", "población": 25582000, "país": "China"}
]
df_ciudades = pd.DataFrame(ciudades)
st.dataframe(df_ciudades)

# Lista de listas
st.header("3. Productos en Inventario")
productos = [
    ["Laptop", 1200, 10],
    ["Teclado", 25, 50],
    ["Mouse", 15, 75]
]
df_productos = pd.DataFrame(productos, columns=["Producto", "Precio", "Stock"])
st.dataframe(df_productos)

# Series
st.header("4. Datos de Personas")
nombres = pd.Series(["Ana", "Luis", "Marta", "Carlos"])
edades = pd.Series([25, 30, 22, 28])
ciudades = pd.Series(["Madrid", "México", "Bogotá", "Buenos Aires"])
df_personas = pd.DataFrame({"Nombre": nombres, "Edad": edades, "Ciudad": ciudades})
st.dataframe(df_personas)

# CSV local
st.header("5. Datos desde CSV")
try:
    df_csv = pd.read_csv("./pages/data.csv")
    st.dataframe(df_csv)
except FileNotFoundError:
    st.warning("Archivo 'data.csv' no encontrado.")

# Excel local
st.header("6. Datos desde Excel")
try:
    df_excel = pd.read_excel("./pages/data.xlsx", engine='openpyxl')
    st.dataframe(df_excel)
except FileNotFoundError:
    st.warning("Archivo 'data.xlsx' no encontrado.")
except ImportError:
    st.warning("Necesitas instalar openpyxl: pip install openpyxl")

# JSON local
st.header("7. Datos de Usuarios desde JSON")
try:
    df_json = pd.read_json("./pages/data.json")
    st.dataframe(df_json)
except FileNotFoundError:
    st.warning("Archivo 'data.json' no encontrado.")

# URL externa (ejemplo con datos abiertos)
st.header("8. Datos desde URL")
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
try:
    df_url = pd.read_csv(url)
    st.dataframe(df_url)
except Exception as e:
    st.warning(f"No se pudo cargar desde URL: {e}")

# SQLite
st.header("9. Datos desde SQLite")
conn = sqlite3.connect("estudiantes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS alumnos (nombre TEXT, calificación INTEGER)")
cursor.execute("INSERT INTO alumnos VALUES ('Pedro', 85), ('Lucía', 90), ('Andrés', 78)")
conn.commit()
df_sqlite = pd.read_sql("SELECT * FROM alumnos", conn)
st.dataframe(df_sqlite)
conn.close()

# NumPy
st.header("10. Datos desde NumPy")
array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df_numpy = pd.DataFrame(array, columns=["Columna A", "Columna B", "Columna C"])
st.dataframe(df_numpy)

st.header("11. Datos desde FireBase (opcional)")
st.info("Esta sección requiere tener una base de datos en FireBase.")

st.header("12. Datos desde MongoDB (opcional)")
st.info("Esta sección requiere tener una base de datos MongoDB en ejecución con pymongo.")