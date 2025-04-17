Here’s a clean, professional ✅ **`README.md`** for your Aadhaar + PAN OCR extraction project with MongoDB, FastAPI, and Tailwind UI.

---

## 📄 `README.md`

```markdown
# 🆔 Identity OCR Extractor

An AI-powered web app built with **FastAPI**, **EasyOCR**, and **MongoDB** to extract structured data like **Name**, **PAN**, **Aadhaar**, **DOB**, and **Mobile Number** from uploaded Aadhaar and PAN card images. Data is displayed in a responsive frontend and saved in a cloud MongoDB collection.

---

## 🚀 Features

- 🖼️ Upload Aadhaar & PAN card images
- 🔍 Extract:
  - ✅ Full Name
  - ✅ PAN Number
  - ✅ Aadhaar Number
  - ✅ Date of Birth (DOB)
  - ✅ Mobile Number (if present)
- 💾 Save data to MongoDB
- 📋 Display all extracted records in a clean table
- 🧹 One-click **Clear Table** feature
- ⚡ GPU-accelerated OCR (EasyOCR with CUDA)
- 🌐 Tailwind-based frontend for responsive UI

---

## 📦 Tech Stack

| Layer       | Tool/Library         |
|-------------|----------------------|
| Backend     | FastAPI              |
| OCR Engine  | EasyOCR + OpenCV     |
| Database    | MongoDB (local/Atlas)|
| Frontend    | Jinja2 + Tailwind CSS|
| OCR Boost   | GPU + Image Sharpening|

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/identity-ocr-extractor.git
cd identity-ocr-extractor
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Update MongoDB URI

Edit `app/services/mongo.py` and replace the connection string:
```python
client = AsyncIOMotorClient("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority")
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Then open your browser at:  
👉 `http://localhost:8000`

---

## 📁 Folder Structure

```
identity-ocr-extractor/
├── app/
│   ├── main.py                # FastAPI app & routing
│   ├── services/
│   │   ├── ocr_extractor.py   # OCR + data extraction logic
│   │   └── mongo.py           # MongoDB connection and CRUD
│   ├── templates/
│   │   └── index.html         # Tailwind UI for table + upload form
│   └── static/                # (optional) Static assets
├── requirements.txt
├── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to fork the repo and submit a PR.
