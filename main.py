import openai
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



import os
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()
        manual_text = data.get("manualText", "").strip()
        tone = data.get("tone", "smart")
        explicit = data.get("explicit", False)

        if not manual_text:
            return jsonify({"error": "No text provided"}), 400

        TONE_TEMPLATES = {
            "savage": "Give a savage and witty comeback to this message: ",
            "polite": "Give a calm and respectful response to defuse this argument: ",
            "smart": "Give an intelligent and logical response to this argument: ",
            "mature": "Give an emotionally mature and understanding reply: "
        }

        base_prompt = TONE_TEMPLATES.get(tone, TONE_TEMPLATES["smart"])
        if explicit and tone == "savage":
            base_prompt = "Give a brutally savage, explicit, and profane clapback to this message. Make it viral-worthy: "
        elif explicit:
            base_prompt += " Feel free to use profanity and sarcasm if needed: "

        prompt = base_prompt + f"\"{manual_text}\""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're trained on the best smart clapbacks from social media. Respond with wit, intelligence, and bite."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=150
        )

        reply = response['choices'][0]['message']['content'].strip()

        return jsonify({
            "extracted_text": manual_text,
            "comeback": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



