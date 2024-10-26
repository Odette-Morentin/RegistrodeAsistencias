import streamlit as st

# Función que saluda al usuario y explica cómo navegar por el sitio
def guiaUsuario() -> None:
    # Título principal con estilo
    st.markdown("# 👋 **Bienvenido a la Aplicación de Control de Asistencia de Profesores**")
    
    # Breve descripción inicial
    st.write("Esta aplicación facilita el control de la asistencia de profesores de manera rápida y eficiente. ¡Explora las funcionalidades a continuación!")

    # Sección: Descripción de la aplicación
    st.markdown("## 📝 **Descripción de la Aplicación**")
    st.write("""
    La aplicación está diseñada para gestionar el registro de asistencia de los profesores en diferentes materias y grupos. A continuación, te presentamos las funcionalidades principales:
    """)

    # Lista de funcionalidades con íconos y texto destacado
    st.markdown("""
    ### Funcionalidades Principales:
    - ✅ **Registrar asistencia:** Los profesores pueden registrar si impartieron sus clases programadas.
    - 📅 **Visualizar clases:** Puedes consultar fácilmente el horario de clases.
    - 📊 **Generar reportes:** Proporciona reportes detallados sobre la asistencia, organizados por materia, grupo y estadísticas globales.
    """)

    # Sección: Cómo Navegar
    st.markdown("## 🧭 **Cómo Navegar**")
    st.write("""
    Para explorar las diferentes funcionalidades de la aplicación, sigue estos pasos:
    """)
    
    # Instrucciones de navegación con numeración
    st.markdown("""
    1. **Menú lateral:** Usa el menú desplegable en el lado izquierdo de la pantalla para acceder a las diferentes secciones.
    2. **Selecciona una opción:** Haz clic en la opción que deseas explorar, como el registro de asistencia o los reportes.
    3. **Sigue las instrucciones en cada sección:** Cada funcionalidad te guiará de manera intuitiva a través del proceso.
    """)

    # Pie de página con mensaje adicional
    st.markdown("### 🎯 ¡Empieza a explorar y gestiona la asistencia de manera eficiente!")
