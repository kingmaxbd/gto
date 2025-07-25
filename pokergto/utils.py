import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_value(label, text):
    label = label.lower()
    for line in text.splitlines():
        if line.lower().strip().startswith(label):
            return line.split(":", 1)[-1].strip()
    return ""
