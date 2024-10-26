# Importar librerías necesarias
import streamlit as st
import pandas as pd

# Leer archivo CSV
ruta_csv = 'horario_db.csv'  
df = pd.read_csv(ruta_csv)

# Definir las columnas relevantes
carrera_seleccion = 'Carrera'
semestre_grupo_col = 'Semestre y Grupo'
materias_col = 'Materia'
dia_col = 'Dia'
horario_col = 'Horario'
profesor_col = 'Profesor'

# Definir cuántas semanas de asistencia se quieren manejar
num_semanas = 16  # Cambia esto según cuántas semanas desees manejar
asistencia_cols = [f'Asistencia{i+1}' for i in range(num_semanas)]

# Asegurarse de que las columnas de asistencia existen en el DataFrame
for col in asistencia_cols:
    if col not in df.columns:
        df[col] = None  # Crear la columna con valores por defecto (None o NaN)

# Eliminar carreras duplicadas
if carrera_seleccion in df.columns:
    op_carreras = df[carrera_seleccion].drop_duplicates().tolist()

# Función para verificar si las semanas anteriores están completas
def verificar_asistencia_semana_anterior(df, semana_seleccion, carrera, semestre_grupo_seleccion, materia_seleccion, dias_seleccion):
    if semana_seleccion > 1:  # Si no es la primera semana
        semanas_anteriores = asistencia_cols[:semana_seleccion - 1]
        asistencia_anterior = df.loc[(df[carrera_seleccion] == carrera) & 
                                     (df[semestre_grupo_col] == semestre_grupo_seleccion) & 
                                     (df[materias_col] == materia_seleccion) & 
                                     (df[dia_col] == dias_seleccion), semanas_anteriores].notna().all(axis=1)
        return asistencia_anterior.all()
    return True  # Si es la primera semana, no hay restricciones

# Función para mostrar el horario de forma más estética incluyendo el nombre del profesor
def mostrar_horario(horarios, profesor):
    st.markdown("### 📅 **Horarios disponibles:**")
    for i, horario in enumerate(horarios, 1):
        st.markdown(f"**Horario {i}:** 🕒 `{horario}` - **Profesor:** 👨‍🏫 `{profesor}`")
    st.divider()  # Separador visual

# Función para registrar la asistencia
def registrar_asistencia():
    # Título general
    st.markdown("# 📊 **Sistema de Registro de Asistencia**")
    st.markdown("### Selecciona los detalles de tu clase para registrar la asistencia.")

    # Selectbox para elegir carrera
    carrera = st.selectbox("🎓 **Selecciona tu carrera**", op_carreras)
    
    if carrera:
        grupos_filtrados = df[df[carrera_seleccion] == carrera]
        op_semestre_grupo = grupos_filtrados[semestre_grupo_col].drop_duplicates().tolist()

        # Selectbox para elegir semestre y grupo
        semestre_grupo_seleccion = st.selectbox("📚 **Selecciona tu semestre y grupo**", op_semestre_grupo)

        if semestre_grupo_seleccion:
            materias_filtradas = grupos_filtrados[grupos_filtrados[semestre_grupo_col] == semestre_grupo_seleccion][materias_col].drop_duplicates()
            if not materias_filtradas.empty:
                materia_seleccion = st.selectbox("📖 **Selecciona tu materia**", materias_filtradas)

                if materia_seleccion:
                    dias_filtrados = grupos_filtrados[(grupos_filtrados[semestre_grupo_col] == semestre_grupo_seleccion) & 
                                                       (grupos_filtrados[materias_col] == materia_seleccion)][dia_col].drop_duplicates()

                    if not dias_filtrados.empty:
                        dias_seleccion = st.selectbox("🗓️ **Selecciona tu día de clases**", dias_filtrados)

                        if dias_seleccion:
                            # Filtrar los horarios y el profesor correspondiente
                            horarios_filtrados = grupos_filtrados[(grupos_filtrados[semestre_grupo_col] == semestre_grupo_seleccion) &
                                                                   (grupos_filtrados[materias_col] == materia_seleccion) & 
                                                                   (grupos_filtrados[dia_col] == dias_seleccion)][horario_col].drop_duplicates()
                            profesor = grupos_filtrados[(grupos_filtrados[semestre_grupo_col] == semestre_grupo_seleccion) & 
                                                        (grupos_filtrados[materias_col] == materia_seleccion) & 
                                                        (grupos_filtrados[dia_col] == dias_seleccion)][profesor_col].values[0]
                            
                            # Mostrar los horarios junto con el nombre del profesor
                            mostrar_horario(horarios_filtrados.tolist(), profesor)

                            # Seleccionar la semana para registrar la asistencia
                            semana_seleccion = st.selectbox("🗂️ **Selecciona la semana**", range(1, num_semanas + 1))

                            # Validación de asistencia de semanas anteriores
                            if not verificar_asistencia_semana_anterior(df, semana_seleccion, carrera, semestre_grupo_seleccion, materia_seleccion, dias_seleccion):
                                st.error(f"⚠️ **Error:** Debes ingresar la asistencia de la semana {semana_seleccion - 1} antes de registrar la semana {semana_seleccion}.")
                            else:
                                # Mostrar los botones de asistencia
                                asistencia = st.radio("👨‍🏫 **¿El profesor asistió a la clase?**", ("Presente", "Ausente"))

                                if st.button("📥 Registrar Asistencia"):
                                    # Asignar 1 para presente y 0 para ausente
                                    asistencia_valor = 1 if asistencia == "Presente" else 0

                                    # Actualizar el DataFrame con la asistencia
                                    df.loc[(df[carrera_seleccion] == carrera) & 
                                           (df[semestre_grupo_col] == semestre_grupo_seleccion) & 
                                           (df[materias_col] == materia_seleccion) & 
                                           (df[dia_col] == dias_seleccion), asistencia_cols[semana_seleccion - 1]] = asistencia_valor

                                    # Guardar el DataFrame actualizado en el archivo CSV
                                    df.to_csv(ruta_csv, index=False)
                                    st.success("✅ **Asistencia registrada correctamente.**")
                                    st.balloons()
                                    st.markdown("🎉 ¡**Excelente! La asistencia ha sido registrada correctamente.**")
