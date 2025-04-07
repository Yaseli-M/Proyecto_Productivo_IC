import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client, Client

# Configuración de página
st.set_page_config(page_title="Análisis Crediticio", layout="wide")

# Conexión a Supabase
url = "https://igdyolghmogpjmjlpzgs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnZHlvbGdobW9ncGptamxwemdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5OTQwNTUsImV4cCI6MjA1OTU3MDA1NX0.Z7ek0HjEOkZ-4heMSzrfMCDoUBg9M7mpS6vE504bgPc"
supabase: Client = create_client(url, key)

# Obtener datos desde Supabase
@st.cache_data
def cargar_datos():
    response = supabase.table("credit_risk_score").select("*").execute()
    return pd.DataFrame(response.data)

df = cargar_datos()

# Convertir la fecha a formato datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Título
st.title("📊 Dashboard de Análisis de Riesgo Crediticio")

# Gráfico de Barras: Saldo total promedio por segmento de riesgo
st.subheader("1. Saldo promedio por segmento de riesgo")
barra_data = df.groupby("SEGMENTO_RIESGO")["SALDO_TOTAL_TARJETA"].mean().sort_values()
fig1, ax1 = plt.subplots()
sns.barplot(x=barra_data.index, y=barra_data.values, ax=ax1)
ax1.set_xlabel("Segmento de Riesgo")
ax1.set_ylabel("Saldo Promedio")
ax1.set_title("Saldo Promedio por Segmento de Riesgo")
st.pyplot(fig1)

# Gráfico de Líneas: Evolución del saldo total en el tiempo
st.subheader("2. Evolución del saldo total de tarjeta")
line_data = df.groupby("Fecha")["SALDO_TOTAL_TARJETA"].mean()
fig2, ax2 = plt.subplots()
line_data.plot(ax=ax2)
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Saldo Total Promedio")
ax2.set_title("Evolución del Saldo Total en el Tiempo")
st.pyplot(fig2)

# Gráfico de Pastel: Distribución por género
st.subheader("3. Distribución de género")
genero_map = {0: "Femenino", 1: "Masculino"}
df["Genero_Label"] = df["GENERO_F"].map(genero_map)
genero_data = df["Genero_Label"].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(genero_data, labels=genero_data.index, autopct='%1.1f%%', startangle=90)
ax3.axis("equal")
st.pyplot(fig3)

# Gráfico de Dispersión: Edad vs. Riesgo Total
st.subheader("4. Edad vs. Riesgo Cliente Total")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=df, x="EDAD", y="RIESGO_CLIENTE_TOTAL_GFP", hue="SEGMENTO_RIESGO", ax=ax4)
ax4.set_xlabel("Edad")
ax4.set_ylabel("Riesgo Cliente Total")
ax4.set_title("Dispersión: Edad vs. Riesgo Cliente Total")
st.pyplot(fig4)

# Pie de página
st.markdown("---")
st.markdown("Desarrollado por **Yamir** 💼 con 🧠 + Streamlit + Supabase")
