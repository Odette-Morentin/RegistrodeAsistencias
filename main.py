# Importar librerías y documentos necesarios 
import streamlit as st
import inicio
import Registro_asistencia
import visualizar_clases
import reportes_estadisticas  # Importar el módulo de reportes
import pandas as pd

# Menú de opciones y lógica de cada una
def main():
    menu_principal = ["Inicio", "Registro de asistencia", "Visualizar Clases", "Reportes y Estadísticas"]
    selected = st.sidebar.selectbox("Opciones", menu_principal)

    # Cargar datos una vez al inicio
    leer_csv = pd.read_csv('horario_db.csv')

    match selected:
        case "Inicio":
            inicio.guiaUsuario()
        case "Registro de asistencia":
            Registro_asistencia.registrar_asistencia()  # Registro de asistencia
        case "Visualizar Clases":
            visualizar_clases.mostrar_horario()  # Visualización de clases
        case "Reportes y Estadísticas":
            st.title("Reportes y Estadísticas")
            reportes_estadisticas.reportes()

if __name__ == "__main__":
    main()
