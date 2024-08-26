import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO

import os
os.system('pip install -U kaleido')

# Función para convertir un gráfico Plotly a una imagen PNG
def fig_to_img(fig):
    img_bytes = fig.to_image(format="png")
    return img_bytes

# Función para generar el PDF
def generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario, img_gramatica, img_vocabulario):
    pdf = FPDF()
    pdf.add_page()

    # Título principal
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Resultados de la Prueba Estatal de Inglés", ln=True, align="C")
    pdf.ln(10)
    
    # Información de la escuela
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Escuela: {escuela}", ln=True)
    pdf.cell(200, 10, txt=f"Modalidad: {modalidad}", ln=True)
    pdf.ln(10)

    # Insertar imágenes de los gráficos
    pdf.image(BytesIO(img_gramatica), x=10, y=pdf.get_y(), w=100)
    pdf.image(BytesIO(img_vocabulario), x=110, y=pdf.get_y(), w=100)
    pdf.ln(85)

    # Añadir tablas de frecuencias
    pdf.set_font("Arial", size=9)
    pdf.cell(100, 10, txt="Tabla de Frecuencias: Gramática", ln=True)
    pdf.ln(5)

    # Tabla de Gramática con menor altura de celdas
    cell_height = 6  # Altura reducida para las celdas
    pdf.cell(60, cell_height, "Nivel", 1)
    pdf.cell(60, cell_height, "Estudiantes", 1)
    pdf.ln()
    for i in range(len(tabla_gramatica)):
        pdf.cell(60, cell_height, tabla_gramatica.iloc[i]['Nivel'], 1)
        pdf.cell(60, cell_height, str(tabla_gramatica.iloc[i]['Estudiantes']), 1)
        pdf.ln()

    pdf.ln(10)

    pdf.cell(100, 10, txt="Tabla de Frecuencias: Vocabulario", ln=True)
    pdf.ln(5)

    # Tabla de Vocabulario con menor altura de celdas
    pdf.cell(60, cell_height, "Nivel", 1)
    pdf.cell(60, cell_height, "Estudiantes", 1)
    pdf.ln()
    for i in range(len(tabla_vocabulario)):
        pdf.cell(60, cell_height, tabla_vocabulario.iloc[i]['Nivel'], 1)
        pdf.cell(60, cell_height, str(tabla_vocabulario.iloc[i]['Estudiantes']), 1)
        pdf.ln()

    return pdf

# Cargar datos desde la ruta especificada
df = pd.read_csv('Resultados.csv')

# Configuración de la página
st.set_page_config(page_title="Resultados de la Prueba Estatal de Inglés", layout="wide")

# Título del Dashboard
st.title("Resultados de la Prueba Estatal de Inglés")

# Filtro por CCT
cct_input = st.text_input("Escribe el CCT:")

# Filtrar DataFrame según el valor de CCT ingresado
df_filtered = df[df['CCT'] == cct_input]

# Lista de categorías en orden deseado
categorias_ordenadas = ['Pre A1', 'A1', 'A2', 'Superior a A2']

# Asignar colores específicos a cada categoría
colores = {
    'Pre A1': '#1f77b4',
    'A1': '#ff7f0e',
    'A2': '#2ca02c',
    'Superior a A2': '#d62728'
}

if not df_filtered.empty:
    # Mostrar Escuela y Modalidad asociadas al CCT
    escuela = df_filtered['Escuela'].iloc[0]
    modalidad = df_filtered['Modalidad'].iloc[0]
    st.write(f"**Escuela:** {escuela}")
    st.write(f"**Modalidad:** {modalidad}")

    # Filtrar valores no nulos para gráficos
    df_gramatica = df_filtered[df_filtered['Gramática'].isin(categorias_ordenadas)]
    df_vocabulario = df_filtered[df_filtered['Vocabulario'].isin(categorias_ordenadas)]

    # Contar la frecuencia de estudiantes
    freq_gramatica = df_gramatica['Gramática'].count()
    freq_vocabulario = df_vocabulario['Vocabulario'].count()

    # Gráfico de sectores para Gramática con colores y orden constante
    fig_gramatica = px.pie(df_gramatica, names='Gramática', 
                           category_orders={'Gramática': categorias_ordenadas},
                           color='Gramática',
                           color_discrete_map=colores)
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

    # Gráfico de sectores para Vocabulario con colores y orden constante
    fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                             category_orders={'Vocabulario': categorias_ordenadas},
                             color='Vocabulario',
                             color_discrete_map=colores)
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
    
    # Crear DataFrames para las tablas sin índice adicional
    tabla_gramatica = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_gramatica.columns = ['Nivel', 'Estudiantes']
    tabla_gramatica = tabla_gramatica.reset_index(drop=True)

    tabla_vocabulario = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_vocabulario.columns = ['Nivel', 'Estudiantes']
    tabla_vocabulario = tabla_vocabulario.reset_index(drop=True)

    # Crear columnas para las tablas
    col1, col2 = st.columns(2)

    # Mostrar tabla de Gramática en la primera columna
    with col1:
        st.write("**Gramática**")
        st.table(tabla_gramatica)

    # Mostrar tabla de Vocabulario en la segunda columna
    with col2:
        st.write("**Vocabulario**")
        st.table(tabla_vocabulario)

    # Botón para generar el PDF
    if st.button("Generar reporte"):
        img_gramatica = fig_to_img(fig_gramatica)
        img_vocabulario = fig_to_img(fig_vocabulario)
        
        pdf = generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario, img_gramatica, img_vocabulario)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        st.download_button(label="Descargar PDF", data=pdf_output, file_name="reporte.pdf", mime="application/pdf")
else:
    st.write("CCT no encontrado. Por favor ingresa un CCT válido.")
