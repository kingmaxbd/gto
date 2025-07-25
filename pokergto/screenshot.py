import mss
import pygetwindow as gw
import pyautogui
from PIL import Image, ImageEnhance
from datetime import datetime
import os

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot_window_under_mouse():
    x, y = pyautogui.position()

    for win in gw.getWindowsWithTitle(""):
        if not win.visible or win.width == 0 or win.height == 0:
            continue

        if win.left <= x <= win.left + win.width and win.top <= y <= win.top + win.height:
            left, top, width, height = win.left, win.top, win.width, win.height

            with mss.mss() as sct:
                monitor = {"left": left, "top": top, "width": width, "height": height}
                screenshot = sct.grab(monitor)

                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                img = ImageEnhance.Contrast(img).enhance(1.5)
                img = ImageEnhance.Brightness(img).enhance(1.1)

                filename = f"{SCREENSHOT_DIR}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                img.save(filename, "PNG")
                print(f"✅ Screenshot saved: {filename}")
                return filename

    print("❌ No window found under cursor.")
    return None
