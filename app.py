import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Conexión a Supabase
SUPABASE_URL = "https://igdyolghmogpjmjlpzgs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnZHlvbGdobW9ncGptamxwemdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5OTQwNTUsImV4cCI6MjA1OTU3MDA1NX0.Z7ek0HjEOkZ-4heMSzrfMCDoUBg9M7mpS6vE504bgPc"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cargar los datos desde la tabla Supabase
@st.cache_data
def load_data():
    response = supabase.table("credit_risk_data").select("*").execute()
    return pd.DataFrame(response.data)

# Streamlit app
st.set_page_config(page_title="Datos de Riesgo Crediticio", layout="wide")
st.title("Datos desde Supabase: Riesgo Crediticio")

df = load_data()

st.write(f"Total de registros: {len(df)}")
st.dataframe(df)

print("DataFrame cargado desde Supabase:")
