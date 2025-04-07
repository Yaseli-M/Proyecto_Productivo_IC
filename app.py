# archivo: app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client, Client

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Análisis de Riesgo de Crédito con Supabase", layout="wide")
st.title("Análisis de Riesgo de Crédito (Conexión Supabase)")

# --- CONEXIÓN A SUPABASE ---
url = "https://igdyolghmogpjmjlpzgs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnZHlvbGdobW9ncGptamxwemdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5OTQwNTUsImV4cCI6MjA1OTU3MDA1NX0.Z7ek0HjEOkZ-4heMSzrfMCDoUBg9M7mpS6vE504bgPc"
supabase: Client = create_client(url, key)

# --- CARGAR DATOS DESDE SUPABASE ---
@st.cache_data
def cargar_datos():
    response = supabase.table("credit_risck").select("*").execute()
    data = response.data
    return pd.DataFrame(data)

df = cargar_datos()

# --- MOSTRAR TABLA ---
st.subheader("Datos obtenidos desde Supabase")
st.dataframe(df, use_container_width=True)

# --- GRAFICOS Y ANÁLISIS ---
st.subheader("Análisis Segmentado")

# 🔹 Gráfico 1: Riesgo por Sexo
if 'Sex' in df.columns and 'Risk' in df.columns:
    st.markdown("### Riesgo de crédito según el género")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x='Sex', hue='Risk', ax=ax1)
    st.pyplot(fig1)

# 🔹 Gráfico 2: Riesgo por Estado Civil
if 'Marital status' in df.columns and 'Risk' in df.columns:
    st.markdown("### Riesgo de crédito según el estado civil")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x='Marital status', hue='Risk', ax=ax2)
    st.pyplot(fig2)

# 🔹 Gráfico 3: Edad por Riesgo
if 'Age' in df.columns and 'Risk' in df.columns:
    st.markdown("### Distribución de edad según riesgo")
    fig3, ax3 = plt.subplots()
    sns.histplot(data=df, x='Age', hue='Risk', kde=True, ax=ax3)
    st.pyplot(fig3)
