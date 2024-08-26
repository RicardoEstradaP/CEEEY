import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

def generar_grafico(gramatica_data, vocabulario_data):
    # Crear una figura de Matplotlib
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    
    # Gráfico de Gramática
    ax[0].bar(gramatica_data['Nivel'], gramatica_data['Estudiantes'], color='blue')
    ax[0].set_title('Frecuencia de Gramática')
    ax[0].set_xlabel('Nivel')
    ax[0].set_ylabel('Estudiantes')
    
    # Gráfico de Vocabulario
    ax[1].bar(vocabulario_data['Nivel'], vocabulario_data['Estudiantes'], color='green')
    ax[1].set_title('Frecuencia de Vocabulario')
    ax[1].set_xlabel('Nivel')
    ax[1].set_ylabel('Estudiantes')
    
    # Guardar la figura en un objeto BytesIO
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close(fig)
    
    return img_buffer

def generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario):
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

    # Gráfico de Matplotlib
    img_buffer = generar_grafico(tabla_gramatica, tabla_vocabulario)
    pdf.image(img_buffer, x=10, y=50, w=190)
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

# Ejemplo de uso (dentro de la app Streamlit)
# Supongamos que 'escuela', 'modalidad', 'tabla_gramatica', y 'tabla_vocabulario' son las variables que tienes
pdf = generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario)
pdf_output = BytesIO()
pdf.output(pdf_output)
pdf_output.seek(0)

# Streamlit descarga el PDF
st.download_button(label="Descargar reporte PDF", data=pdf_output, file_name="reporte.pdf", mime="application/pdf")
