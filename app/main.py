from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil, os

from app.services.ocr_extractor import extract_text_from_image
from app.services.mongo import save_to_mongo, get_all_records
from fastapi.responses import RedirectResponse
from app.services.mongo import delete_all_records

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def index(request: Request):
    records = await get_all_records()
    return templates.TemplateResponse("index.html", {"request": request, "records": records})

@app.post("/upload")
async def upload_file(request: Request, aadhaar_file: UploadFile = File(...), pan_file: UploadFile = File(...)):
    # Save files temporarily
    temp_aadhaar = f"temp_{aadhaar_file.filename}"
    temp_pan = f"temp_{pan_file.filename}"
    with open(temp_aadhaar, "wb") as buffer:
        shutil.copyfileobj(aadhaar_file.file, buffer)
    with open(temp_pan, "wb") as buffer:
        shutil.copyfileobj(pan_file.file, buffer)

    # Extract
    pan_data = extract_text_from_image(temp_pan)
    aadhaar_data = extract_text_from_image(temp_aadhaar)
    

    # Merge
    final_data = {
        "name": pan_data["name"] or aadhaar_data["name"] ,
        "dob": aadhaar_data["dob"] or pan_data["dob"],
        "aadhaar": aadhaar_data["aadhaar"],
        "pan": pan_data["pan"],
        "mobile": aadhaar_data["mobile"] or pan_data["mobile"],
        "uploaded_at": aadhaar_data["uploaded_at"]
    }

    await save_to_mongo(final_data)
    os.remove(temp_aadhaar)
    os.remove(temp_pan)

    records = await get_all_records()
    return templates.TemplateResponse("index.html", {"request": request, "records": records})

@app.post("/clear")
async def clear_records():
    await delete_all_records()
    return RedirectResponse("/", status_code=303)