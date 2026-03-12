import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE INTERFAZ (PALETA DE COLORES) ---
st.set_page_config(page_title="Sistema C.A.F.E.", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F5F5F5; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 10px; border: 1px solid #E0E0E0; }
    div[data-testid="metric-container"]:nth-child(1) { border-left: 5px solid #4CAF50; } /* Verde - Capital */
    div[data-testid="metric-container"]:nth-child(2) { border-left: 5px solid #FF9800; } /* Naranja - Caja Chica */
    div[data-testid="metric-container"]:nth-child(3) { border-left: 5px solid #2196F3; } /* Azul - Préstamos */
    div[data-testid="metric-container"]:nth-child(4) { border-left: 5px solid #9C27B0; } /* Morado - Voluntarios */
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (BASE DE DATOS TEMPORAL) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'capital_prestable': 5000.0,
        'caja_chica': 150.0,
        'prestamos_activos': 1200.0,
        'voluntarios': 450.0,
        'socios': pd.DataFrame([
            {"Nombre": "Socio Fundador 1", "Ahorro": 200.0, "Intereses": 15.0, "Tipo": "Fundador"},
            {"Nombre": "Socio Externo A", "Ahorro": 50.0, "Intereses": 0.0, "Tipo": "Externo"}
        ])
    }

st.title("🏦 SISTEMA C.A.F.E.")
st.caption("Caja de Ahorro Fe y Esperanza - Gestión Integral")

# --- 1. DASHBOARD PRINCIPAL (MÉTRICAS) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Capital Prestable (FIC)", f"${st.session_state.db['capital_prestable']}", help="Dinero listo para otorgar préstamos")
with col2:
    st.metric("Caja Chica / Gastos", f"${st.session_state.db['caja_chica']}", help="Fondo operativo y multas")
with col3:
    st.metric("Préstamos Activos", f"${st.session_state.db['prestamos_activos']}", help="Cartera vigente en la calle")
with col4:
    st.metric("Aportes Voluntarios", f"${st.session_state.db['voluntarios']}", help="Ahorros extra que generan intereses")

st.divider()

# --- 2. PANELES DE OPERACIÓN ---
tab1, tab2, tab3, tab4 = st.tabs(["👥 Socios", "💸 Préstamos", "📅 Aportes Domingos", "📊 Reportes"])

with tab1:
    st.subheader("Listado de Socios Registrados")
    st.table(st.session_state.db['socios'])
    
    with st.expander("➕ Registrar Nuevo Socio"):
        c1, c2 = st.columns(2)
        nuevo_nom = c1.text_input("Nombre Completo")
        tipo_s = c2.selectbox("Tipo", ["Fundador", "Externo"])
        if st.button("Guardar Socio"):
            # Lógica de inscripción Art. 4 ($10 USD)
            st.session_state.db['caja_chica'] += 3.0
            st.session_state.db['capital_prestable'] += 4.0
            st.success(f"Socio {nuevo_nom} registrado. $3 a Caja Chica, $4 a FIC.")

with tab2:
    st.subheader("Gestión de Créditos")
    col_p1, col_p2 = st.columns(2)
    monto_p = col_p1.number_input("Monto Solicitado", min_value=50, step=50)
    tasa_p = col_p2.selectbox("Tasa Aplicable", ["Socio (5%)", "Externo (8%)"])
    
    # Validación de Liquidez (Art. 5)
    if monto_p > st.session_state.db['capital_prestable']:
        st.error("⚠️ Fondos Insuficientes en el FIC para este monto.")
    else:
        if st.button("Aprobar Préstamo"):
            st.session_state.db['capital_prestable'] -= monto_p
            st.session_state.db['prestamos_activos'] += monto_p
            st.success(f"Desembolso aprobado por ${monto_p}")

with tab3:
    st.subheader("Control Dominical (Puntualidad)")
    hora_actual = datetime.now().strftime("%H:%M")
    st.write(f"Hora de registro: **{hora_actual}**")
    
    socio_pago = st.selectbox("Socio que entrega aporte", st.session_state.db['socios']['Nombre'])
    if st.button("Registrar $2.00 Semanales"):
        # Lógica de Multa Art. 2 ($0.50 si es después de las 18:00)
        ahora = datetime.now()
        if ahora.hour >= 18:
            st.session_state.db['caja_chica'] += 0.50
            st.warning("Multa de $0.50 aplicada por retraso.")
        st.session_state.db['capital_prestable'] += 2.0
        st.success("Aporte registrado correctamente.")

with tab4:
    st.subheader("Resumen de Utilidades (Modelo Igualitario)")
    utilidad_total = st.session_state.db['caja_chica'] + (st.session_state.db['prestamos_activos'] * 0.05) # Simulación
    st.info(f"Utilidad Líquida Estimada: ${utilidad_total:.2f}")
    st.write(f"Monto por cada uno de los 10 fundadores: **${utilidad_total/10:.2f}**")
