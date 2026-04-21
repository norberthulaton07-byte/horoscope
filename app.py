import json
import os
import random

from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    import anthropic
except ImportError:
    anthropic = None


app = Flask(__name__)
CORS(app)

VALID_SIGNS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]

SIGN_DATES = {
    "aries": "March 21 - April 19",
    "taurus": "April 20 - May 20",
    "gemini": "May 21 - June 20",
    "cancer": "June 21 - July 22",
    "leo": "July 23 - August 22",
    "virgo": "August 23 - September 22",
    "libra": "September 23 - October 22",
    "scorpio": "October 23 - November 21",
    "sagittarius": "November 22 - December 21",
    "capricorn": "December 22 - January 19",
    "aquarius": "January 20 - February 18",
    "pisces": "February 19 - March 20",
}

FALLBACK_COLORS = [
    "Crimson",
    "Emerald",
    "Sapphire",
    "Amber",
    "Silver",
    "Midnight Blue",
    "Lavender",
    "Coral",
]

FOCUS_GUIDANCE = {
    "general": "Pay attention to the mood of the day and the choices in front of you.",
    "love": "Open conversations may reveal a softer truth you were not expecting.",
    "career": "A steady approach will do more for you than rushing for quick recognition.",
    "health": "Listen to your body's pace and make room for rest as well as effort.",
    "finances": "Small practical decisions may create a stronger sense of security.",
}

FOCUS_QUOTES = {
    "general": "The day unfolds best when you notice what keeps returning to your attention.",
    "love": "Matters of the heart respond better to sincerity than to perfect timing.",
    "career": "Progress grows through consistency, especially when others are only watching for big moments.",
    "health": "Your energy steadies when you treat rest and effort as partners instead of opposites.",
    "finances": "Practical choices carry extra weight now, and careful planning can create real relief.",
}

FOCUS_OPENINGS = {
    "general": "A subtle rhythm follows you today, and small signs may carry more meaning than usual.",
    "love": "A softer emotional current moves around you today, inviting honesty and warmth.",
    "career": "The stars lean toward steady ambition today, rewarding patience and clear priorities.",
    "health": "A grounding energy surrounds you today, encouraging balance in both body and mind.",
    "finances": "A practical cosmic pulse guides you today, helping wise choices stand out from impulsive ones.",
}

FOCUS_TIPS = {
    "general": "Keep your attention on the one thing that feels both calm and important.",
    "love": "Say what you mean gently, and listen for what is not said out loud.",
    "career": "Handle the task that builds trust before the one that brings attention.",
    "health": "Choose the habit that helps your body feel supported, not pressured.",
    "finances": "Review one spending choice carefully before making the next move.",
}

SIGN_QUOTES = {
    "aries": "A spark of courage follows you today, and the stars favor bold but thoughtful action.",
    "taurus": "Steady ground returns beneath your feet, and calm choices carry unusual strength.",
    "gemini": "Your mind moves quickly today, and one conversation may open a door you did not expect.",
    "cancer": "Your intuition is especially clear now, guiding you toward what feels safe and true.",
    "leo": "A warm light surrounds your efforts today, drawing attention to the gifts you share freely.",
    "virgo": "Small details begin to form a larger pattern, and your patience helps everything settle into place.",
    "libra": "Balance comes through honesty today, and gentle words may restore harmony around you.",
    "scorpio": "Hidden truths rise to the surface, giving you the chance to move with deeper confidence.",
    "sagittarius": "A restless spark invites you forward, and even a simple step may feel like an adventure.",
    "capricorn": "Discipline becomes your quiet advantage today, turning effort into visible progress.",
    "aquarius": "Fresh ideas gather around you now, and originality becomes your strongest guide.",
    "pisces": "Dreamlike insight colors the day, helping you notice meaning where others see only routine.",
}

SIGN_TIPS = {
    "aries": "Lead with courage, but let patience choose the final move.",
    "taurus": "Protect your peace before saying yes to extra demands.",
    "gemini": "Write down the idea that returns twice today.",
    "cancer": "Trust the place where your heart feels most at ease.",
    "leo": "Share your confidence, but leave room for someone else to shine too.",
    "virgo": "Finish one small task completely before starting another.",
    "libra": "Choose the honest answer, even if it takes longer to say kindly.",
    "scorpio": "Keep one plan private until it feels ready to grow.",
    "sagittarius": "Say yes to curiosity, but keep one foot on practical ground.",
    "capricorn": "Take the slow, solid route instead of the impressive shortcut.",
    "aquarius": "Follow the unusual idea that still makes practical sense.",
    "pisces": "Give your intuition a moment of silence before making a choice.",
}

SIGN_COLORS = {
    "aries": "Crimson",
    "taurus": "Emerald",
    "gemini": "Yellow Gold",
    "cancer": "Pearl White",
    "leo": "Sunset Orange",
    "virgo": "Olive Green",
    "libra": "Rose Pink",
    "scorpio": "Midnight Blue",
    "sagittarius": "Royal Purple",
    "capricorn": "Slate Gray",
    "aquarius": "Electric Blue",
    "pisces": "Seafoam",
}


def build_fallback_horoscope(sign, focus):
    focus_line = FOCUS_GUIDANCE.get(focus, FOCUS_GUIDANCE["general"])
    focus_quote = FOCUS_QUOTES.get(focus, FOCUS_QUOTES["general"])
    focus_tip = FOCUS_TIPS.get(focus, FOCUS_TIPS["general"])
    focus_opening = FOCUS_OPENINGS.get(focus, FOCUS_OPENINGS["general"])
    lucky_number = random.randint(1, 99)
    lucky_color = SIGN_COLORS.get(sign, random.choice(FALLBACK_COLORS))
    sign_opening = SIGN_QUOTES.get(
        sign,
        f"{sign.capitalize()} moves through the day with quiet momentum, and subtle signals may prove more useful than dramatic ones.",
    )

    reading = (
        f"{sign_opening} {focus_opening} {focus_quote} {focus_line} Trust the pattern that keeps returning to your attention, "
        f"because it may be pointing toward your next good step in this area of life."
    )

    return {
        "reading": reading,
        "lucky_tip": (
            f"{SIGN_TIPS.get(sign, 'Pause before reacting, then choose the calmer path.')} "
            f"{focus_tip}"
        ),
        "lucky_number": lucky_number,
        "lucky_color": lucky_color,
    }


def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or anthropic is None:
        return None
    return anthropic.Anthropic(api_key=api_key)


@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "name": "Horoscope API",
            "version": "1.0",
            "description": "Cross-language integration: Python API + JavaScript frontend",
            "endpoints": {
                "GET /": "API information",
                "GET /signs": "List all valid zodiac signs",
                "GET /horoscope/<sign>": "Get a horoscope for a zodiac sign",
            },
        }
    )


@app.route("/signs", methods=["GET"])
def get_signs():
    signs_data = [{"sign": sign, "dates": SIGN_DATES[sign]} for sign in VALID_SIGNS]
    return jsonify({"signs": signs_data, "total": len(signs_data)})


@app.route("/horoscope/<sign>", methods=["GET"])
def get_horoscope(sign):
    sign = sign.lower().strip()
    if sign not in VALID_SIGNS:
        return jsonify(
            {
                "error": f"'{sign}' is not a valid zodiac sign.",
                "valid_signs": VALID_SIGNS,
            }
        ), 400

    focus = request.args.get("focus", "general").lower().strip() or "general"
    client = get_anthropic_client()

    if client is None:
        return jsonify(
            {
                "sign": sign.capitalize(),
                "dates": SIGN_DATES[sign],
                "focus": focus,
                "horoscope": build_fallback_horoscope(sign, focus),
                "generated_by": "Local fallback generator",
            }
        )

    prompt = f"""You are a mystical astrologer. Generate a horoscope reading for {sign.capitalize()} ({SIGN_DATES[sign]}).

Focus area: {focus}

Write a horoscope that is:
- 3-4 sentences long
- Mystical and poetic in tone
- Positive but realistic
- Specific enough to feel personal

Respond in this exact JSON format with no markdown:
{{
  "reading": "The main horoscope text here.",
  "lucky_tip": "Your lucky tip here.",
  "lucky_number": 7,
  "lucky_color": "A color name"
}}"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        horoscope_data = json.loads(raw)
        generated_by = "Claude AI (Anthropic)"
    except json.JSONDecodeError:
        horoscope_data = build_fallback_horoscope(sign, focus)
        generated_by = "Claude fallback parser"
    except Exception as exc:
        return jsonify({"error": "Failed to generate horoscope.", "details": str(exc)}), 500

    return jsonify(
        {
            "sign": sign.capitalize(),
            "dates": SIGN_DATES[sign],
            "focus": focus,
            "horoscope": horoscope_data,
            "generated_by": generated_by,
        }
    )


if __name__ == "__main__":
    print("Horoscope API running on http://localhost:5000")
    print("JavaScript frontend can now call this Python API.")
    app.run(debug=True, port=5000)
