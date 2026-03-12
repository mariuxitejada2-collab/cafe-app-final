import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
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

# --- CONEXIÓN A DATOS ---
url_hoja = "https://docs.google.com/spreadsheets/d/1Qx6Uhz_XHSETKhQwlgYNpaenq6-8nTKfGcbwAvL7hkg/edit?usp=sharingHEETS" 
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos():
    return conn.read(spreadsheet=url_hoja, worksheet="DB_CAFE", ttl=0)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1A237E;'>🏦 C.A.F.E</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="card"><div class="card-header header-purple">💰 Capital Total</div><div class="card-body"><h2>Socios: {len(df)}</h2></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="card-header header-blue">📊 Estado</div><div class="card-body"><p>Sincronizado con Google ✅</p></div></div>', unsafe_allow_html=True)

    # Listado de Socios (Estilo Imagen Original)
    st.markdown('<div class="card"><div class="card-header header-green">👥 Listado de Socios</div><div class="card-body">', unsafe_allow_html=True)
    st.dataframe(df[["Usuario", "Nombre", "Celular", "Saldo"]], use_container_width=True, hide_index=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Formulario de Registro
    with st.expander("📝 Registrar Nuevo Socio"):
        with st.form("reg_form"):
            u = st.text_input("Usuario")
            n = st.text_input("Nombre Completo")
            c = st.text_input("Celular")
            p = st.text_input("Clave", type="password")
            if st.form_submit_button("Guardar Registro"):
                nuevo_socio = pd.DataFrame([{"Usuario": u, "Nombre": n, "Celular": c, "Saldo": 0.0, "Clave": p}])
                df_final = pd.concat([df, nuevo_socio], ignore_index=True)
                conn.update(spreadsheet=url_hoja, worksheet="DB_CAFE", data=df_final)
                st.success("¡Socio registrado exitosamente!")
                st.rerun()

except Exception as e:
    st.error("Configura la URL de tu hoja de cálculo en el código.")
