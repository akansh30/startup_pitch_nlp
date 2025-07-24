import os
import json
import pandas as pd
from dotenv import load_dotenv
import openai

# Loading API key
load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_model = "llama3-70b-8192"

def call_llama(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=openai.api_model,
            messages=[
                {"role": "system", "content": "You are an expert VC analyst who evaluates startup pitch decks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=700
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("Error:", e)
        return "Error generating summary."

def format_text(deck_data):
    return "\n".join([f"Slide {slide['slide_num']}: {slide['text']}" for slide in deck_data["slides"]])

def generate_summary_and_category(deck_text):
    summary_prompt = f"""
You are an investor evaluating a startup based on its pitch deck slides.

From the slides below, extract the following:

1. Write exactly 4 clear and concise bullet points that summarize:
   - The problem being solved
   - The solution offered
   - Any traction or milestone evidence
   - The business model

2. Predict the startup's category (e.g., Fintech, HealthTech, SaaS, B2C, Logistics, etc.)

Slides:
{deck_text}

Return in this format (no extra symbols):

Summary:
- Bullet point 1
- Bullet point 2
- Bullet point 3
- Bullet point 4

Category: [your category]
"""
    return call_llama(summary_prompt)

def main():
    labeled_folder = "data/labeled"
    output_rows = []

    for filename in os.listdir(labeled_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(labeled_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                deck_data = json.load(f)

            deck_text = format_text(deck_data)
            result = generate_summary_and_category(deck_text)

            summary, category = "N/A", "Unknown"
            try:
                if "Summary:" in result and "Category:" in result:
                    summary = result.split("Summary:")[1].split("Category:")[0].strip()
                    category = result.split("Category:")[1].strip()
            except Exception as e:
                print(f"Failed parsing result for {filename}: {e}")

            output_rows.append({
                "Deck Name": deck_data["deck_name"],
                "Summary Bullets": summary,
                "Category": category
            })

    df = pd.DataFrame(output_rows)
    df.to_csv("results/deck_summaries.csv", index=False)
    print("Summaries saved to results/deck_summaries.csv")

if __name__ == "__main__":
    main()
