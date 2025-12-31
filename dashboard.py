import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Barça Media Monitor", page_icon="⚽", layout="wide")

def load_data():
    try:
        conn = sqlite3.connect("reputation.db")
        df = pd.read_sql_query("SELECT * FROM news", conn)
        conn.close()
        df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.date
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- BARRA LATERAL ---
    st.sidebar.header("Filtros de Análisis")

    sentimientos_disponibles = list(df["sentiment"].unique())
    sentimiento_filtro = st.sidebar.multiselect(
        "Selecciona Sentimiento:",
        options=sentimientos_disponibles,
        default=sentimientos_disponibles
    )

    fuentes_reales = sorted(list(df["source"].unique()))
    opciones_fuente = ["All"] + fuentes_reales

    seleccion_fuente = st.sidebar.selectbox(
        "Selecciona Fuente:",
        options=opciones_fuente,
        index=0
    )

    if seleccion_fuente == "All":
        fuentes_a_mostrar = fuentes_reales
    else:
        fuentes_a_mostrar = [seleccion_fuente]

    df_filtrado = df[
        (df["sentiment"].isin(sentimiento_filtro)) & 
        (df["source"].isin(fuentes_a_mostrar))
    ]

    # --- CUERPO PRINCIPAL ---
    st.title("FC Barcelona - Media Reputation Monitor")

    if not df_filtrado.empty:

        col1, col2, col3 = st.columns(3)

        dominante = df_filtrado["sentiment"].mode().iloc[0]
        
        col1.metric("Noticias", len(df_filtrado))
        col2.metric("Clima General", dominante.upper())
        col3.metric("Fuentes", df_filtrado["source"].nunique())

        st.write("---")
        total = len(df_filtrado)
        negativas = len(df_filtrado[df_filtrado["sentiment"] == "negative"])
        porcentaje_negativo = (negativas / total) * 100

        if dominante == "negative" or porcentaje_negativo > 40:
            st.error(f"⚠️ **Alerta de Reputación:** Se detecta un volumen crítico de noticias negativas ({porcentaje_negativo:.1f}%).")
        elif dominante == "positive":
            st.success(f"✅ **Salud de Marca Optima:** El sentimiento predominante es positivo.")
        else:
            st.info("⚖️ **Panorama Equilibrado:** La cobertura es informativa y balanceada.")

        st.divider()

        c_izq, c_der = st.columns(2)
        
        with c_izq:
                    st.subheader("Cuota de Sentimiento")
                    
                    df_pie = df_filtrado.copy()
                    df_pie = df_pie.dropna(subset=['sentiment'])
                    
                    if not df_pie.empty:

                        counts = df_pie['sentiment'].value_counts().reset_index()
                        counts.columns = ['sentiment', 'total']

                        fig_donut = px.pie(
                            counts, 
                            values='total', 
                            names='sentiment', 
                            hole=0.5,
                            color='sentiment',
                            color_discrete_map={
                                "positive": "#2E8B57", 
                                "negative": "#8E1B1B", 
                                "neutral": "#7F8C8D"
                            }
                        )
                        
                        fig_donut.update_layout(
                            margin=dict(t=30, b=30, l=10, r=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            showlegend=True
                        )

                        st.plotly_chart(fig_donut, use_container_width=True, key="donut_reputation_final")
                    else:
                        st.info("No hay datos de sentimiento para mostrar.")
        
        with c_der:

            fuentes_count = df_filtrado["source"].value_counts().reset_index()
            fuentes_count.columns = ['Medio', 'Cantidad']
            
            fig_bar = px.bar(
                fuentes_count, 
                x='Medio', 
                y='Cantidad', 
                color='Medio', 
                title="Cantidad de Noticias por Medio"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Detalle de los Artículos")
        st.dataframe(df_filtrado[["publishedAt", "source", "title", "sentiment"]], use_container_width=True, hide_index=True)
    else:
        st.warning("No hay noticias para los filtros seleccionados.")
else:
    st.error("No se encontró la base de datos.")