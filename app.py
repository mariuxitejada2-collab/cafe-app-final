import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página y Estética (Logo)
st.set_page_config(page_title="CAFE - Caja de Ahorro", page_icon="💰")
st.title("🏦 Sistema de Gestión CAFE")
st.subheader("Caja de Ahorro Fe y Esperanza")

# Simulación de Base de Datos (En una app real esto iría en SQL)
if 'socios' not in st.session_state:
    st.session_state.socios = pd.DataFrame(
        columns=["ID", "Nombre", "Ahorro_Total", "Tipo", "Deuda_Actual"]
    )

# --- MENÚ LATERAL ---
menu = st.sidebar.selectbox("Panel de Control", ["Inicio", "Aportes Domingos", "Préstamos", "Estado de Cuenta"])

# --- LÓGICA DE APORTES (DOMINGOS 6:00 PM) ---
if menu == "Aportes Domingos":
    st.header("📥 Registro de Aporte Semanal")
    nombre = st.selectbox("Seleccionar Socio", st.session_state.socios["Nombre"])
    hora_pago = st.time_input("Hora de Pago", datetime.now().time())
    
    if st.button("Registrar Aporte $2.00"):
        multa = 0.50 if hora_pago.hour >= 18 else 0.0
        # Aquí se sumaría el ahorro y se restaría la multa en la base de datos
        st.success(f"Aporte registrado para {nombre}. Multa aplicada: ${multa}")
        if multa > 0:
            st.warning("⚠️ Pago fuera de horario (Después de las 6:00 PM)")

# --- LÓGICA DE PRÉSTAMOS (TASAS 5% Y 8%) ---
elif menu == "Préstamos":
    st.header("💸 Solicitud de Crédito")
    tipo_socio = st.radio("Tipo de Solicitante", ["Socio Fundador (5%)", "Externo (8%)"])
    monto = st.number_input("Monto a solicitar", min_value=50.0, step=50.0)
    
    tasa = 0.05 if "Fundador" in tipo_socio else 0.08
    interes_mensual = monto * tasa
    total_a_pagar = monto + interes_mensual
    
    st.info(f"Interés mensual: ${interes_mensual:.2f} | Total a devolver: ${total_a_pagar:.2f}")
    
    if st.button("Aprobar Desembolso"):
        st.balloons()
        st.success("Préstamo registrado en el sistema.")

# --- REGISTRO DE SOCIOS INICIAL ---
elif menu == "Inicio":
    st.write("Bienvenido al sistema digital de **CAFE**. Utilice el menú lateral para gestionar los fondos.")
    with st.expander("Registrar Nuevo Socio"):
        nuevo_nombre = st.text_input("Nombre Completo")
        tipo = st.selectbox("Categoría", ["Fundador", "Externo"])
        if st.button("Añadir a la Caja"):
            nueva_fila = {"ID": len(st.session_state.socios)+1, "Nombre": nuevo_nombre, "Ahorro_Total": 0, "Tipo": tipo, "Deuda_Actual": 0}
            st.session_state.socios = st.session_state.socios.append(nueva_fila, ignore_index=True)
            st.success("Socio registrado con éxito.")
    
    st.dataframe(st.session_state.socios)

