#!/usr/bin/env python3
"""
Script para generar cartillas de bingo desde imágenes WEBP
1. Convierte WEBP a PNG
2. Detecta y elimina duplicados
3. Genera 50 cartillas únicas en PDF
"""

import os
import hashlib
from pathlib import Path
from PIL import Image
import imagehash
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import random
import json

# Configuración
WEBP_DIR = Path("/home/user/Bingo")
OUTPUT_DIR = Path("/home/user/Bingo/images_converted")
PDF_OUTPUT = Path("/home/user/Bingo/cartillas_bingo.pdf")
REPORT_FILE = Path("/home/user/Bingo/duplicates_report.txt")

# Crear directorio de salida
OUTPUT_DIR.mkdir(exist_ok=True)

def convert_webp_to_png():
    """Convierte todas las imágenes WEBP a PNG"""
    print("=" * 50)
    print("PASO 1: Convirtiendo WEBP a PNG...")
    print("=" * 50)

    webp_files = list(WEBP_DIR.glob("*.webp"))
    converted = []

    for webp_file in webp_files:
        png_name = webp_file.stem + ".png"
        png_path = OUTPUT_DIR / png_name

        try:
            img = Image.open(webp_file)
            # Convertir a RGB si es necesario (para evitar problemas con RGBA)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco para transparencias
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(png_path, 'PNG')
            converted.append(png_path)
            print(f"  ✓ {webp_file.name} -> {png_name}")
        except Exception as e:
            print(f"  ✗ Error con {webp_file.name}: {e}")

    print(f"\nTotal convertidas: {len(converted)} imágenes")
    return converted

def detect_duplicates():
    """Detecta duplicados usando hash perceptual y MD5"""
    print("\n" + "=" * 50)
    print("PASO 2: Detectando duplicados...")
    print("=" * 50)

    png_files = list(OUTPUT_DIR.glob("*.png"))

    # Diccionarios para almacenar hashes
    md5_hashes = {}
    perceptual_hashes = {}
    duplicates = []
    unique_images = []

    for png_file in png_files:
        # Calcular MD5 del contenido
        with open(png_file, 'rb') as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()

        # Calcular hash perceptual
        try:
            img = Image.open(png_file)
            p_hash = str(imagehash.phash(img))

            # Verificar si es duplicado exacto (MD5)
            if md5_hash in md5_hashes:
                duplicates.append({
                    'file': png_file.name,
                    'duplicate_of': md5_hashes[md5_hash],
                    'type': 'MD5 exacto'
                })
                os.remove(png_file)
                print(f"  ✗ Eliminado (MD5): {png_file.name} = {md5_hashes[md5_hash]}")
                continue

            # Verificar si es duplicado perceptual (imágenes visualmente iguales)
            if p_hash in perceptual_hashes:
                duplicates.append({
                    'file': png_file.name,
                    'duplicate_of': perceptual_hashes[p_hash],
                    'type': 'Hash perceptual'
                })
                os.remove(png_file)
                print(f"  ✗ Eliminado (perceptual): {png_file.name} ≈ {perceptual_hashes[p_hash]}")
                continue

            # No es duplicado, agregar a los diccionarios
            md5_hashes[md5_hash] = png_file.name
            perceptual_hashes[p_hash] = png_file.name
            unique_images.append(png_file)

        except Exception as e:
            print(f"  ⚠ Error procesando {png_file.name}: {e}")

    print(f"\nDuplicados encontrados y eliminados: {len(duplicates)}")
    print(f"Imágenes únicas restantes: {len(unique_images)}")

    return unique_images, duplicates

def generate_report(duplicates, unique_count):
    """Genera reporte de duplicados"""
    print("\n" + "=" * 50)
    print("PASO 3: Generando reporte...")
    print("=" * 50)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("REPORTE DE DUPLICADOS - BINGO IMAGES\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total de imágenes originales (WEBP): {len(list(WEBP_DIR.glob('*.webp')))}\n")
        f.write(f"Duplicados eliminados: {len(duplicates)}\n")
        f.write(f"Imágenes únicas finales: {unique_count}\n\n")

        if duplicates:
            f.write("-" * 60 + "\n")
            f.write("DETALLE DE DUPLICADOS ELIMINADOS:\n")
            f.write("-" * 60 + "\n\n")

            for i, dup in enumerate(duplicates, 1):
                f.write(f"{i}. {dup['file']}\n")
                f.write(f"   Duplicado de: {dup['duplicate_of']}\n")
                f.write(f"   Método de detección: {dup['type']}\n\n")
        else:
            f.write("No se encontraron duplicados.\n")

    print(f"  ✓ Reporte guardado en: {REPORT_FILE}")

def generate_bingo_cards(unique_images, num_cards=50):
    """Genera cartillas de bingo en PDF"""
    print("\n" + "=" * 50)
    print("PASO 4: Generando cartillas de bingo...")
    print("=" * 50)

    if len(unique_images) < 24:
        print(f"  ⚠ Se necesitan al menos 24 imágenes únicas para las cartillas.")
        print(f"    Solo hay {len(unique_images)} imágenes disponibles.")
        return False

    # Configuración del PDF
    c = canvas.Canvas(str(PDF_OUTPUT), pagesize=letter)
    page_width, page_height = letter

    # Configuración de la grilla
    grid_size = 5
    cell_size = 1.3 * inch
    grid_width = grid_size * cell_size
    grid_height = grid_size * cell_size

    # Centrar la grilla
    start_x = (page_width - grid_width) / 2
    start_y = (page_height - grid_height) / 2 - 0.5 * inch

    # Generar combinaciones únicas
    all_combinations = set()
    image_paths = [str(img) for img in unique_images]

    for card_num in range(1, num_cards + 1):
        # Generar combinación única
        attempts = 0
        while attempts < 1000:
            selected = tuple(sorted(random.sample(image_paths, 24)))
            if selected not in all_combinations:
                all_combinations.add(selected)
                break
            attempts += 1

        # Mezclar para posición aleatoria
        card_images = list(selected)
        random.shuffle(card_images)

        # Título
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, page_height - 0.8 * inch, f"CARTILLA {card_num}")

        # Dibujar grilla
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)

        img_index = 0
        for row in range(grid_size):
            for col in range(grid_size):
                x = start_x + col * cell_size
                y = start_y + (grid_size - 1 - row) * cell_size

                # Dibujar celda
                c.rect(x, y, cell_size, cell_size)

                # Centro libre
                if row == 2 and col == 2:
                    # Estrella o FREE en el centro
                    c.setFillColor(colors.gold)
                    c.rect(x, y, cell_size, cell_size, fill=1)
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawCentredString(x + cell_size/2, y + cell_size/2 - 6, "FREE")
                    c.setFont("Helvetica", 10)
                    c.drawCentredString(x + cell_size/2, y + cell_size/2 - 20, "★")
                else:
                    # Dibujar imagen
                    img_path = card_images[img_index]
                    img_index += 1

                    try:
                        # Padding dentro de la celda
                        padding = 4
                        img_x = x + padding
                        img_y = y + padding
                        img_width = cell_size - 2 * padding
                        img_height = cell_size - 2 * padding

                        c.drawImage(img_path, img_x, img_y,
                                   width=img_width, height=img_height,
                                   preserveAspectRatio=True, anchor='c')
                    except Exception as e:
                        # Si falla, dibujar placeholder
                        c.setFillColor(colors.lightgrey)
                        c.rect(x + 2, y + 2, cell_size - 4, cell_size - 4, fill=1)
                        c.setFillColor(colors.black)

        # Pie de página
        c.setFont("Helvetica", 10)
        c.drawCentredString(page_width / 2, 0.5 * inch, f"Página {card_num} de {num_cards}")

        # Nueva página (excepto la última)
        if card_num < num_cards:
            c.showPage()

        if card_num % 10 == 0:
            print(f"  ✓ Generadas {card_num}/{num_cards} cartillas...")

    c.save()
    print(f"\n  ✓ PDF guardado en: {PDF_OUTPUT}")
    return True

def main():
    print("\n" + "=" * 60)
    print("   GENERADOR DE CARTILLAS DE BINGO")
    print("=" * 60)

    # Paso 1: Convertir WEBP a PNG
    converted = convert_webp_to_png()

    # Paso 2: Detectar y eliminar duplicados
    unique_images, duplicates = detect_duplicates()

    # Paso 3: Generar reporte
    generate_report(duplicates, len(unique_images))

    print("\n" + "=" * 50)
    print(f"RESUMEN: {len(unique_images)} IMÁGENES ÚNICAS ENCONTRADAS")
    print("=" * 50)

    # Paso 4: Generar cartillas
    if len(unique_images) >= 24:
        generate_bingo_cards(unique_images, num_cards=50)
        print("\n" + "=" * 60)
        print("   ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"\nArchivos generados:")
        print(f"  - Imágenes PNG: {OUTPUT_DIR}/")
        print(f"  - Reporte: {REPORT_FILE}")
        print(f"  - Cartillas: {PDF_OUTPUT}")
    else:
        print(f"\n⚠ No hay suficientes imágenes únicas ({len(unique_images)}/24 mínimo)")
        print("  No se pueden generar las cartillas de bingo.")

if __name__ == "__main__":
    main()
