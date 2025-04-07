# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from supabase import create_client, Client

# Configura Supabase
url = "https://igdyolghmogpjmjlpzgs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
supabase: Client = create_client(url, key)

# Título
st.title("Predicción de Riesgo Crediticio")

# Carga los datos desde Supabase
@st.cache_data
def cargar_datos():
    response = supabase.table("credit_risk_data").select("*").execute()
    data = pd.DataFrame(response.data)
    return data

df = cargar_datos()

# Mostrar tabla
st.subheader("Datos cargados")
st.dataframe(df.head())

# Estadísticas
st.subheader("Resumen Estadístico")
st.write(df.describe())

# Visualización: Distribución de riesgo
st.subheader("Distribución del Riesgo Crediticio")
if 'risk' in df.columns:
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='risk', ax=ax)
    st.pyplot(fig)
else:
    st.warning("La columna 'risk' no fue encontrada.")

# Visualización: Correlación entre variables
st.subheader("Matriz de Correlación")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)
