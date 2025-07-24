# Startup Pitch Deck Evaluation with NLP 

This project analyzes startup pitch decks using NLP and zero-shot classification to extract insights and compute composite quality scores across business dimensions.

---

##  Project Workflow and File Flow

| Step | File | Output Location |
|------|------|-----------------|
|1️| `parse_pdf.py` | → `data/extracted_pdf/` (Extracted text from PDFs) |
|2️| `classify_slides.py` | → `data/labeled/` (Slides labeled with categories and confidence) |
|3️| `score_decks.py` | → `results/deck_scores.csv` (Scored decks with insights and ranking) |
|4️| `visualize_scores.py` | → `output_visualizations/` (Radar charts, heatmaps, and barplot) |
|5️| `generate_summaries.py` | → `results/deck_summaries.csv` (LLM-based 4-bullet summaries and categories) |

---

## Step-by-Step Approach

### 1. **PDF Parsing**
- Used `PyMuPDF`and `pytesseract` to extract structured text from pitch deck PDFs.
- Each slide's text was separated and cleaned.
- Output saved in `data/extracted_pdf/`.

### 2. **Slide Classification**
- Each slide was passed through a **zero-shot classifier**.
- The model `facebook/bart-large-mnli` assigned one of nine business labels:
  - `Problem`, `Solution`, `Market Size`, `Traction`, `Team`, `Business Model`, `Moat / Vision` , `Ask`,
    `Other`
- The confidence score for each classification was stored.
- Output saved in `data/labeled/`.

### 3. **Scoring Pitch Decks**
- Each labeled slide contributes its confidence score to the matching category.
- Scores are summed across all 6 dimensions.
- The total score determines a deck's quality.
- A custom one-liner **Investability Insight** is generated based on logic defined.
- Output saved in `results/deck_scores.csv`.

### 4. **Visualization**
- Radar charts, correlation heatmaps, and barplots are generated.
- Helps visually compare strengths and weaknesses across decks.
- Output images are saved in `output_visualizations/`.

### 5. **LLM-Based Summary Generation**
- Used `GROQ's LLaMA 3` API to generate:
  - 4 bullet point summaries
  - Predicted category (e.g. Logistics, Tech, etc.)
- Output saved in `results/deck_summaries.csv`.

---

## Visualizations

<img width="2379" height="595" alt="image" src="https://github.com/user-attachments/assets/6384def9-bebf-4f30-84ca-1bf43b0984a6" />


