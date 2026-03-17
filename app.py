import streamlit as st
import requests
import datetime

# === CONFIGURACIÓN DE N8N ===
N8N_WEBHOOK_URL = "https://n8n.srv1491231.hstgr.cloud/webhook/formulario-futbol"

# === MAGIA DE DISEÑO (CSS) PARA EL BOTÓN ===
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #8FBC8F;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
}
div.stButton > button:first-child:hover {
    background-color: #7DAA7D;
}
</style>
""", unsafe_allow_html=True)

# === INTERFAZ WEB ===
st.title("ex.angelica")
st.write("Ingreso de estadísticas para el modelo de predicción")

col_izq, col_der = st.columns(2)

equipos_lista = [
    "Nacional", "America", "Millonarios", "Santa Fe", "Junior", 
    "Cali", "Once Caldas", "Pereira", "Medellin", "Tolima"
]

# --- COLUMNA LOCAL ---
with col_izq:
    st.subheader("Local")
    equipo_l = st.selectbox("Equipo L (Nombre):", equipos_lista, key="local_team")
    gol_l = st.number_input("Goles Local:", min_value=0, step=1)
    corners_l = st.number_input("Tiros de Esquina Local:", min_value=0, step=1)
    tiros_arco_l = st.number_input("Tiros a Arco Local:", min_value=0, step=1)
    amarillas_l = st.number_input("Tarjetas Amarillas Local:", min_value=0, step=1)
    rojas_l = st.number_input("Tarjetas Rojas Local:", min_value=0, step=1)

# --- COLUMNA DERECHA ---
with col_der:
    st.subheader("Datos del Partido")
    fecha = st.date_input("Fecha:", format="DD/MM/YYYY")
    gol_v = st.number_input("Goles Visitante:", min_value=0, step=1)
    corners_v = st.number_input("Tiros de Esquina Visitante:", min_value=0, step=1)
    tiros_arco_v = st.number_input("Tiros a Arco Visitante:", min_value=0, step=1)
    amarillas_v = st.number_input("Tarjetas Amarillas Visitante:", min_value=0, step=1)
    rojas_v = st.number_input("Tarjetas Rojas Visitante:", min_value=0, step=1)

st.write("---") 

# --- CONDICIONES DEL PARTIDO ---
col_inf_izq, col_inf_der = st.columns(2)

with col_inf_izq:
    arbitro = st.text_input("Nombre del Árbitro:")

with col_inf_der:
    temperatura = st.number_input("Temperatura (°C):", step=1)

st.write("---") 

# --- DATOS DE EVALUACIÓN ---
st.subheader("Evaluación del Equipo")
col_eval1, col_eval2, col_eval3, col_eval4 = st.columns(4)

with col_eval1:
    ronda = st.number_input("Número de Ronda:", min_value=1, step=1)

with col_eval2:
    valla_invicta = st.selectbox("Valla Invicta:", ["Sí", "No"])

with col_eval3:
    condicion = st.selectbox("Condición:", ["Local", "Visitante"])

with col_eval4:
    resultado = st.selectbox("Resultado:", ["Ganó", "Perdió", "Empató"])

# --- BOTÓN Y ENVÍO ---
if st.button("Enviar"):
    if not equipo_l:
        st.warning("⚠️ Por favor, selecciona un equipo local.")
    else:
        # Paquete de datos actualizado
        datos_para_n8n = {
            "encabezado": "ex.angelica",
            "equipo_local": equipo_l,
            "fecha": fecha.strftime("%d/%m/%Y"),
            "arbitro": arbitro,
            "temperatura": temperatura,
            "gol_local": gol_l,
            "corners_local": corners_l,
            "tiros_arco_local": tiros_arco_l,
            "amarillas_local": amarillas_l,
            "rojas_local": rojas_l,
            "gol_visitante": gol_v,
            "corners_visitante": corners_v,
            "tiros_arco_visitante": tiros_arco_v,
            "amarillas_visitante": amarillas_v,
            "rojas_visitante": rojas_v,
            "ronda": ronda,
            "valla_invicta": valla_invicta,
            "condicion": condicion,
            "resultado": resultado
        }
        
        headers = {
            "ngrok-skip-browser-warning": "true"
        }
        
        try:
            respuesta = requests.post(N8N_WEBHOOK_URL, json=datos_para_n8n, headers=headers)
            if respuesta.status_code == 200:
                st.success("✅ ¡Datos enviados correctamente a n8n!")
            else:
                st.error(f"❌ n8n respondió con un error: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"🔌 No se pudo conectar. Detalle: {e}")
