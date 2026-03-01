import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "wardrobe_data.json")
with open(DATA_PATH, "r") as f:
    WARDROBE_DATA = json.load(f)


def get_age_tip(age):
    tips = {
        "Teen": "💡 Keep it fun and expressive — bold prints and relaxed silhouettes work great for your age.",
        "20s":  "💡 Experiment freely — mix trends with timeless basics to build a signature style.",
        "30+":  "💡 Invest in quality staples. Refined fits and classic cuts elevate any look effortlessly.",
    }
    return tips.get(age, "💡 Dress for confidence — style is always personal.")


def get_color_palette(data, complexity):
    colors = data.get("colors", {})
    palette = colors.get(complexity, [])
    return ", ".join(palette) if palette else "Versatile neutrals"


def generate_recommendation(age, gender, occasion, theme, complexity, nationality=None):
    if not gender or not occasion:
        return {
            "text": "Please select all required fields.",
            "outfit_img": "", "footwear_img": "", "accessories_img": "",
            "outfit_detail": "", "footwear_detail": "", "accessories_detail": "",
            "color_palette": "", "occasion": "", "theme": "", "complexity": "", "gender": "",
        }

    gender = gender.lower()
    gender_cap = gender.capitalize()
    occasion_cap = occasion.capitalize()

    # Retrieve wardrobe data
    outfit_detail = footwear_detail = accessories_detail = color_palette = ""
    try:
        if occasion_cap == "Wedding":
            nat = (nationality or "indian").lower().capitalize()
            section = WARDROBE_DATA.get("Wedding", {}).get(nat, {}).get(gender_cap, {})
        else:
            section = WARDROBE_DATA.get(occasion_cap, {}).get(gender_cap, {})

        outfit_detail      = section.get("outfit", "A stylish outfit tailored for the occasion")
        footwear_detail    = section.get("footwear", "Coordinated footwear")
        accessories_detail = section.get("accessories", "Elegant accessories")
        color_palette      = get_color_palette(section, complexity or "Balanced")
    except Exception:
        outfit_detail = "A stylish outfit tailored for the occasion"
        footwear_detail = "Coordinated footwear"
        accessories_detail = "Elegant accessories"
        color_palette = "Classic neutrals"

    age_tip = get_age_tip(age)
    nat_label = f" · {nationality.capitalize()} Style" if occasion_cap == "Wedding" and nationality else ""

    recommendation_text = (
        f"✨ Your Personalized Style Recommendation\n\n"
        f"Occasion: {occasion_cap}{nat_label}\n"
        f"Theme: {theme or 'Neutral'} · Color Style: {complexity or 'Balanced'}\n\n"
        f"👗 Outfit\n{outfit_detail}\n\n"
        f"👞 Footwear\n{footwear_detail}\n\n"
        f"💎 Accessories\n{accessories_detail}\n\n"
        f"🎨 Suggested Colors: {color_palette}\n\n"
        f"{age_tip}"
    )

    # Image logic
    if occasion_cap == "Casual":
        outfit_img = f"/static/images/casual_{gender}.jpg"
    elif occasion_cap == "Interview":
        outfit_img = f"/static/images/interview_{gender}.jpg"
    elif occasion_cap == "Party":
        outfit_img = f"/static/images/party_{gender}.jpg"
    elif occasion_cap == "Wedding":
        nat_key = (nationality or "indian").lower()
        outfit_img = f"/static/images/wedding_{nat_key}_{gender}.jpg"
    else:
        outfit_img = f"/static/images/casual_{gender}.jpg"

    if gender == "male":
        footwear_img = "/static/images/formal_shoes_male.jpg"
        accessories_img = "/static/images/watch_male.jpg"
    else:
        footwear_img = "/static/images/heels_female.jpg"
        accessories_img = "/static/images/jewelry_female.jpg"

    if occasion_cap == "Casual":
        footwear_img = f"/static/images/sneakers_{gender}.jpg"

    return {
        "text": recommendation_text,
        "outfit_img": outfit_img,
        "footwear_img": footwear_img,
        "accessories_img": accessories_img,
        "outfit_detail": outfit_detail,
        "footwear_detail": footwear_detail,
        "accessories_detail": accessories_detail,
        "color_palette": color_palette,
        "occasion": occasion_cap,
        "theme": theme or "Neutral",
        "complexity": complexity or "Balanced",
        "gender": gender_cap,
    }
