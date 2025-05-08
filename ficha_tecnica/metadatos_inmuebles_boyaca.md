# 📄 Ficha Técnica de la Base de Datos de Inmuebles – Boyacá

---

## 1. Nombre del conjunto de datos:
**Oferta inmobiliaria en línea – Principales ciudades de Boyacá**

---

## 2. Fuente de datos:
- Scraping realizado al portal [fincaraiz.com.co](https://fincaraiz.com.co)  
- Scrapeo directo de páginas individuales de inmuebles

---

## 3. Fecha de recolección:
05/05/2025

---

## 4. Cobertura geográfica:
Ciudades principales del departamento de Boyacá, Colombia:

- Tunja  
- Duitama  
- Sogamoso  
- Paipa  

---

## 5. Descripción general:
Este conjunto de datos recopila información sobre inmuebles publicados para la venta en el portal Finca Raíz, incluyendo características físicas, ubicación, precio, vendedor y coordenadas geográficas (si están disponibles).

---

## 6. Número de registros:
*Registros: 939*
*columns : 22*

---

## 7. Variables incluidas:

| Variable            | Descripción                                                                 |
|---------------------|------------------------------------------------------------------------------|
| `tipo_inmueble`     | Tipo de propiedad (Casa, Apartamento, Lote, etc.)                           |
| `finalidad`         | Si el inmueble está en venta o arriendo                                     |
| `estado_inmueble`   | Condición del inmueble (Usado, Nuevo, Remodelado)                           |
| `Ciudad`            | Ciudad donde se encuentra el inmueble                                       |
| `ubicacion_asociada`| Nombre del barrio, sector o zona asociado                                   |
| `area m²`           | Área del inmueble en metros cuadrados                                       |
| `habitaciones`      | Número de habitaciones                                                       |
| `baños`             | Número de baños                                                              |
| `precio`            | Precio del inmueble en pesos colombianos                                    |
| `estrato`           | Nivel socioeconómico estimado                                                |
| `comodidades`       | Lista de características adicionales (balcón, parqueadero, etc.)            |
| `descripcion`       | Descripción textual del anuncio                                              |
| `contacto`          | Información de contacto (cuando está disponible)                            |
| `codigo`            | Código del anuncio en la plataforma                                          |
| `vendedor`          | Nombre del agente o inmobiliaria                                             |
| `link_venta`        | URL del anuncio                                                              |
| `link_image`        | URL de imagen principal del inmueble                                         |
| `error`             | Marca si hubo algún error durante el scraping                               |
| `latitud`           | Coordenada geográfica – latitud (si disponible)                             |
| `longitud`          | Coordenada geográfica – longitud (si disponible)                            |

---

## 8. Formato de los datos:
- CSV / DataFrame de pandas
- [Dataset](../data/datos_ciudades.csv)
