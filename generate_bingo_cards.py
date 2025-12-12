#!/usr/bin/env python3
"""
Generador de Cartillas de Bingo con Imágenes
Diseño UX/UI profesional
"""

import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math

# Configuración
IMAGES_DIR = Path("/home/user/Bingo/images_converted")
OUTPUT_DIR = Path("/home/user/Bingo/cartillas")
OUTPUT_DIR.mkdir(exist_ok=True)

# Diseño UX/UI - Colores (paleta moderna y amigable)
COLORS = {
    'background': '#F8FAFC',      # Fondo suave gris-blanco
    'card_bg': '#FFFFFF',          # Fondo de cartilla blanco
    'header_bg': '#6366F1',        # Indigo vibrante para header
    'header_text': '#FFFFFF',      # Texto blanco en header
    'grid_border': '#E2E8F0',      # Bordes suaves
    'cell_bg': '#FFFFFF',          # Fondo de celda
    'cell_border': '#CBD5E1',      # Borde de celda
    'free_bg': '#1F2937',          # Negro elegante para FREE
    'free_text': '#FFFFFF',        # Texto blanco para FREE
    'card_number': '#64748B',      # Gris para número de cartilla
    'shadow': '#00000020',         # Sombra suave
    'accent': '#8B5CF6',           # Violeta acento
}

# Dimensiones (optimizadas para impresión A4/Letter)
CARD_WIDTH = 1200
CARD_HEIGHT = 1400
GRID_SIZE = 5
CELL_PADDING = 8
HEADER_HEIGHT = 120
MARGIN = 60

def hex_to_rgb(hex_color):
    """Convierte color hex a RGB"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 8:  # Con alpha
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_rounded_rectangle(draw, coords, radius, fill, outline=None, width=1):
    """Dibuja un rectángulo con esquinas redondeadas"""
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline, width=width)

def add_shadow(image, offset=(5, 5), blur_radius=10):
    """Añade sombra suave a una imagen"""
    # Crear capa de sombra
    shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    # La sombra se crea desplazada
    return image  # Simplificado para rendimiento

def load_images():
    """Carga todas las imágenes PNG disponibles"""
    images = []
    for img_path in IMAGES_DIR.glob("*.png"):
        try:
            img = Image.open(img_path)
            images.append(img_path)
        except Exception as e:
            print(f"Error cargando {img_path}: {e}")
    return images

def resize_image_to_cell(img_path, cell_size):
    """Redimensiona imagen para caber en celda manteniendo aspecto"""
    img = Image.open(img_path)

    # Convertir a RGBA si es necesario
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Calcular tamaño manteniendo proporción
    target_size = cell_size - (CELL_PADDING * 2)

    # Thumbnail mantiene proporción
    img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)

    # Crear imagen cuadrada con la imagen centrada
    result = Image.new('RGBA', (target_size, target_size), (255, 255, 255, 0))

    # Centrar imagen
    x = (target_size - img.width) // 2
    y = (target_size - img.height) // 2
    result.paste(img, (x, y), img if img.mode == 'RGBA' else None)

    return result

def get_font(size, bold=False):
    """Obtiene fuente del sistema"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

    return ImageFont.load_default()

def create_bingo_card(card_number, image_paths, all_images):
    """Crea una cartilla de bingo con diseño UX/UI moderno"""

    # Crear imagen base
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), hex_to_rgb(COLORS['background']))
    draw = ImageDraw.Draw(card)

    # Calcular dimensiones de la grilla
    grid_start_x = MARGIN
    grid_start_y = MARGIN + HEADER_HEIGHT + 20
    grid_width = CARD_WIDTH - (2 * MARGIN)
    grid_height = CARD_HEIGHT - grid_start_y - MARGIN
    cell_size = min(grid_width // GRID_SIZE, grid_height // GRID_SIZE)

    # Centrar la grilla
    actual_grid_width = cell_size * GRID_SIZE
    actual_grid_height = cell_size * GRID_SIZE
    grid_start_x = (CARD_WIDTH - actual_grid_width) // 2

    # === HEADER con letras B-I-N-G-O como encabezados de columna ===
    header_y = MARGIN
    bingo_letters = ['B', 'I', 'N', 'G', 'O']

    # Fuente grande para que las letras ocupen el header
    letter_font = get_font(90, bold=True)

    # Dibujar cada letra sobre su columna correspondiente
    for col, letter in enumerate(bingo_letters):
        letter_cell_x = grid_start_x + col * cell_size

        # Fondo de cada letra (rectángulo redondeado)
        create_rounded_rectangle(
            draw,
            (letter_cell_x + 2, header_y, letter_cell_x + cell_size - 2, header_y + HEADER_HEIGHT),
            radius=15,
            fill=hex_to_rgb(COLORS['header_bg'])
        )

        # Centrar letra perfectamente en la celda del header
        bbox = draw.textbbox((0, 0), letter, font=letter_font)
        letter_width = bbox[2] - bbox[0]
        letter_height = bbox[3] - bbox[1]

        # Centrado horizontal
        letter_x = letter_cell_x + (cell_size - letter_width) // 2
        # Centrado vertical ajustado (compensar ascendentes/descendentes)
        letter_y = header_y + (HEADER_HEIGHT - letter_height) // 2 - bbox[1]

        draw.text((letter_x, letter_y), letter, fill=hex_to_rgb(COLORS['header_text']), font=letter_font)

    # === GRILLA DE IMÁGENES ===
    img_index = 0

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_x = grid_start_x + col * cell_size
            cell_y = grid_start_y + row * cell_size

            # Fondo de celda
            create_rounded_rectangle(
                draw,
                (cell_x + 2, cell_y + 2, cell_x + cell_size - 2, cell_y + cell_size - 2),
                radius=12,
                fill=hex_to_rgb(COLORS['cell_bg']),
                outline=hex_to_rgb(COLORS['cell_border']),
                width=2
            )

            # Centro FREE
            if row == 2 and col == 2:
                # Fondo negro elegante para FREE
                create_rounded_rectangle(
                    draw,
                    (cell_x + 4, cell_y + 4, cell_x + cell_size - 4, cell_y + cell_size - 4),
                    radius=12,
                    fill=hex_to_rgb(COLORS['free_bg'])
                )

                # Estrella decorativa más grande
                star_font = get_font(56)
                star = "★"
                bbox = draw.textbbox((0, 0), star, font=star_font)
                star_x = cell_x + (cell_size - (bbox[2] - bbox[0])) // 2
                star_y = cell_y + cell_size // 2 - 55
                draw.text((star_x, star_y), star, fill=hex_to_rgb(COLORS['free_text']), font=star_font)

                # Texto FREE más grande y centrado
                free_font = get_font(42, bold=True)
                free_text = "FREE"
                bbox = draw.textbbox((0, 0), free_text, font=free_font)
                free_x = cell_x + (cell_size - (bbox[2] - bbox[0])) // 2
                free_y = cell_y + cell_size // 2 + 10
                draw.text((free_x, free_y), free_text, fill=hex_to_rgb(COLORS['free_text']), font=free_font)
            else:
                # Colocar imagen
                if img_index < len(image_paths):
                    try:
                        img = resize_image_to_cell(image_paths[img_index], cell_size)
                        img_x = cell_x + (cell_size - img.width) // 2
                        img_y = cell_y + (cell_size - img.height) // 2

                        # Convertir card a RGBA para pegar con transparencia
                        if card.mode != 'RGBA':
                            card = card.convert('RGBA')

                        card.paste(img, (img_x, img_y), img)
                        draw = ImageDraw.Draw(card)
                    except Exception as e:
                        print(f"Error con imagen: {e}")

                img_index += 1

    # === PIE DE PÁGINA - Número de cartilla ===
    footer_font = get_font(28)
    footer_text = f"Cartilla #{card_number:02d}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_x = (CARD_WIDTH - (bbox[2] - bbox[0])) // 2
    footer_y = CARD_HEIGHT - MARGIN + 10

    draw.text((footer_x, footer_y), footer_text, fill=hex_to_rgb(COLORS['card_number']), font=footer_font)

    # Línea decorativa
    line_y = footer_y - 15
    line_width = 100
    line_x1 = (CARD_WIDTH - line_width) // 2
    draw.line([(line_x1, line_y), (line_x1 + line_width, line_y)],
              fill=hex_to_rgb(COLORS['accent']), width=3)

    # Convertir a RGB para guardar como PNG
    if card.mode == 'RGBA':
        background = Image.new('RGB', card.size, hex_to_rgb(COLORS['background']))
        background.paste(card, mask=card.split()[3])
        card = background

    return card

def generate_all_cards(num_cards=50):
    """Genera todas las cartillas de bingo"""
    print("=" * 60)
    print("   GENERADOR DE CARTILLAS DE BINGO - DISEÑO UX/UI")
    print("=" * 60)

    # Cargar imágenes
    all_images = load_images()
    print(f"\nImágenes disponibles: {len(all_images)}")

    if len(all_images) < 24:
        print(f"ERROR: Se necesitan al menos 24 imágenes, solo hay {len(all_images)}")
        return

    # Generar cartillas únicas
    generated_combinations = set()

    print(f"\nGenerando {num_cards} cartillas...")
    print("-" * 40)

    for card_num in range(1, num_cards + 1):
        # Seleccionar 24 imágenes aleatorias (5x5 - 1 centro FREE)
        attempts = 0
        while attempts < 1000:
            selected = random.sample(all_images, 24)
            # Crear hash de la combinación para verificar unicidad
            combo_key = tuple(sorted([str(p) for p in selected]))

            if combo_key not in generated_combinations:
                generated_combinations.add(combo_key)
                break
            attempts += 1

        # Mezclar para posición aleatoria
        random.shuffle(selected)

        # Crear cartilla
        card = create_bingo_card(card_num, selected, all_images)

        # Guardar
        output_path = OUTPUT_DIR / f"cartilla_{card_num:02d}.png"
        card.save(output_path, 'PNG', quality=95)

        if card_num % 10 == 0 or card_num == 1:
            print(f"  ✓ Cartilla {card_num:02d}/{num_cards} generada")

    print("-" * 40)
    print(f"\n✓ {num_cards} cartillas generadas exitosamente")
    print(f"  Ubicación: {OUTPUT_DIR}/")
    print(f"  Formato: PNG ({CARD_WIDTH}x{CARD_HEIGHT} px)")

    return True

if __name__ == "__main__":
    generate_all_cards(50)
