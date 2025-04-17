import easyocr
import re
import cv2
import numpy as np
from datetime import datetime

# Initialize EasyOCR with GPU support
reader = easyocr.Reader(['en'], gpu=True)


def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    processed_path = "processed_" + path.split("/")[-1]
    cv2.imwrite(processed_path, sharpened)
    return processed_path


def extract_text_from_image(image_path: str) -> dict:
    image_path = preprocess_image(image_path)
    result = reader.readtext(image_path, detail=0)
    text = " ".join(result)

    extracted = {
        "name": None,
        "dob": None,
        "pan": None,
        "aadhaar": None,
        "mobile": None,
        "uploaded_at": datetime.utcnow()
    }

    print("\n🔍 OCR Detected Lines:")
    for line in result:
        print(line)

    # Flatten lines
    lines = [str(l).strip() for l in result]

    # === PAN ===
    for line in lines:
        match = re.search(r"[A-Z]{5}[0-9O]{4}[A-Z]", line)
        if match:
            pan = match.group()
            pan = pan[:5] + pan[5:9].replace("O", "0") + pan[9]
            extracted["pan"] = pan
            break

    # === Aadhaar ===
    for line in lines:
        match = re.search(r"\d{4}[\s\-]?\d{4}[\s\-]?\d{4}", line)
        if match:
            extracted["aadhaar"] = match.group().replace(" ", "").replace("-", "")
            break

    # === DOB ===
    for line in lines:
        match = re.search(r"\d{2}/\d{2}/\d{4}", line) or re.search(r"\d{4}-\d{2}-\d{2}", line)
        if match:
            extracted["dob"] = match.group()
            break

    # === MOBILE NUMBER ===
    for line in lines:
        match = re.search(r"(?:\+91[\-\s]?)?[6-9]\d{9}", line)
        if match:
            extracted["mobile"] = match.group().replace("+91", "").replace("-", "").replace(" ", "")
            break

    # === NAME Extraction ===
    name_keywords = ["name"]
    ignored_keywords = [
        "income", "tax", "govt", "india", "department", "permanent", "father", "date",
        "account", "number", "signature", "birth"
    ]

    # Step 1: Detect "Name" line and take the next clean uppercase line
    for i, line in enumerate(lines):
        current = line.strip().lower()
        if any(kw == current for kw in name_keywords):
            for j in range(i + 1, min(i + 4, len(lines))):  # Look up to 3 lines after
                next_line = lines[j].strip()
                if (
                    next_line.isupper()
                    and len(next_line.split()) >= 2
                    and all(w.isalpha() for w in next_line.split())
                ):
                    extracted["name"] = next_line.title()
                    break
            if extracted["name"]:
                break

    # Step 2: Fallback - first likely uppercase name line (not junk)
    if not extracted["name"]:
        for line in lines:
            clean = line.strip().upper()
            if any(kw in clean for kw in ignored_keywords):
                continue
            if (
                clean.isupper()
                and len(clean.split()) >= 2
                and all(w.isalpha() for w in clean.split())
            ):
                extracted["name"] = clean.title()
                break

    # Step 3: Last resort fallback
    if not extracted["name"] and len(lines) > 1:
        fallback = lines[1].strip()
        if all(kw not in fallback.upper() for kw in ignored_keywords):
            extracted["name"] = fallback.title()

    return extracted
