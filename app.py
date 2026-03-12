import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN VISUAL (ESTÉTICA DE TU FOTO) ---
st.set_page_config(page_title="C.A.F.E - Dashboard", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .card {
        background-color: white; border-radius: 15px; padding: 0px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 25px;
        overflow: hidden; border: 1px solid #E0E0E0;
    }
    .card-header { padding: 12px 20px; color: white; font-weight: bold; font-size: 18px; }
    .header-purple { background-color: #6A1B9A; }
    .header-blue { background-color: #1565C0; }
    .header-green { background-color: #2E7D32; }
    .card-body { padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN DIRECTA (MÉTODO INFALIBLE) ---
# Extraemos los datos como CSV directamente desde Google
SHEET_ID = "1Qx6Uhz_XHSETKhQwlgYNpaenq6-8nTKfGcbwAvL7hkg"
SHEET_NAME = "DB_CAFE"
url = f"https://docs.google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=10)
def cargar_datos():
    return pd.read_csv(url)

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1A237E;'>🏦 SISTEMA C.A.F.E</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos()

    # DASHBOARD ESTILO TARJETAS
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
            <div class="card">
                <div class="card-header header-purple">💰 Resumen de Capital</div>
                <div class="card-body"><h2>Socios: {len(df)}</h2></div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="card">
                <div class="card-header header-blue">📊 Estado del Sistema</div>
                <div class="card-body"><p style="font-size:18px;">Conexión: <span style="color:green;">Exitosa ✅</span></p></div>
            </div>
        ''', unsafe_allow_html=True)

    # LISTADO DE SOCIOS (Lookup de tu imagen)
    st.markdown('<div class="card"><div class="card-header header-green">👥 Listado de Socios Registrados</div><div class="card-body">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error al leer la hoja: {e}")
    st.info("Asegúrate de que la pestaña en tu Google Sheet se llame exactamente: DB_CAFE")

