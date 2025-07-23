import os
import json
from tqdm import tqdm
from transformers import pipeline

# Paths
INPUT_FOLDER = "data/extracted_pdfs"
OUTPUT_FOLDER = "data/labeled"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define labels for classification
CATEGORIES = [
    "Problem",
    "Solution",
    "Market Size",
    "Traction",
    "Team",
    "Business Model",
    "Moat / Vision",
    "Ask",
    "Other"
]

# Load HuggingFace zero-shot classifier
print("Loading model...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print(" Model loaded!")

def classify_slide_text(text):
    """Classify slide content into one of the predefined categories."""
    result = classifier(text, candidate_labels=CATEGORIES, multi_label=False)
    label = result['labels'][0]  # top predicted label
    score = result['scores'][0]
    return label, score

def label_deck_slides(deck_path):
    """Apply classification to each slide in a deck."""
    with open(deck_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    for slide in deck_data["slides"]:
        label, confidence = classify_slide_text(slide["text"])
        slide["label"] = label
        slide["confidence"] = round(confidence, 4)

    return deck_data

def classify_all_decks():
    for filename in tqdm(os.listdir(INPUT_FOLDER)):
        if filename.endswith(".json"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            labeled_deck = label_deck_slides(input_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(labeled_deck, f, indent=2, ensure_ascii=False)

            print(f"Labeled: {filename} ({len(labeled_deck['slides'])} slides)")

# Run all
if __name__ == "__main__":
    classify_all_decks()
