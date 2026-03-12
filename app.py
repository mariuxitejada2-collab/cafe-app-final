import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="SISTEMA C.A.F.E.", layout="centered")

# --- 2. BASE DE DATOS TEMPORAL (Simulada en memoria) ---
if 'db_usuarios' not in st.session_state:
    # Usuario Admin por defecto
    st.session_state.db_usuarios = {
        "admin": {"clave": "cafe2026", "rol": "admin", "nombre": "Administrador General"}
    }

# --- 3. LÓGICA DE NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# --- PANTALLA DE ACCESO (LOGIN / REGISTRO) ---
if not st.session_state.autenticado:
    st.title("🏦 BIENVENIDO A C.A.F.E.")
    pestana = st.tabs(["Iniciar Sesión", "Registrarse (Nuevo Socio)"])

    # FORMULARIO DE INICIO DE SESIÓN
    with pestana[0]:
        user_input = st.text_input("Usuario", key="login_user")
        pass_input = st.text_input("Contraseña", type="password", key="login_pass")
        if st.button("Entrar al Sistema"):
            if user_input in st.session_state.db_usuarios and st.session_state.db_usuarios[user_input]["clave"] == pass_input:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = user_input
                st.session_state.rol = st.session_state.db_usuarios[user_input]["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

    # FORMULARIO DE REGISTRO
    with pestana[1]:
        st.subheader("Crea tu cuenta de Socio")
        nuevo_user = st.text_input("Crea un nombre de usuario", help="Ejemplo: juanperez20")
        nombre_real = st.text_input("Nombre Completo")
        nueva_clave = st.text_input("Crea una contraseña", type="password")
        confirmar_clave = st.text_input("Confirma tu contraseña", type="password")
        
        if st.button("Finalizar Registro"):
            if nuevo_user in st.session_state.db_usuarios:
                st.warning("⚠️ Este usuario ya existe. Intenta con otro.")
            elif nueva_clave != confirmar_clave:
                st.error("❌ Las contraseñas no coinciden.")
            elif len(nueva_clave) < 4:
                st.error("❌ La contraseña debe tener al menos 4 caracteres.")
            else:
                # Guardar nuevo socio en la "base de datos"
                st.session_state.db_usuarios[nuevo_user] = {
                    "clave": nueva_clave,
                    "rol": "socio",
                    "nombre": nombre_real,
                    "ahorro": 0.0  # Inicia en cero
                }
                st.success("✅ ¡Registro exitoso! Ahora puedes iniciar sesión.")

# --- PANTALLA PRINCIPAL (DASHBOARD) ---
else:
    user_data = st.session_state.db_usuarios[st.session_state.usuario_actual]
    
    # Barra lateral para cerrar sesión
    st.sidebar.title(f"👤 {user_data['nombre']}")
    st.sidebar.write(f"Rol: **{user_data['rol'].upper()}**")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # VISTA ADMINISTRADOR
    if st.session_state.rol == "admin":
        st.title("📊 Panel de Control Administrativo")
        st.write("Vista global de la Caja de Ahorro Fe y Esperanza.")
        # Aquí puedes pegar el código de las métricas (Capital, Préstamos, etc.) que hicimos antes.
        st.metric("Capital Total FIC", "$5,000.00")
        st.subheader("Socios Registrados")
        st.write(pd.DataFrame.from_dict(st.session_state.db_usuarios, orient='index')[['nombre', 'rol']])

    # VISTA SOCIO
    else:
        st.title(f"👋 Hola, {user_data['nombre']}")
        st.metric("Mi Ahorro Acumulado", f"${user_data.get('ahorro', 0.0)}")
        
        st.divider()
        st.subheader("💰 Solicitar un Préstamo")
        monto = st.number_input("¿Cuánto dinero necesitas?", min_value=50, step=10)
        meses = st.slider("Plazo en meses", 1, 12, 3)
        
        # Cálculo de cuota simple (Interés del 5% mensual según estatuto)
        interes_total = monto * 0.05 * meses
        cuota_mensual = (monto + interes_total) / meses
        
        st.info(f"Proyección: Pagarás **{meses} cuotas** de **${cuota_mensual:.2f}**")
        
        if st.button("Enviar Solicitud"):
            st.success("📩 Solicitud enviada. El administrador revisará tu capacidad de pago.")

