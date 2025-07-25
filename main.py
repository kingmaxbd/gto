from pokergto.screenshot import take_screenshot_window_under_mouse
from pokergto.ocr_parser import fix_card_info_with_ocr_and_color
from pokergto.utils import encode_image_to_base64
from pokergto.gpt_api import send_to_openai_parse_table, send_to_openai_gto_decision
from pokergto.utils import encode_image_to_base64, extract_value
import os
import keyboard

def main():
    print("⏳ Waiting for Ctrl+S to analyze poker spot...")
    keyboard.wait("ctrl+s")

    img_path = take_screenshot_window_under_mouse()
    b64 = encode_image_to_base64(img_path)

    parsed_text = send_to_openai_parse_table(b64)
    if parsed_text:
        parsed_text = fix_card_info_with_ocr_and_color(parsed_text, img_path)
        print("\n📋 Parsed Table (Corrected):\n" + parsed_text)

        decision = send_to_openai_gto_decision(parsed_text)

        hole_cards = extract_value("hole cards", parsed_text)
        board = extract_value("board", parsed_text)
        pot = extract_value("pot", parsed_text)
        stack = extract_value("your stack", parsed_text)

        summary = f"{hole_cards} | Board: {board} | Pot: {pot} | Stack: {stack} | EV → {decision}"
        print("\n🎯 Final Decision:")
        print(summary)

    #os.remove(img_path)
    print(f"🗑️ Screenshot {img_path} deleted.")

if __name__ == "__main__":
    main()
