from rapidfuzz import process
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Define primary categories and sub-categories 
CATEGORY_MAP = {
    "Food": [
        "grocery", "restaurant", "fast food", "coffee", "snacks", "food delivery",
        "bakery", "alcohol", "takeaway"
    ],
    "Transport": [
        "bus", "train", "taxi", "fuel", "ride-sharing", "car maintenance",
        "public transport pass", "parking", "toll fees", "bike rental"
    ],
    "Entertainment": [
        "movies", "concerts", "subscriptions", "gaming",
        "theme park", "sports events", "streaming services",
        "music concerts", "board games"
    ],
    "Health": [
        "doctor", "medicine", "gym", "therapy", "dentist",
        "insurance", "supplements", "mental health", "hospital visits"
    ],
    "Utilities": [
        "electricity", "water", "internet", "phone bill",
        "gas", "cable TV", "waste management", "home security"
    ],
    "Shopping": [
        "clothing", "electronics", "home appliances", "furniture",
        "beauty products", "online shopping", "toys", "accessories"
    ],
    "Education": [
        "school fees", "online courses", "tuition", "books"
        "certifications", "educational subscriptions", "stationery",
        "college expenses"
    ],
    "Personal Care": [
        "haircut", "spa", "cosmetics", "wellness", "skincare",
        "massages", "nail salon", "fragrances"
    ],
    "Travel": [
        "airfare", "hotel", "car rental", "sightseeing",
        "travel insurance", "luggage", "souvenirs", "cruise"
    ],
}


# Lemmatize subcategories in CATEGORY_MAP
CATEGORY_MAP_LEMMATIZED = {
    primary: [lemmatizer.lemmatize(sub.lower()) for sub in subcategories]
    for primary, subcategories in CATEGORY_MAP.items()
}

def standardize_category(user_input: str) -> tuple:
    user_input = user_input.strip().lower()
    base_word = lemmatizer.lemmatize(user_input)  # Lemmatize user input
    print(f"Input: {user_input}, Base Word: {base_word}")  # Debugging

    best_category = None
    best_subcategory = None
    highest_score = 0

    # First, try to match the input with subcategories
    for primary, subcategories in CATEGORY_MAP_LEMMATIZED.items():
        result = process.extractOne(base_word, subcategories, score_cutoff=80)  # Match lemmatized subcategories
        print(f"Primary: {primary}, Result: {result}")  # Debugging
        if result:
            match, score = result[:2]
            if score > highest_score:
                best_category = primary
                best_subcategory = match
                highest_score = score

    # If no subcategory match, try to match the input with primary categories
    if not best_category:
        result = process.extractOne(base_word, CATEGORY_MAP_LEMMATIZED.keys(), score_cutoff=80)  # Match lemmatized primary categories
        print(f"Primary Category Result: {result}")  # Debugging
        if result:
            match, score = result[:2]
            best_category = match
            best_subcategory = None

    print(f"Best Category: {best_category}, Best Subcategory: {best_subcategory}")  # Debugging
    return best_category, best_subcategory