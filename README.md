# Proyecto: Análisis de Datos Inmobiliarios en Boyacá

## Descripción General
Este proyecto tiene como objetivo principal analizar y visualizar datos de inmuebles extraídos por web scraping desde el portal Finca Raíz, centrado en las cuatro ciudades más importantes del departamento de Boyacá: Tunja, Duitama, Sogamoso y Paipa. Se busca generar un storytelling basado en los datos, que permita identificar oportunidades de compra, tendencias del mercado y patrones de valorización.

## Estructura del Repositorio

/
├── README.md
├── data/
│ └── inmuebles_boyaca.csv
├── ficha_tecnica/
│ └── metadatos_inmuebles_boyaca.md
├── scrapy/
│ ├── scraper.py
│ ├── urls_tunja.txt
│ ├── urls_duitama.txt
│ ├── urls_sogamoso.txt
│ └── urls_paipa.txt
├── dashboard/
│ └── dashboard_inmuebles.html
└── visualizaciones/
└── *.png / *.html (graficos generados)

## Objetivos del Proyecto

1. **Recolección de Datos:**
   - Realizar scraping de inmuebles en venta por ciudad.
   - Almacenar datos estructurados en CSV.

2. **Generación de Metadatos (Ficha Técnica):**
   - Tipo de datos por columna.
   - Fuentes y descripción.
   - Posibles valores nulos o inconsistencias.

3. **Visualización de Datos (Storytelling):**
   - Mapa de precios por barrio (colores).
   - Precio vs área en m2.
   - Análisis de valorización por remodelación.
   - Oportunidades de compra de lotes en zonas destacadas.
   - Comparación de precio*m2 por estrato o ubicación.

4. **Storytelling: Preguntas a responder con visualizaciones**

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
- [CSV con datos](./data/inmuebles_boyaca.csv)
- [Ficha técnica / metadatos](./ficha_tecnica/metadatos_inmuebles_boyaca.md)
- [Script de scraping](./scrapy/scraper.py)
- [Dashboard en HTML](./dashboard/dashboard_inmuebles.html)

---

> Este proyecto busca generar valor a partir de los datos inmobiliarios abiertos y extraídos de forma ética, con fines educativos y de análisis urbano y económico.
