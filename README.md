# Proyecto: Análisis de Datos Inmobiliarios en Boyacá

## Descripción General
Este proyecto tiene como objetivo principal analizar y visualizar datos de inmuebles extraídos por web scraping desde el portal [Finca Raíz](https://www.fincaraiz.com.co/venta/duitama/boyaca), centrado en las cuatro ciudades más importantes del departamento de Boyacá: Tunja, Duitama, Sogamoso y Paipa. Se busca generar un storytelling basado en los datos, que permita identificar oportunidades de compra, tendencias del mercado y patrones de valorización.

## Objetivos del Proyecto

1. **Recolección de Datos:**
   - Realizar scraping de inmuebles en venta por ciudad.
   - Almacenar datos estructurados en CSV.

2. **Limpieza de Datos:**
   - Tydy Data - Datos - Ordenados o estructurados
   - Handling Data - Manejo de fechas
   - String processing - procesamiento de texto
   - Valores desconocidos - eliminación, imputación

3. **Generación de Metadatos (Ficha Técnica):**
   - Tipo de datos por columna.
   - Fuentes y descripción.

4. **Visualización de Datos (Storytelling):**
   - Mapa de precios por barrio (colores).
   - Precio vs área en m2.
   - Análisis de valorización por remodelación.
   - Oportunidades de compra de lotes en zonas destacadas.
   - Comparación de precio*m2 por estrato o ubicación.

5. **Storytelling: Preguntas a responder con visualizaciones**

   - ¿Cuál es la distribución de precios por barrio?
   - ¿Cómo se relaciona el área en m2 con el precio?
   - ¿Qué propiedades ganarían valor si se remodelan?
   - ¿Dónde hay oportunidades de compra de lotes en buenas zonas?
   - ¿Cuáles viviendas podrían ser asequibles según el presupuesto del usuario?
   - ¿Existe sobrevaloración por estrato o ubicación?
   - ¿Qué es mejor indicador de clase socioeconómica: estrato o barrio?

## Requisitos
- Python 3.10+
- Pandas, Plotly, Folium, BeautifulSoup, Dash o Streamlit (opcional)

## Enlaces Relevantes
- [CSV con datos](./data)
- [Ficha técnica / metadatos](./ficha_tecnica/metadatos_inmuebles_boyaca.md)
- [Script de scraping](./scrapy)
- [Dashboard en HTML](https://royecto-an-lisis-de-datos-inmobiliarios.onrender.com/)
- [Datos_Tratados](./limpieza_data/Limpieza_Analítica_de_Datos_inmuebles.ipynb)

---

> Este proyecto busca generar valor a partir de los datos inmobiliarios abiertos y extraídos de forma ética, con fines educativos y de análisis urbano y económico.
