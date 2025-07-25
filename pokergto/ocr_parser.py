import easyocr
import torch
import re
import numpy as np
from PIL import Image

def detect_card_color(image: Image.Image, box) -> str:
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = box
    cx = int((x1 + x2 + x3 + x4) / 4)
    cy = int((y1 + y2 + y3 + y4) / 4)
    r, g, b = image.getpixel((cx, cy))
    return 'red' if r > g and r > b and r > 100 else 'black'

def fix_card_info_with_ocr_and_color(parsed_text: str, image_path: str) -> str:
    gpu_enabled = torch.cuda.is_available()
    reader = easyocr.Reader(['en'], gpu=True)
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)
    results = reader.readtext(image_np)

    cards = []
    for box, text, conf in results:
        cleaned = text.replace(" ", "").upper()
        if re.match(r'^(10|[2-9AJQK])[♠♥♦♣SHDC]$', cleaned) and conf > 0.4:
            color = detect_card_color(image, box)
            rank = cleaned[:-1]
            suit_char = cleaned[-1]
            if color == 'red':
                suit = '♥' if suit_char in ['H', '♥'] else '♦'
            else:
                suit = '♠' if suit_char in ['S', '♠'] else '♣'
            cards.append(f"{rank}{suit}")

    cards = cards[:7]
    hole_cards = " ".join(cards[:2]) if len(cards) >= 2 else ""
    board_cards = " ".join(cards[2:]) if len(cards) > 2 else ""

    def replace_line(label, value, text):
        pattern = re.compile(f"{label}:.*", re.IGNORECASE)
        return re.sub(pattern, f"{label}: {value}", text)

    if hole_cards:
        parsed_text = replace_line("Hole cards", hole_cards, parsed_text)
    if board_cards:
        parsed_text = replace_line("Board", board_cards, parsed_text)

    return parsed_text
