import os
import subprocess
import sys

# Forzar la instalación de dependencias si no están presentes usando --user para evitar problemas de permisos
def install_missing_packages():
    REQUIRED_LIBRARIES = ["plotly", "pandas", "streamlit", "openpyxl"]
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", lib])

install_missing_packages()

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Ruta del archivo por defecto
DEFAULT_FILE_PATH = "CONTROL FACTURACION Y COBRANZA FEB 25.xlsx"

# Función para cargar los datos
def load_data(file):
    try:
        xls = pd.ExcelFile(file)
        df = pd.read_excel(xls, sheet_name="BD", skiprows=1, usecols=[1, 2, 3, 4, 5, 6, 7])
        df.columns = ["Cliente", "Facturado", "Mes_Facturado", "Cobrado", "Mes_Cobrado", "Saldo", "Mes_Saldo"]
        df["Facturado"] = pd.to_numeric(df["Facturado"], errors="coerce").fillna(0)
        df["Cobrado"] = pd.to_numeric(df["Cobrado"], errors="coerce").fillna(0)
        df["Saldo"] = pd.to_numeric(df["Saldo"], errors="coerce").fillna(0)
        df["Mes_Facturado"] = pd.to_datetime(df["Mes_Facturado"], errors="coerce")
        df["Mes_Cobrado"] = pd.to_datetime(df["Mes_Cobrado"], errors="coerce")
        df["Mes_Saldo"] = pd.to_datetime(df["Mes_Saldo"], errors="coerce")
        
        # Filtrar solo datos del año 2025
        df = df[df["Mes_Facturado"].dt.year == 2025]
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Interfaz para subir archivo
st.title("Dashboard de Facturación y Cobranza 2025")
archivo_subido = st.file_uploader("Sube un archivo Excel de facturación", type=["xlsx"])

# Determinar qué archivo usar
df = None
if archivo_subido is not None:
    df = load_data(archivo_subido)
else:
    if os.path.exists(DEFAULT_FILE_PATH):
        df = load_data(DEFAULT_FILE_PATH)
    else:
        st.error("No se encontró el archivo predeterminado y no se ha subido ningún archivo.")
        st.stop()

# Botón para recargar datos
if st.button("Recargar datos"):
    st.experimental_rerun()

# Filtro de cliente
clientes = df["Cliente"].unique()
cliente_seleccionado = st.selectbox("Selecciona un cliente", options=["Todos"] + list(clientes))

# Filtrar datos según selección
df_filtrado = df if cliente_seleccionado == "Todos" else df[df["Cliente"] == cliente_seleccionado]

# Métricas clave
facturado_total = df_filtrado["Facturado"].sum()
cobrado_total = df_filtrado["Cobrado"].sum()
saldo_total = df_filtrado["Saldo"].sum()

st.metric("Facturado Total", f"${facturado_total:,.2f}")
st.metric("Cobrado Total", f"${cobrado_total:,.2f}")
st.metric("Saldo Pendiente", f"${saldo_total:,.2f}")

# Gráfico de tendencias
df_trend = df_filtrado.groupby("Mes_Facturado")["Facturado"].sum().reset_index()
fig = px.line(df_trend, x="Mes_Facturado", y="Facturado", title="Tendencia de Facturación", markers=True)
st.plotly_chart(fig)

# Mostrar tabla con detalles
st.dataframe(df_filtrado)
