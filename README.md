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

---
## Scoring Logic

Each pitch deck is first analyzed and its slides are classified into `9 `categories using a `zero-shot classification model`. These categories include `Problem, Solution, Market Size, Traction, Team, Business Model, Moat or Vision, Ask, and Other`.
However, for scoring purposes, I only focus on `6` of the most important categories from an investor’s point of view. These are `Problem, Market Size, Traction, Team, Business Model, and Moat or Vision`. These categories reflect the main signals that investors usually look for when evaluating a startup.
The scoring system works by adding up the confidence levels assigned by the classifier for each of these six dimensions. So if a pitch deck clearly explains its problem and team, and the model is confident in those classifications, the deck will receive `higher scores` in those areas. The total score is calculated by summing all six category scores.
After the total score is calculated, a short insight is also generated to describe the investability of the deck. This insight is based on how strong the scores are across different categories and gives a quick summary of how promising the startup looks from an investor’s perspective
---

## Why facebook/bart-large-mnli?

I used this model because it's a powerful `zero-shot classification model`. It helps categorize each slide in a pitch deck even if the model hasn’t seen those categories during training. This means it can understand and label slide content into topics like Problem, Market Size, or Team without needing custom training. It's a great fit for extracting structure from unstructured text.

## Why Tesseract?

Some of the pitch decks (4 PDFs) were not machine-readable..they were scanned or image-based. So I used Tesseract to extract text from those slides using OCR.

## Why Groq LLaMA 3?
I used the Groq LLaMA 3 model because it is a fast and powerful open-weight model. It helped generate summaries and classify startups based on their pitch decks. Being open and efficient made it a good fit for this task.

---

##  Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/akansh30/startup_pitch_nlp.git
cd startup_pitch_nlp
```
### 2. Create virtual environment
```bash
uv venv .venv
Source .venv\Scripts\activate  # On Windows
```
### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```
### 4. Add API keys
Create a `.env` file in the root directory and add:
```bash
GROQ_API_KEY=your_api_key_here
```



