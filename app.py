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
def generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario, file_path, logo_path):
    pdf = FPDF()
    pdf.add_page()

    # Añadir el logo en la parte superior
    pdf.image(logo_path, x=10, y=8, w=40)  # Ajusta x, y y w según sea necesario
    
    # Título principal
    pdf.set_font("Arial", size=12)
    pdf.set_y(30)  # Ajustar la posición del título para que no se sobreponga al logo
    pdf.cell(200, 10, txt="Resultados por escuela - INEIIY 2024", ln=True, align="C")
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
st.set_page_config(page_title="Resultados por escuela - INEIIY 2024", layout="wide")

# Convertir la imagen del logo a base64 (opcional)
logo_path = "logo.png"

# Mostrar el logo arriba del título en la parte superior de la página
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="data:image/png;base64,{image_to_base64(logo_path)}" width="235" height="56" style="margin-bottom: 10px;">
        <h1>Resultados por escuela - INEIIY 2024</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Filtro por CCT
cct_input = st.text_input("Escribe el CCT:")

# Filtrar DataFrame según el valor de CCT ingresado
df_cct_filtered = df[df['CCT'] == cct_input]

if not df_cct_filtered.empty:
    # Filtro por Turno
    turno_options = df_cct_filtered['Turno'].unique()  # Obtener opciones únicas de turno
    turno_selected = st.selectbox("Selecciona el Turno:", turno_options)

    # Filtrar DataFrame según el valor de Turno seleccionado
    df_filtered = df_cct_filtered[df_cct_filtered['Turno'] == turno_selected]

    if not df_filtered.empty:
        # Mostrar Escuela y Modalidad asociadas al CCT
        escuela = df_filtered['Escuela'].iloc[0]
        modalidad = df_filtered['Modalidad'].iloc[0]
        st.write(f"**Escuela:** {escuela}")
        st.write(f"**Modalidad:** {modalidad}")

        # Filtrar valores no nulos para gráficos
        df_gramatica = df_filtered[df_filtered['Gramática'].notna()]
        df_vocabulario = df_filtered[df_filtered['Vocabulario'].notna()]

        # Contar la frecuencia de estudiantes
        freq_gramatica = df_gramatica['Gramática'].count()
        freq_vocabulario = df_vocabulario['Vocabulario'].count()

        # Lista de categorías en orden deseado
        categorias_ordenadas = ['Pre A1', 'A1', 'A2', 'Superior a A2']

        # Definir colores gradientes para los gráficos de sectores
        colores_gramatica = {
            'Pre A1': '#a2c9a0',  # Verde más claro
            'A1': '#7aab7e',
            'A2': '#4a8d54',
            'Superior a A2': '#2d5b30'  # Verde más oscuro
        }

        colores_vocabulario = {
            'Pre A1': '#f9f3a6',  # Amarillo más claro
            'A1': '#f3e46b',
            'A2': '#f1d236',
            'Superior a A2': '#f0b30f'  # Amarillo más oscuro
        }

        # Gráfico de sectores para Gramática con gradiente verde militar
        fig_gramatica = px.pie(df_gramatica, names='Gramática', 
                               category_orders={'Gramática': categorias_ordenadas},
                               color='Gramática',
                               color_discrete_map=colores_gramatica)
        fig_gramatica.update_layout(
            title={
                'text': f"Gramática<br><span style='font-size:12px'>Frecuencia: {freq_gramatica} estudiantes",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=120)
        )

        # Gráfico de sectores para Vocabulario con gradiente amarillo mostaza
        fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                                 category_orders={'Vocabulario': categorias_ordenadas},
                                 color='Vocabulario',
                                 color_discrete_map=colores_vocabulario)
        fig_vocabulario.update_layout(
            title={
                'text': f"Vocabulario<br><span style='font-size:12px'>Frecuencia: {freq_vocabulario} estudiantes",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=120)
        )

        # Crear dos columnas para los gráficos
        col1, col2 = st.columns(2)

        # Mostrar gráfico de Gramática en la primera columna
        col1.plotly_chart(fig_gramatica, use_container_width=True)

        # Mostrar gráfico de Vocabulario en la segunda columna
        col2.plotly_chart(fig_vocabulario, use_container_width=True)

        # Tabla de frecuencias en dos columnas
        st.subheader("Tabla de Frecuencias")
        
        # Crear DataFrames para las tablas con porcentaje (para el PDF)
        tabla_gramatica_pdf = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).fillna(0).reset_index()
        tabla_gramatica_pdf.columns = ['Nivel', 'Estudiantes']
        tabla_gramatica_pdf['Porcentaje'] = (tabla_gramatica_pdf['Estudiantes'] / freq_gramatica) * 100

        tabla_vocabulario_pdf = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).fillna(0).reset_index()
        tabla_vocabulario_pdf.columns = ['Nivel', 'Estudiantes']
        tabla_vocabulario_pdf['Porcentaje'] = (tabla_vocabulario_pdf['Estudiantes'] / freq_vocabulario) * 100
        
        col3, col4 = st.columns(2)

        # Tabla de Frecuencias de Gramática
        tabla_gramatica = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).fillna(0)
        tabla_gramatica = tabla_gramatica.reset_index()
        tabla_gramatica.columns = ['Nivel', 'Estudiantes']
        tabla_gramatica['Porcentaje'] = (tabla_gramatica['Estudiantes'] / freq_gramatica) * 100

        col3.table(tabla_gramatica)

        # Tabla de Frecuencias de Vocabulario
        tabla_vocabulario = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).fillna(0)
        tabla_vocabulario = tabla_vocabulario.reset_index()
        tabla_vocabulario.columns = ['Nivel', 'Estudiantes']
        tabla_vocabulario['Porcentaje'] = (tabla_vocabulario['Estudiantes'] / freq_vocabulario) * 100

        col4.table(tabla_vocabulario)
        
        # Botón para generar PDF
        if st.button("Generar PDF"):
            pdf_file_path = "reporte.pdf"
            generar_pdf(escuela, modalidad, tabla_gramatica_pdf, tabla_vocabulario_pdf, pdf_file_path, logo_path)
            
            # Descargar el archivo PDF
            with open(pdf_file_path, "rb") as f:
                pdf_data = f.read()
            b64_pdf = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="reporte.pdf">Descargar reporte PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Eliminar el archivo PDF temporal después de la descarga
            os.remove(pdf_file_path)
    else:
        st.write("No se encontraron datos para el CCT proporcionado y el turno seleccionado.")
else:
    st.write("No se encontraron datos para el CCT proporcionado.")
