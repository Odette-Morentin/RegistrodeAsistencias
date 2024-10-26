# Importar librerías necesarias
import streamlit as st
import pandas as pd

def mostrar_horario():
    csv_file = 'horario_db.csv'  # Reemplaza con el nombre de tu archivo CSV

    # Título principal de la aplicación con estilo
    st.markdown("# 📅 **Visualización del Horario de Clases**")

    # Subtítulo para la sección
    st.markdown("### 🗓️ **Consulta y visualiza los horarios disponibles de manera organizada**")
    
    # Divisor visual
    st.divider()

    df = pd.read_csv(csv_file)

    # Filtrar las columnas que contienen datos (descartar columnas con solo valores NaN o vacíos)
    df_filtered = df.dropna(axis=1, how='all')

    # Si después de filtrar hay columnas que mostrar
    if not df_filtered.empty:
        # Mostrar el DataFrame filtrado
        st.markdown("#### Horarios de Clases Disponibles:")
        st.dataframe(df_filtered)  # Mostrar la tabla de horarios

        # Divisor visual
        st.divider()

        # Información adicional sobre los datos mostrados
        st.info("🔍 **Consejo:** Solo se muestran las columnas con datos. Puedes hacer scroll en la tabla para explorar todos los horarios disponibles.")
    else:
        st.warning("⚠️ **Advertencia:** No hay columnas con datos disponibles para mostrar.")

