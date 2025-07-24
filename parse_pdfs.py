import os
import json
from tqdm import tqdm
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

PDF_FOLDER = "data/raw_pdfs"
OUTPUT_FOLDER = "data/extracted_pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_with_ocr(pdf_path):
    """Convert PDF pages to images and extract text using Tesseract OCR"""
    slides = []
    images = convert_from_path(pdf_path, dpi=300)
    
    for i, img in enumerate(images, start=1):
        text = pytesseract.image_to_string(img)
        if text.strip():
            slides.append({
                "slide_num": i,
                "text": text.strip()
            })
    return slides

def process_all_pdfs_with_ocr(folder_path):
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith(".pdf"):
            deck_name = os.path.splitext(filename)[0]
            pdf_path = os.path.join(folder_path, filename)

            slides = extract_text_with_ocr(pdf_path)

            output = {
                "deck_name": deck_name,
                "slides": slides
            }

            with open(os.path.join(OUTPUT_FOLDER, f"{deck_name}.json"), "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"OCR Extracted: {deck_name} ({len(slides)} slides)")

# Runing the OCR extraction
process_all_pdfs_with_ocr(PDF_FOLDER)