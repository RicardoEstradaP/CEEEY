import streamlit as st
import pandas as pd
import plotly.express as px
import pdfkit
from io import BytesIO

# Función para generar el PDF
def generar_pdf_html(escuela, modalidad, tabla_gramatica, tabla_vocabulario):
    # Crear el contenido HTML del PDF
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            .title {{ text-align: center; font-size: 14px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Resultados de la Prueba Estatal de Inglés</h1>
        <p><strong>Escuela:</strong> {escuela}</p>
        <p><strong>Modalidad:</strong> {modalidad}</p>

        <div class="title">Tabla de Frecuencias: Gramática</div>
        <table>
            <tr>
                <th>Nivel</th>
                <th>Estudiantes</th>
                <th>Porcentaje</th>
            </tr>
    """
    
    for i in range(len(tabla_gramatica)):
        html_content += f"""
            <tr>
                <td>{tabla_gramatica.iloc[i]['Nivel']}</td>
                <td>{tabla_gramatica.iloc[i]['Estudiantes']}</td>
                <td>{tabla_gramatica.iloc[i]['Porcentaje']:.2f}%</td>
            </tr>
        """
    
    html_content += """
        </table>

        <div class="title">Tabla de Frecuencias: Vocabulario</div>
        <table>
            <tr>
                <th>Nivel</th>
                <th>Estudiantes</th>
                <th>Porcentaje</th>
            </tr>
    """
    
    for i in range(len(tabla_vocabulario)):
        html_content += f"""
            <tr>
                <td>{tabla_vocabulario.iloc[i]['Nivel']}</td>
                <td>{tabla_vocabulario.iloc[i]['Estudiantes']}</td>
                <td>{tabla_vocabulario.iloc[i]['Porcentaje']:.2f}%</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    # Generar PDF desde el HTML
    pdf_output = pdfkit.from_string(html_content, False)
    return pdf_output

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
                           color='Gramática')
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
                             color='Vocabulario')
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
    
    # Crear DataFrames para las tablas sin índice adicional y con porcentaje
    tabla_gramatica = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_gramatica.columns = ['Nivel', 'Estudiantes']
    tabla_gramatica['Porcentaje'] = (tabla_gramatica['Estudiantes'] / freq_gramatica) * 100
    tabla_gramatica = tabla_gramatica.reset_index(drop=True)

    tabla_vocabulario = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_vocabulario.columns = ['Nivel', 'Estudiantes']
    tabla_vocabulario['Porcentaje'] = (tabla_vocabulario['Estudiantes'] / freq_vocabulario) * 100
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
        pdf_output = generar_pdf_html(escuela, modalidad, tabla_gramatica, tabla_vocabulario)
        st.download_button(label="Descargar PDF", data=pdf_output, file_name="reporte.pdf", mime="application/pdf")
else:
    st.write("CCT no encontrado. Por favor ingresa un CCT válido.")
