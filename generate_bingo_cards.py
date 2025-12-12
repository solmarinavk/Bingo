#!/usr/bin/env python3
"""
Generador de Cartillas de Bingo 3x3 con Imágenes
Diseño UX/UI profesional
"""

import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Configuración
IMAGES_DIR = Path("/home/user/Bingo/images_converted")
OUTPUT_DIR = Path("/home/user/Bingo/cartillas")
OUTPUT_DIR.mkdir(exist_ok=True)

# Diseño UX/UI - Colores
COLORS = {
    'background': '#F8FAFC',
    'header_bg': '#6366F1',
    'header_text': '#FFFFFF',
    'cell_bg': '#FFFFFF',
    'cell_border': '#CBD5E1',
    'card_number': '#64748B',
    'accent': '#8B5CF6',
}

# Dimensiones para 3x3
CARD_WIDTH = 900
CARD_HEIGHT = 1100
GRID_SIZE = 3
CELL_PADDING = 8
HEADER_HEIGHT = 100
MARGIN = 50

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_rounded_rectangle(draw, coords, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline, width=width)

def load_images():
    images = []
    for img_path in IMAGES_DIR.glob("*.png"):
        try:
            Image.open(img_path)
            images.append(img_path)
        except Exception as e:
            print(f"Error cargando {img_path}: {e}")
    return images

def resize_image_to_cell(img_path, cell_size):
    img = Image.open(img_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    target_size = cell_size - (CELL_PADDING * 2)
    img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)

    result = Image.new('RGBA', (target_size, target_size), (255, 255, 255, 0))
    x = (target_size - img.width) // 2
    y = (target_size - img.height) // 2
    result.paste(img, (x, y), img if img.mode == 'RGBA' else None)

    return result

def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    return ImageFont.load_default()

def create_bingo_card(card_number, image_paths):
    """Crea una cartilla de bingo 3x3"""

    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), hex_to_rgb(COLORS['background']))
    draw = ImageDraw.Draw(card)

    # Calcular dimensiones
    grid_start_y = MARGIN + HEADER_HEIGHT + 15
    grid_width = CARD_WIDTH - (2 * MARGIN)
    grid_height = CARD_HEIGHT - grid_start_y - MARGIN - 50
    cell_size = min(grid_width // GRID_SIZE, grid_height // GRID_SIZE)

    actual_grid_width = cell_size * GRID_SIZE
    grid_start_x = (CARD_WIDTH - actual_grid_width) // 2

    # === HEADER con letras B-I-N ===
    header_y = MARGIN
    bingo_letters = ['B', 'I', 'N']
    letter_font = get_font(70, bold=True)

    for col, letter in enumerate(bingo_letters):
        letter_cell_x = grid_start_x + col * cell_size

        create_rounded_rectangle(
            draw,
            (letter_cell_x + 2, header_y, letter_cell_x + cell_size - 2, header_y + HEADER_HEIGHT),
            radius=12,
            fill=hex_to_rgb(COLORS['header_bg'])
        )

        bbox = draw.textbbox((0, 0), letter, font=letter_font)
        letter_width = bbox[2] - bbox[0]
        letter_height = bbox[3] - bbox[1]
        letter_x = letter_cell_x + (cell_size - letter_width) // 2
        letter_y = header_y + (HEADER_HEIGHT - letter_height) // 2 - bbox[1]

        draw.text((letter_x, letter_y), letter, fill=hex_to_rgb(COLORS['header_text']), font=letter_font)

    # === GRILLA DE IMÁGENES 3x3 ===
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

            # Colocar imagen
            if img_index < len(image_paths):
                try:
                    img = resize_image_to_cell(image_paths[img_index], cell_size)
                    img_x = cell_x + (cell_size - img.width) // 2
                    img_y = cell_y + (cell_size - img.height) // 2

                    if card.mode != 'RGBA':
                        card = card.convert('RGBA')

                    card.paste(img, (img_x, img_y), img)
                    draw = ImageDraw.Draw(card)
                except Exception as e:
                    print(f"Error con imagen: {e}")

            img_index += 1

    # === PIE DE PÁGINA ===
    footer_font = get_font(24)
    footer_text = f"Cartilla #{card_number:02d}"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_x = (CARD_WIDTH - (bbox[2] - bbox[0])) // 2
    footer_y = CARD_HEIGHT - MARGIN + 5

    draw.text((footer_x, footer_y), footer_text, fill=hex_to_rgb(COLORS['card_number']), font=footer_font)

    # Línea decorativa
    line_y = footer_y - 12
    line_width = 80
    line_x1 = (CARD_WIDTH - line_width) // 2
    draw.line([(line_x1, line_y), (line_x1 + line_width, line_y)],
              fill=hex_to_rgb(COLORS['accent']), width=3)

    # Convertir a RGB
    if card.mode == 'RGBA':
        background = Image.new('RGB', card.size, hex_to_rgb(COLORS['background']))
        background.paste(card, mask=card.split()[3])
        card = background

    return card

def generate_all_cards(num_cards=50):
    """Genera todas las cartillas de bingo 3x3"""
    print("=" * 60)
    print("   GENERADOR DE CARTILLAS DE BINGO 3x3")
    print("=" * 60)

    all_images = load_images()
    print(f"\nImágenes disponibles: {len(all_images)}")

    # Para 3x3 necesitamos 9 imágenes por cartilla
    images_per_card = GRID_SIZE * GRID_SIZE  # 9

    if len(all_images) < images_per_card:
        print(f"ERROR: Se necesitan al menos {images_per_card} imágenes, solo hay {len(all_images)}")
        return

    generated_combinations = set()

    print(f"\nGenerando {num_cards} cartillas 3x3...")
    print("-" * 40)

    for card_num in range(1, num_cards + 1):
        attempts = 0
        while attempts < 1000:
            selected = random.sample(all_images, images_per_card)
            combo_key = tuple(sorted([str(p) for p in selected]))

            if combo_key not in generated_combinations:
                generated_combinations.add(combo_key)
                break
            attempts += 1

        random.shuffle(selected)
        card = create_bingo_card(card_num, selected)

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
