import streamlit as st
import pandas as pd
import plotly.express as px

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
            'text': f"Gramática<br><span style='font-size:12px'>Frecuencia: {freq_gramatica} estudiantes</span>",
            'y':0.9,  # Ajustar la posición vertical del título
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)  # Ajustar el margen superior para crear espacio entre el título y el gráfico
    )

    # Gráfico de sectores para Vocabulario con colores y orden constante
    fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                             category_orders={'Vocabulario': categorias_ordenadas},
                             color='Vocabulario',
                             color_discrete_map=colores)
    fig_vocabulario.update_layout(
        title={
            'text': f"Vocabulario<br><span style='font-size:12px'>Frecuencia: {freq_vocabulario} estudiantes</span>",
            'y':0.9,  # Ajustar la posición vertical del título
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)  # Ajustar el margen superior para crear espacio entre el título y el gráfico
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
    tabla_gramatica.columns = ['Nivel', 'Estudiantes']  # Cambiar los nombres de las columnas
    tabla_gramatica = tabla_gramatica.reset_index(drop=True)  # Eliminar la columna de índice

    tabla_vocabulario = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_vocabulario.columns = ['Nivel', 'Estudiantes']  # Cambiar los nombres de las columnas
    tabla_vocabulario = tabla_vocabulario.reset_index(drop=True)  # Eliminar la columna de índice

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

else:
    st.write("CCT no encontrado. Por favor ingresa un CCT válido.")
