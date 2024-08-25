import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos desde la ruta especificada
df = pd.read_csv('D:\\Phyton\\Pruebas\\PEI-1\\Resultados.csv')

# Configuración de la página
st.set_page_config(page_title="Resultados de la Prueba Estatal de Inglés", layout="wide")

# Título del Dashboard
st.title("Resultados de la Prueba Estatal de Inglés")

# Filtro por Zona
zona_input = st.selectbox("Selecciona la Zona:", df['Zona'].unique())

# Filtrar DataFrame según la zona seleccionada
df_zona = df[df['Zona'] == zona_input]

# Configuración para el dashboard
if not df_zona.empty:
    # Crear un filtro por CCT
    cct_input = st.text_input("Escribe el CCT:")

    # Filtrar DataFrame según el valor de CCT ingresado
    df_filtered = df_zona[df_zona['CCT'] == cct_input]

    # Lista de categorías en orden deseado
    categorias_ordenadas = ['Pre A1', 'A1', 'A2', 'Superior a A2']

    # Asignar colores específicos a cada categoría
    colores = {
        'Pre A1': '#1f77b4',
        'A1': '#ff7f0e',
        'A2': '#2ca02c',
        'Superior a A2': '#d62728'
    }

    # Crear tres columnas para el nuevo segmento
    col1, col2, col3 = st.columns(3)

    # Mostrar listado de Escuelas en la primera columna
    with col1:
        st.subheader("Listado de Escuelas")
        if not df_zona['Escuela'].empty:
            st.write(df_zona['Escuela'].unique())

    # Gráfico de sectores para Gramática en la segunda columna
    with col2:
        if not df_filtered.empty:
            df_gramatica = df_filtered[df_filtered['Gramática'].isin(categorias_ordenadas)]
            freq_gramatica = df_gramatica['Gramática'].count()
            fig_gramatica = px.pie(df_gramatica, names='Gramática', 
                                   category_orders={'Gramática': categorias_ordenadas},
                                   color='Gramática',
                                   color_discrete_map=colores)
            fig_gramatica.update_layout(
                title={
                    'text': f"Gramática<br><span style='font-size:12px'>Frecuencia: {freq_gramatica} estudiantes</span>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                margin=dict(t=120)  # Ajustar el margen superior para crear espacio entre el título y el gráfico
            )
            st.plotly_chart(fig_gramatica, use_container_width=True)

    # Gráfico de sectores para Vocabulario en la tercera columna
    with col3:
        if not df_filtered.empty:
            df_vocabulario = df_filtered[df_filtered['Vocabulario'].isin(categorias_ordenadas)]
            freq_vocabulario = df_vocabulario['Vocabulario'].count()
            fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                                     category_orders={'Vocabulario': categorias_ordenadas},
                                     color='Vocabulario',
                                     color_discrete_map=colores)
            fig_vocabulario.update_layout(
                title={
                    'text': f"Vocabulario<br><span style='font-size:12px'>Frecuencia: {freq_vocabulario} estudiantes</span>",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                margin=dict(t=120)  # Ajustar el margen superior para crear espacio entre el título y el gráfico
            )
            st.plotly_chart(fig_vocabulario, use_container_width=True)

    # Mostrar datos detallados para el CCT seleccionado
    if not df_filtered.empty:
        escuela = df_filtered['Escuela'].iloc[0]
        modalidad = df_filtered['Modalidad'].iloc[0]
        st.write(f"**Escuela:** {escuela}")
        st.write(f"**Modalidad:** {modalidad}")

        # Tabla de frecuencias en dos columnas
        st.subheader("Tabla de Frecuencias")

        # Crear DataFrames para las tablas sin índice adicional
        tabla_gramatica = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).reset_index()
        tabla_gramatica.columns = ['Nivel', 'Estudiantes']
        tabla_gramatica = tabla_gramatica.reset_index(drop=True)  # Eliminar la columna de índice

        tabla_vocabulario = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).reset_index()
        tabla_vocabulario.columns = ['Nivel', 'Estudiantes']
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
    st.write("No se encontraron datos para la zona seleccionada.")
