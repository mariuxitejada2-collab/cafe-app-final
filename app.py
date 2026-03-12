import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection  # <--- ESTA LÍNEA ES LA QUE FALTA

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="C.A.F.E - Dashboard", page_icon="🏦", layout="wide")
# --- CONEXIÓN A DATOS ---
# Esta es la URL que apunta directamente a tu hoja DB_CAFE
url_hoja = "https://docs.google.com/spreadsheets/d/1Qx6Uhz_XHSETKhQwlgYNpaenq6-8nTKfGcbwAvL7hkg/edit?usp=sharing" 

conn = st.connection("gsheets", type=GSheetsConnection)

# Intentamos leer la hoja
try:
    df = conn.read(spreadsheet=url_hoja, worksheet="DB_CAFE", ttl=0)
    
    # --- INTERFAZ ---
    st.markdown("<h1 style='text-align: center; color: #1A237E;'>🏦 C.A.F.E</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="card"><div class="card-header header-purple">💰 Capital Total</div><div class="card-body"><h2>Socios: {len(df)}</h2></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="card-header header-blue">📊 Estado</div><div class="card-body"><p>Sincronizado con Google ✅</p></div></div>', unsafe_allow_html=True)

    # Listado de Socios (Con los nombres de columna que pusiste en tu Excel)
    st.markdown('<div class="card"><div class="card-header header-green">👥 Listado de Socios</div><div class="card-body">', unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df[["Usuario", "Nombre", "Celular", "Saldo"]], use_container_width=True, hide_index=True)
    else:
        st.info("La base de datos está lista. ¡Agreguemos al primer socio!")
    st.markdown('</div></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.info("Asegúrate de que el botón COMPARTIR en Google Sheets diga 'Cualquier persona con el enlace'.")


