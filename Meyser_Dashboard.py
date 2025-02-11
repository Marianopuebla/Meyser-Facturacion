import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos limpios
def load_data():
    file_path = "CONTROL FACTURACION Y COBRANZA FEB 25.xlsx"
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="BD", skiprows=1, usecols=[1, 2, 3, 4, 5, 6, 7])
    df.columns = ["Cliente", "Facturado", "Mes_Facturado", "Cobrado", "Mes_Cobrado", "Saldo", "Mes_Saldo"]
    df["Facturado"] = pd.to_numeric(df["Facturado"], errors="coerce").fillna(0)
    df["Cobrado"] = pd.to_numeric(df["Cobrado"], errors="coerce").fillna(0)
    df["Saldo"] = pd.to_numeric(df["Saldo"], errors="coerce").fillna(0)
    df["Mes_Facturado"] = pd.to_datetime(df["Mes_Facturado"], errors="coerce")
    df["Mes_Cobrado"] = pd.to_datetime(df["Mes_Cobrado"], errors="coerce")
    df["Mes_Saldo"] = pd.to_datetime(df["Mes_Saldo"], errors="coerce")
    return df

# Cargar datos
df = load_data()

# Configuración de la aplicación
st.title("Dashboard de Facturación y Cobranza")

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
