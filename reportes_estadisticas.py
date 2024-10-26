import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF
from io import BytesIO
import os

# Función para guardar gráficos como imágenes en el sistema de archivos temporalmente
def guardar_grafico(fig):
    temp_filename = "temp_grafico.png"  # Nombre temporal
    fig.savefig(temp_filename, format="png")
    return temp_filename

# Función para exportar la gráfica actual a PDF con su descripción
def exportar_grafico_a_pdf(titulo, descripcion, figura):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, titulo, ln=True, align='C')
    pdf.ln(10)

    # Descripción
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, descripcion)
    pdf.ln(10)

    # Guardar el gráfico en el PDF
    imagen_grafico = guardar_grafico(figura)  # Guardamos la imagen temporalmente
    pdf.image(imagen_grafico, x=10, y=None, w=170)  # Ajustar el tamaño de la imagen según sea necesario

    # Guardar el archivo PDF
    output_filename = 'reporte_asistencia_grafica.pdf'
    pdf.output(output_filename)

    # Eliminar el archivo temporal después de guardarlo en el PDF
    os.remove(imagen_grafico)

    return output_filename

# Leer el archivo CSV
leer_csv = pd.read_csv('horario_db.csv')

# Definir las columnas de asistencia (Asistencia1, Asistencia2, ..., Asistencia16)
asistencia_cols = [col for col in leer_csv.columns if 'Asistencia' in col]
profesor_col = 'Profesor'
materia_col = 'Materia'

# Función para filtrar solo las columnas de asistencia válidas (0 o 1, excluyendo NaN)
def filtrar_columnas_llenas(df):
    return df[asistencia_cols].apply(lambda col: col.dropna().isin([0, 1]).all(), axis=0)

# Función para generar gráfico por profesor
def reporte_por_profesor(df, profesor):
    df_profesor = df[df[profesor_col] == profesor]
    columnas_llenas = filtrar_columnas_llenas(df_profesor)
    columnas_llenas = columnas_llenas[columnas_llenas].index
    df_profesor = df_profesor.loc[:, columnas_llenas]

    clases_impartidas = (df_profesor == 1).sum().sum()
    clases_perdidas = (df_profesor == 0).sum().sum()
    total_clases = clases_impartidas + clases_perdidas

    st.subheader(f'📊 **Reporte de Asistencia para {profesor}**')
    fig, ax = plt.subplots()
    ax.pie([clases_impartidas, clases_perdidas], labels=['Clases Impartidas', 'Clases Perdidas'],
           autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'])
    ax.axis('equal')
    st.pyplot(fig)
    
    descripcion = f"""
    **Clases Impartidas:** {clases_impartidas}  
    **Clases Perdidas:** {clases_perdidas}  
    **Total de Clases:** {total_clases}
    """
    
    st.markdown(descripcion)
    st.markdown("### 📘 **Interpretación:**")
    st.write(f"El profesor *{profesor}* tenía un total de *{total_clases}* clases programadas. Impartió *{clases_impartidas}* y perdió *{clases_perdidas}* clases.")

    # Guardar el gráfico y la descripción en session_state
    st.session_state['grafico_actual'] = {"titulo": f"Reporte de Asistencia para {profesor}", "descripcion": descripcion, "figura": fig}

# Función para generar gráfico por materia
def reporte_por_materia(df, materia):
    df_materia = df[df[materia_col] == materia]
    columnas_llenas = filtrar_columnas_llenas(df_materia)
    columnas_llenas = columnas_llenas[columnas_llenas].index
    df_materia = df_materia.loc[:, columnas_llenas]

    clases_impartidas = (df_materia == 1).sum().sum()
    clases_perdidas = (df_materia == 0).sum().sum()
    total_clases = clases_impartidas + clases_perdidas

    st.subheader(f'📊 **Reporte de Asistencia para la Materia: {materia}**')
    fig, ax = plt.subplots()
    ax.bar(['Clases Impartidas', 'Clases Perdidas'], [clases_impartidas, clases_perdidas], color=['#66c2a5', '#fc8d62'])
    ax.set_ylabel('Número de Clases')
    st.pyplot(fig)

    descripcion = f"""
    **Clases Impartidas:** {clases_impartidas}  
    **Clases Perdidas:** {clases_perdidas}  
    **Total de Clases:** {total_clases}
    """
    
    st.markdown(descripcion)
    st.markdown("### 📘 **Interpretación:**")
    st.write(f"Para la materia *{materia}*, se han impartido **{clases_impartidas}** clases y se han perdido **{clases_perdidas}**.")

    # Guardar el gráfico y la descripción en session_state
    st.session_state['grafico_actual'] = {"titulo": f"Reporte de Asistencia para la Materia: {materia}", "descripcion": descripcion, "figura": fig}

# Función para generar estadísticas globales
def estadisticas_globales(df):
    columnas_llenas = filtrar_columnas_llenas(df)
    columnas_llenas = columnas_llenas[columnas_llenas].index
    df = df.loc[:, columnas_llenas]

    clases_impartidas = (df == 1).sum().sum()
    clases_perdidas = (df == 0).sum().sum()
    total_clases = clases_impartidas + clases_perdidas

    st.subheader('📊 **Estadísticas Globales de Asistencia**')
    fig, ax = plt.subplots()
    ax.pie([clases_impartidas, clases_perdidas], labels=['Clases Impartidas', 'Clases Perdidas'],
           autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'])
    ax.axis('equal')
    st.pyplot(fig)
    
    descripcion = f"""
    **Total de Clases:** {total_clases}  
    **Clases Impartidas:** {clases_impartidas}  
    **Clases Perdidas:** {clases_perdidas}
    """
    
    st.markdown(descripcion)
    st.markdown("### 📘 **Interpretación:**")
    st.write(f"De un total de *{total_clases}* clases programadas, se impartieron *{clases_impartidas}* y se perdieron *{clases_perdidas}*.")

    # Guardar el gráfico y la descripción en session_state
    st.session_state['grafico_actual'] = {"titulo": "Estadísticas Globales de Asistencia", "descripcion": descripcion, "figura": fig}

# Función principal para generar reportes
def reportes():
    st.markdown("# 📊 **Sistema de Reportes de Asistencia**")
    st.markdown("### 📝 *Genera reportes detallados de asistencia por profesor, materia o estadísticas globales.*")

    # Reporte por profesor
    st.markdown("## 👨‍🏫 **Reporte por Profesor**")
    profesor = st.selectbox("Selecciona un profesor", leer_csv[profesor_col].unique())
    if st.button("Generar Reporte por Profesor"):
        reporte_por_profesor(leer_csv, profesor)

    # Reporte por materia
    st.markdown("## 📚 **Reporte por Materia**")
    materia = st.selectbox("Selecciona una materia", leer_csv[materia_col].unique())
    if st.button("Generar Reporte por Materia"):
        reporte_por_materia(leer_csv, materia)

    # Estadísticas globales
    st.markdown("## 🌍 **Estadísticas Globales**")
    if st.button("Generar Estadísticas Globales"):
        estadisticas_globales(leer_csv)

    # Botón para exportar la gráfica actual a PDF
    if 'grafico_actual' in st.session_state and st.button("Exportar Gráfico Actual a PDF"):
        grafico_actual = st.session_state['grafico_actual']
        filename = exportar_grafico_a_pdf(grafico_actual['titulo'], grafico_actual['descripcion'], grafico_actual['figura'])
        st.success(f"PDF generado exitosamente: {filename}")