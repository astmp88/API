from flask import Flask, jsonify, request
from groq import Groq
import os
import random
from datetime import datetime
from flask import render_template 

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Mystical themes to randomize the fortunes
MYSTICAL_THEMES = [
    "cosmic alignment",
    "ancient prophecy",
    "crystal ball vision",
    "tarot cards",
    "tea leaves",
    "dragon's breath",
    "unicorn whispers",
    "mystical runes",
    "enchanted forest spirits",
    "celestial bodies",
    "magical potions",
    "wizard's scroll"
]

FORTUNE_STYLES = [
    "mysterious and cryptic",
    "overly dramatic and theatrical",
    "comically specific and oddly detailed",
    "zen-like with nonsensical wisdom",
    "rhyming like a bad poem",
    "like a confused fortune cookie mixed with horoscope"
]

def generate_fortune():
    """Generate a humorous, mystical fortune using Groq API"""
    
    # Randomly select theme and style
    theme = random.choice(MYSTICAL_THEMES)
    style = random.choice(FORTUNE_STYLES)
    
    # Create a fun prompt for Groq
    prompt = f"""Your prophecies are funny, a bit sarcastic, over-the-top, and full of mystic nonsense.
Generate a single, funny fortune that is {style}.
The fortune should reference {theme}.
Keep it to 1-3 sentences maximum.
Make it amusing, whimsical, and slightly absurd, but still sound mystical.

Do NOT include any introduction or explanation, just give the fortune itself."""

    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a humorous mystical fortune teller but also a bit sarcastic"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.2,
            max_tokens=150
        )
        
        fortune_text = chat_completion.choices[0].message.content.strip('"').strip("'")
        
        return {
            "fortune": fortune_text,
            "theme": theme,
            "style": style,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "fortune": "The spirits are too busy watching octopus videos! Try again later! 🔮",
            "timestamp": datetime.now().isoformat()
        }

@app.route('/web')
def web_interface():
    return render_template('magic_fortuneteller.html')

@app.route('/')
def home():
    """Welcome page with API instructions"""
    return jsonify({
        "message": "🔮 Welcome to the Mystical Fortune API! 🔮",
        "endpoints": {
            "/fortune": "GET - Receive your magical destiny",
            "/fortune/batch": "GET - Receive multiple fortunes (use ?count=N parameter)"
        },
        "example": "Try: GET /fortune"
    })

@app.route('/fortune', methods=['GET'])
def get_fortune():
    """Main endpoint to get a single fortune"""
    fortune_data = generate_fortune()
    return jsonify(fortune_data)

@app.route('/fortune/batch', methods=['GET'])
def get_multiple_fortunes():
    """Get multiple fortunes at once"""
    count = request.args.get('count', default=3, type=int)
    
    # Limit to reasonable number
    if count > 10:
        return jsonify({
            "error": "The mystical energies can only handle 10 fortunes at once!"
        }), 400
    
    if count < 1:
        return jsonify({
            "error": "You must request at least 1 fortune!"
        }), 400
    
    fortunes = []
    for _ in range(count):
        fortunes.append(generate_fortune())
    
    return jsonify({
        "fortunes": fortunes,
        "count": len(fortunes)
    })

@app.route('/fortune/lucky-numbers', methods=['GET'])
def lucky_numbers():
    """Bonus endpoint: Get lucky numbers with a fortune"""
    fortune_data = generate_fortune()
    fortune_data["lucky_numbers"] = random.sample(range(1, 100), 6)
    fortune_data["lucky_color"] = random.choice([
        "Mystical Purple", "Cosmic Blue", "Enchanted Green", 
        "Dragon Red", "Unicorn Pink", "Phoenix Gold"
    ])
    return jsonify(fortune_data)

if __name__ == '__main__':
    # Check if API key is set
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY environment variable is not set!")
        print("Please set it before running the API:")
        print("export GROQ_API_KEY='your-api-key-here'")
    
    print("🔮 Starting Mystical Fortune API...")
    print("✨ The spirits are ready to predict your future!")
    app.run(debug=True, host='0.0.0.0', port=5001)
