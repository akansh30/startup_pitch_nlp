import os
import json
import pandas as pd

# Defining scoring dimensions
CATEGORIES = ["Problem", "Solution", "Market Size", "Traction", "Team", "Business Model", "Moat / Vision"]

def score_deck(deck_data):
    score_dict = {cat: 0.0 for cat in CATEGORIES}
    for slide in deck_data["slides"]:
        label = slide["label"]
        confidence = slide["confidence"]
        if label in score_dict:
            score_dict[label] += confidence
    return score_dict

def generate_insight(score, scores):
    p = scores.get("Problem", 0.0)
    s = scores.get("Solution", 0.0)
    m = scores.get("Market Size", 0.0)
    t = scores.get("Traction", 0.0)
    team = scores.get("Team", 0.0)
    bm = scores.get("Business Model", 0.0)
    moat = scores.get("Moat / Vision", 0.0)

    if score >= 5.0:
        return "Strong clarity and business signals i.e likely investor-ready."
    elif score >= 4.0:
        return "Good structure with strong team or market potential; traction may be modest."
    elif score >= 3.0:
        if team >= 1.0 and m >= 1.0:
            return "Balanced deck with strong team and clear market signals, but weak traction or moat."
        elif t > 0.5 and p > 0.5:
            return "Good early traction and clarity; could be more convincing on vision or defensibility."
        else:
            return "Decent clarity, but lacks strong market or team depth."
    elif score >= 2.0:
        if team > 1.0:
            return "Highlights a capable team, but lacks clarity on problem, traction, and defensibility."
        elif p > 0.7 and bm > 0.5:
            return "Basic idea with some business clarity, but lacks depth across team, market, and traction."
        else:
            return "Basic clarity present; but investability unclear without traction."
    else:
        return "Weak pitch with unclear signals; needs significant refinement."

def load_labeled_decks(folder_path):
    all_decks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                deck_data = json.load(f)
            scores = score_deck(deck_data)
            scores["Deck Name"] = deck_data["deck_name"]
            scores["Total Score"] = sum(scores[cat] for cat in CATEGORIES)
            scores["Investability Insight"] = generate_insight(scores["Total Score"], scores)
            all_decks.append(scores)
    return pd.DataFrame(all_decks)

def rank_and_save(df, output_path="results/deck_scores.csv"):
    df["Rank"] = df["Total Score"].rank(ascending=False, method="min").astype(int)
    df_sorted = df.sort_values(by="Total Score", ascending=False)
    df_sorted.to_csv(output_path, index=False)
    print(f"Scored decks saved to {output_path}")
    return df_sorted

if __name__ == "__main__":
    labeled_folder = "data/labeled"
    df_scores = load_labeled_decks(labeled_folder)
    ranked_df = rank_and_save(df_scores)
    print(ranked_df)
