import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client, Client

# Configuración de página
st.set_page_config(page_title="Dashboard Crediticio", layout="wide")

# Supabase config
url = "https://igdyolghmogpjmjlpzgs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnZHlvbGdobW9ncGptamxwemdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5OTQwNTUsImV4cCI6MjA1OTU3MDA1NX0.Z7ek0HjEOkZ-4heMSzrfMCDoUBg9M7mpS6vE504bgPc"
supabase: Client = create_client(url, key)

# Función para cargar los datos
@st.cache_data
def cargar_datos():
    try:
        response = supabase.table("credit_risk_data").select("*").execute()
        data = response.data
        if data:
            return pd.DataFrame(data)
        else:
            st.warning("No se encontraron datos en la tabla.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al conectar con Supabase:\n\n{e}")
        return pd.DataFrame()

# Cargar datos
df = cargar_datos()

if not df.empty:
    st.title("📊 Dashboard de Análisis de Riesgo Crediticio")

    # Convertir la fecha a datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')

    # Gráfico 1: Barras - Segmento de riesgo vs saldo total promedio
    st.subheader("1️⃣ Saldo promedio por segmento de riesgo")
    barra_data = df.groupby("SEGMENTO_RIESGO")["SALDO_TOTAL_TARJETA"].mean().sort_values()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=barra_data.index, y=barra_data.values, ax=ax1)
    ax1.set_xlabel("Segmento de Riesgo")
    ax1.set_ylabel("Saldo Promedio")
    ax1.set_title("Saldo Promedio por Segmento de Riesgo")
    st.pyplot(fig1)

    # Gráfico 2: Línea - Evolución del saldo total
    st.subheader("2️⃣ Evolución del saldo total de tarjeta")
    linea_data = df.groupby("Fecha")["SALDO_TOTAL_TARJETA"].mean().sort_index()
    fig2, ax2 = plt.subplots()
    linea_data.plot(ax=ax2)
    ax2.set_xlabel("Fecha")
    ax2.set_ylabel("Saldo Promedio")
    ax2.set_title("Evolución del Saldo Promedio en el Tiempo")
    st.pyplot(fig2)

    # Gráfico 3: Pastel - Distribución de género
    st.subheader("3️⃣ Distribución por género")
    genero_map = {0: "Femenino", 1: "Masculino"}
    df["Genero_Label"] = df["GENERO_F"].map(genero_map)
    genero_data = df["Genero_Label"].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.pie(genero_data, labels=genero_data.index, autopct='%1.1f%%', startangle=90)
    ax3.set_title("Distribución de Género")
    ax3.axis('equal')
    st.pyplot(fig3)

    # Gráfico 4: Dispersión - Edad vs Riesgo
    st.subheader("4️⃣ Edad vs. Riesgo Cliente Total")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=df, x="EDAD", y="RIESGO_CLIENTE_TOTAL_GFP", hue="SEGMENTO_RIESGO", ax=ax4)
    ax4.set_xlabel("Edad")
    ax4.set_ylabel("Riesgo Cliente Total")
    ax4.set_title("Relación Edad vs. Riesgo Total")
    st.pyplot(fig4)

    st.markdown("---")
    st.markdown("💼 Desarrollado por **Yamir** con 🧠 Streamlit + Supabase")
else:
    st.warning("No se pudo cargar la información. Verifica la conexión o los permisos en Supabase.")

