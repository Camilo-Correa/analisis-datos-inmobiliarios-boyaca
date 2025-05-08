from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import re
import csv

# ------------------ FUNCIONES AUXILIARES ------------------

def buscar_linea_despues_de(texto, patron):
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        if patron.lower() in linea.lower():
            for j in range(i + 1, min(i + 5, len(lineas))):
                if lineas[j].strip():
                    return lineas[j].strip()
    return ""

def extract_regex(pattern, text, default=""):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default

def extraer_datos(url):
    try:
        options = Options()
        options.add_argument("--headless")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(6)
        html = driver.page_source
        body_text = driver.find_element(By.TAG_NAME, "body").text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")
        driver.quit()

        # Tipo de inmueble
        tipo_inmueble = ""
        for tipo in ["Casa", "Apartamento", "Lote", "Finca", "Consultorio", "Oficina", "Local"]:
            if tipo.lower() in body_text.lower():
                tipo_inmueble = tipo
                break

        # Finalidad
        if "Venta" in body_text:
            finalidad = "venta"
        elif "Arriendo" in body_text:
            finalidad = "arriendo"
        else:
            finalidad = ""

        estado_inmueble = "Usado" if "usado" in body_text.lower() else "Nuevo"

        precio = extract_regex(r"precio de Venta es de \$ ([\d\.\s]+)", body_text)
        if not precio or "precio" in precio.lower():
            precio = buscar_linea_despues_de(text, "Precio de Venta") or buscar_linea_despues_de(text, "Precio de Arriendo")

        vendedor = extract_regex(r"por (.*?) el \d{1,2} de \w+", body_text)
        if not vendedor or "estás en" in vendedor.lower():
            vendedor = buscar_linea_despues_de(text, "por ")

        ubicacion_principal = buscar_linea_despues_de(text, "Ubicación Principal")
        ubicacion_asociada = buscar_linea_despues_de(text, "Ubicaciones asociadas")
        estrato = buscar_linea_despues_de(text, "Estrato")
        antiguedad = buscar_linea_despues_de(text, "Antigüedad")
        area_m2 = buscar_linea_despues_de(text, "Área Construida")
        habitaciones = buscar_linea_despues_de(text, "Habitaciones")
        banos = buscar_linea_despues_de(text, "Baños")

        # 🟩 Administración (sí/no y valor si aparece)
        admin_line = buscar_linea_despues_de(text, "Administración")
        if "admin" in admin_line.lower():
            administracion = "Sí"
            precio_admin = extract_regex(r"administraci[oó]n.*?\$([\d\.\s]+)", admin_line)
            if precio_admin:
                administracion += f" (${precio_admin})"
        else:
            administracion = "No"

        descripcion = buscar_linea_despues_de(text, "Descripción")
        if not descripcion:
            descripcion = extract_regex(r"Descripci[oó]n\s*:\s*(.*)", text)

        # 🟩 Teléfono o contacto
        contacto = buscar_linea_despues_de(text, "Contáctanos")
        if not contacto:
            contacto = extract_regex(r"Tel[eé]fono[s]*\s*[:\-]?\s*([\d\s\-\(\)]+)", text)
        if not contacto:
            contacto = extract_regex(r"(?:Llamar|WhatsApp).*?(\d{7,12})", text)

        codigo = buscar_linea_despues_de(text, "Código Fincaraíz")

        # Imagen principal
        imagen = ""
        imagen_tag = soup.find("img", {"class": re.compile(".*swiper-slide.*")})
        if imagen_tag and imagen_tag.get("src"):
            imagen = imagen_tag["src"]

        comodidades = []
        lineas = text.split("\n")
        try:
            idx = lineas.index("Comodidades de la propiedad")
            for i in range(idx + 1, len(lineas)):
                linea = lineas[i].strip()
                if linea == "Ver más" or not linea:
                    break
                comodidades.append(linea.replace("•", "").strip())
        except:
            pass

        return {
            "tipo_inmueble": tipo_inmueble,
            "finalidad": finalidad,
            "estado_inmueble": estado_inmueble,
            "ubicacion_principal": ubicacion_principal,
            "ubicacion_asociada": ubicacion_asociada,
            "area": f"{area_m2} m²" if area_m2 else "",
            "habitaciones": habitaciones,
            "baños": banos,
            "precio": f"${precio}" if precio and not precio.startswith("$") else precio,
            "estrato": estrato,
            "antigüedad": antiguedad,
            "administración": administracion,
            "comodidades": ", ".join(comodidades),
            "descripcion": descripcion,
            "contacto": contacto,
            "codigo": codigo,
            "vendedor": vendedor,
            "link_venta": url,
            "link_image": imagen,
            "error": ""
        }
    except Exception as e:
        return {
            "tipo_inmueble": "",
            "finalidad": "",
            "estado_inmueble": "",
            "ubicacion_principal": "",
            "ubicacion_asociada": "",
            "area": "",
            "habitaciones": "",
            "baños": "",
            "precio": "",
            "estrato": "",
            "antigüedad": "",
            "administración": "",
            "comodidades": "",
            "descripcion": "",
            "contacto": "",
            "codigo": "",
            "vendedor": "",
            "link_venta": url,
            "link_image": "",
            "error": str(e)
        }

# ------------------ PROCESO PRINCIPAL ------------------

with open("links-1.txt", "r") as file:
    urls = [line.strip() for line in file if line.strip()]

datos_recolectados = []

print(f"Extrayendo datos de {len(urls)} propiedades...\n")

for url in tqdm(urls, desc="Progreso"):
    datos = extraer_datos(url)
    datos_recolectados.append(datos)

# Guardar en CSV
campos = list(datos_recolectados[0].keys())

with open("datos-fincaraiz.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(datos_recolectados)

print("\n✅ Proceso finalizado. Datos guardados en 'datos-fincaraiz.csv'")
