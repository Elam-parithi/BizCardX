

import cv2
import matplotlib.pyplot as plt
import easyocr
import re
import os
import pandas as pd

reader = easyocr.Reader(['en'])

def process_image(image_path):
    image = cv2.imread(image_path)
    res = reader.readtext(image_path)
    for bbox, text, prob in res:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.axis('off')
    plt.imshow(image)
    return plt, res

def img_to_binary(file):
    with open(file, 'rb') as file:
        binaryData = file.read()
    return binaryData

def get_data(res, img_path):
    data = {
        "company_name": [],
        "card_holder": [],
        "designation": [],
        "mobile_number": [],
        "email": [],
        "website": [],
        "area": [],
        "city": [],
        "state": [],
        "pin_code": [],
        "image": img_to_binary(img_path)
    }

    for ind, i in enumerate(res):
        if "www" in i.lower():
            data["website"].append(i)
        elif "@" in i:
            data["email"].append(i)
        elif "-" in i:
            data["mobile_number"].append(i)
            if len(data["mobile_number"]) == 2:
                data["mobile_number"] = " & ".join(data["mobile_number"])
        elif ind == len(res) - 1:
            data["company_name"].append(i)
        elif ind == 0:
            data["card_holder"].append(i)
        elif ind == 1:
            data["designation"].append(i)
        if re.findall('^[0-9].+, [a-zA-Z]+', i):
            data["area"].append(i.split(',')[0])
        elif re.findall('[0-9] [a-zA-Z]+', i):
            data["area"].append(i)
        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
        match3 = re.findall('^[E].*', i)
        if match1:
            data["city"].append(match1[0])
        elif match2:
            data["city"].append(match2[0])
        elif match3:
            data["city"].append(match3[0])
        state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
        if state_match:
            data["state"].append(i[:9])
        elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
            data["state"].append(i.split()[-1])
        if len(data["state"]) == 2:
            data["state"].pop(0)
        if len(i) >= 6 and i.isdigit():
            data["pin_code"].append(i)
        elif re.findall('[a-zA-Z]{9} +[0-9]', i):
            data["pin_code"].append(i[10:])
    return data


