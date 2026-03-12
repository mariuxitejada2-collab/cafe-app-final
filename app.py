import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="SISTEMA C.A.F.E.", layout="wide")

# --- BASE DE DATOS SIMULADA ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "admin": {"clave": "cafe2026", "rol": "admin"},
        "socio1": {"clave": "1234", "rol": "socio", "nombre": "Socio Fundador 1", "ahorro": 200.0}
    }

# --- FUNCIÓN: TABLA DE AMORTIZACIÓN ---
def generar_amortizacion(monto, meses, tasa):
    cuota = monto * (tasa / (1 - (1 + tasa)**-meses))
    datos = []
    saldo = monto
    for i in range(1, meses + 1):
        interes = saldo * tasa
        abono_capital = cuota - interes
        saldo -= abono_capital
        datos.append([i, round(cuota, 2), round(interes, 2), round(abono_capital, 2), max(0, round(saldo, 2))])
    return pd.DataFrame(datos, columns=["Mes", "Cuota", "Interés", "Abono Capital", "Saldo Pendiente"])

# --- LÓGICA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso SISTEMA C.A.F.E.")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if usuario in st.session_state.usuarios and st.session_state.usuarios[usuario]["clave"] == clave:
            st.session_state.autenticado = True
            st.session_state.rol = st.session_state.usuarios[usuario]["rol"]
            st.session_state.usuario_actual = usuario
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
else:
    # --- VISTA: CERRAR SESIÓN ---
    st.sidebar.write(f"Usuario: **{st.session_state.usuario_actual}**")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # --- VISTA: ADMINISTRADOR ---
    if st.session_state.rol == "admin":
        st.title("📊 Panel Administrativo - C.A.F.E.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Capital Prestable", "$5,000.00")
        col2.metric("Préstamos en Calle", "$1,200.00")
        col3.metric("Caja Chica (Multas)", "$150.00")
        
        st.subheader("Gestión Global de Socios")
        st.table(pd.DataFrame([{"Socio": "Socio Fundador 1", "Ahorro": 200.0, "Mora": "$0.00"}]))

    # --- VISTA: SOCIO ---
    else:
        datos_socio = st.session_state.usuarios[st.session_state.usuario_actual]
        st.title(f"👋 Bienvenido, {datos_socio['nombre']}")
        
        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Mi Ahorro Total", f"${datos_socio['ahorro']}")
        col_s2.metric("Estado de Préstamo", "Sin deuda activa")

        st.divider()
        st.subheader("📝 Solicitar Préstamo")
        monto = st.number_input("Monto a solicitar ($)", min_value=50, step=50)
        plazo = st.slider("Plazo (meses)", 1, 12, 3)
        
        # Tasa según estatuto (Socio 5% = 0.05)
        tasa_mensual = 0.05 
        
        if st.button("Ver Tabla de Amortización"):
            tabla = generar_amortizacion(monto, plazo, tasa_mensual)
            st.write("### Proyección de Pagos")
            st.table(tabla)
            st.info(f"Cuota mensual estimada: **${tabla['Cuota'].iloc[0]}**")
            
            if st.button("Confirmar Solicitud"):
                st.success("Solicitud enviada al Administrador para aprobación.")

