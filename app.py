import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import base64

# Función para convertir imagen a base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Función para generar el PDF y guardarlo en un archivo temporal
def generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario, file_path):
    pdf = FPDF()
    pdf.add_page()

    # Añadir el logo
    logo_path = "logo.png"
    pdf.image(logo_path, x=10, y=10, w=469/5, h=112/5)  # Ajusta el tamaño del logo a 469x112 píxeles
    pdf.ln(30)  # Espacio para el título

    # Título principal
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resultados por escuela - Prueba Estatal de Inglés 2024", ln=True, align="C")
    pdf.ln(10)
    
    # Información de la escuela
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Escuela: {escuela}", ln=True)
    pdf.cell(200, 10, txt=f"Modalidad: {modalidad}", ln=True)
    pdf.ln(10)

    # Añadir tablas de frecuencias con porcentaje
    pdf.set_font("Arial", size=10)
    
    pdf.cell(100, 10, txt="Tabla de Frecuencias: Gramática", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_gramatica)):
        pdf.cell(80, 10, txt=f"{tabla_gramatica.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Porcentaje']:.2f}%", border=1)
        pdf.ln()
    pdf.ln(10)

    pdf.cell(100, 10, txt="Tabla de Frecuencias: Vocabulario", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_vocabulario)):
        pdf.cell(80, 10, txt=f"{tabla_vocabulario.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Porcentaje']:.2f}%", border=1)
        pdf.ln()
    
    # Ajustar posición para pie de página (10 mm desde el borde inferior)
    pdf.ln(10)  # Espacio adicional para asegurar que el pie de página esté visible

    # Añadir la leyenda al final de la página
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 10, txt="La información proporcionada en esta página es suministrada por el Centro de Evaluación Educativa del Estado de Yucatán con fines exclusivamente informativos", align='C')

    # Guardar el PDF en un archivo temporal
    pdf.output(file_path)

# Cargar datos desde la ruta especificada
df = pd.read_csv('Resultados.csv')

# Configuración de la página
st.set_page_config(page_title="Resultados por escuela - Prueba Estatal de Inglés", layout="wide")

# Convertir la imagen del logo a base64
logo_path = "logo.png"
logo_base64 = image_to_base64(logo_path)

# Mostrar el logo arriba del título en la parte superior de la página
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="data:image/png;base64,{logo_base64}" width="235" height="56" style="margin-bottom: 10px;">
        <h1>Resultados por escuela - Prueba Estatal de Inglés 2024</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Filtro por CCT
cct_input = st.text_input("Escribe el CCT:")

# Filtrar DataFrame según el valor de CCT ingresado
df_filtered = df[df['CCT'] == cct_input]

if not df_filtered.empty:
    # Extraer datos necesarios
    escuela = df_filtered['Escuela'].values[0]
    modalidad = df_filtered['Modalidad'].values[0]
    tabla_gramatica_pdf = df_filtered[['Nivel Gramática', 'Estudiantes Gramática', 'Porcentaje Gramática']]
    tabla_vocabulario_pdf = df_filtered[['Nivel Vocabulario', 'Estudiantes Vocabulario', 'Porcentaje Vocabulario']]
    
    tabla_gramatica_visible = tabla_gramatica_pdf.rename(columns={
        'Nivel Gramática': 'Nivel',
        'Estudiantes Gramática': 'Estudiantes'
    })
    
    tabla_vocabulario_visible = tabla_vocabulario_pdf.rename(columns={
        'Nivel Vocabulario': 'Nivel',
        'Estudiantes Vocabulario': 'Estudiantes'
    })

    # Mostrar tablas en la aplicación
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Gramática**")
        st.table(tabla_gramatica_visible)

    with col2:
        st.write("**Vocabulario**")
        st.table(tabla_vocabulario_visible)

    # Botón para generar el PDF
    if st.button("Generar reporte"):
        temp_file_path = "reporte.pdf"
        generar_pdf(escuela, modalidad, tabla_gramatica_pdf, tabla_vocabulario_pdf, temp_file_path)
        
        # Proporcionar un enlace para descargar el archivo PDF
        st.markdown(
            f"""
            <a href="data:file/pdf;base64,{base64.b64encode(open(temp_file_path, "rb").read()).decode()}" download="reporte.pdf" style="display: inline-block; background-color: red; color: white; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px;">Descargar PDF</a>
            """,
            unsafe_allow_html=True
        )

    # Mostrar la leyenda en la página principal
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px; margin-top: 20px;'>
            La información proporcionada en esta página es suministrada por el Centro de Evaluación Educativa del Estado de Yucatán con fines exclusivamente informativos
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.write("CCT no encontrado. Por favor ingresa un CCT válido.")
