import matplotlib.pyplot as plt
import easyocr
import re
import os
import pandas as pd
from PIL import Image, ImageDraw

# Initialize EasyOCR Reader only once
reader = easyocr.Reader(['en'], gpu=True)

def process_image(image_path):
    """ Reads text from image and annotates detected text """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    # Perform OCR
    results = reader.readtext(image_path)

    for bbox, text, prob in results:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))

        draw.rectangle([tl, br], outline="green", width=2)
        draw.text((tl[0], tl[1] - 10), text, fill="blue")

    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

    return results

def img_to_binary(file_path):
    """ Convert image to binary data for storage """
    with open(file_path, 'rb') as file:
        return file.read()

def extract_data(results, img_path):
    """ Extract structured data from OCR results """
    data = {
        "company_name": "",
        "card_holder": "",
        "designation": "",
        "mobile_number": "",
        "email": "",
        "website": "",
        "area": "",
        "city": "",
        "state": "",
        "pin_code": "",
        "image": img_to_binary(img_path)
    }

    mobile_numbers = []

    for index, (bbox, text, prob) in enumerate(results):
        text = text.strip()

        if "www" in text.lower() or "http" in text.lower():
            data["website"] = text
        elif "@" in text:
            data["email"] = text
        elif re.match(r'^\+?\d{1,3}?[-.\s]?\(?\d{2,5}?\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}$', text):
            mobile_numbers.append(text)
        elif index == 0:
            data["card_holder"] = text
        elif index == 1:
            data["designation"] = text
        elif index == len(results) - 1:
            data["company_name"] = text

        # Address extraction
        if re.search(r'^[0-9].+, [a-zA-Z]+', text):
            data["area"] = text.split(',')[0]
        elif re.search(r'[0-9] [a-zA-Z]+', text):
            data["area"] = text

        # City extraction
        city_match = re.search(r'.+St , ([a-zA-Z]+)', text) or re.search(r'.+St,, ([a-zA-Z]+)', text)
        if city_match:
            data["city"] = city_match.group(1)

        # State extraction
        state_match = re.search(r'([a-zA-Z]{9}) +[0-9]', text)
        if state_match:
            data["state"] = state_match.group(1)

        # PIN Code extraction
        if re.match(r'^\d{6}$', text):
            data["pin_code"] = text

    # Format mobile numbers
    if len(mobile_numbers) == 2:
        data["mobile_number"] = " & ".join(mobile_numbers)
    elif mobile_numbers:
        data["mobile_number"] = mobile_numbers[0]
    return data

if __name__ == "__main__":
    image_path = r"../Sample_dataset/1.png"
    print("pass 1")
    results = process_image(image_path)
    print("pass 1")
    extracted_data = extract_data(results, image_path)
    print(pd.DataFrame([extracted_data]))
