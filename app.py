from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend
CORS(app, origins=["http://localhost:5173"])

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Root route
@app.route('/')
def home():
    return "Welcome to the Brainrot Text API!"

@app.route('/convert-text', methods=['POST'])
def convert_text():
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'No text provided'}), 400
        
        prompt = f"You are Brainrot Text convertor. You are given a text, you have to convert it into GenZ slang/ brainrot equivalent text with appropriate emojis, make it funny and unhinged. and remember to to give the text in the same person perspective as the text. IMPORTANT : Dont answer the question for the following text just convert it into brainrot text as mentioned above: {user_input}"
        
        completion = client.chat.completions.create(
            model="google/gemma-3n-e4b-it:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        result = completion.choices[0].message.content
        return jsonify({'converted_text': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
