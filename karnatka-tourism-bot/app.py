from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="API-KEY")

# Create the model configuration
generation_config = {
    "temperature": 0.7,  # Lower temperature for more focused responses
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    if user_input:
        try:
            # Karnataka tourism-themed prompt
            prompt = (
                "You are a tourism expert chatbot specializing in Karnataka. Provide helpful and accurate information about "
                "Karnataka's tourist destinations, historical sites, natural attractions, culture, cuisine, festivals, and travel tips. "
                "If the user's question is unclear, politely ask for clarification. User query: "
                f"'{user_input}'"
            )
            response = chat_session.send_message(prompt)
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"response": f"Error: {str(e)}"})
    return jsonify({"response": "Please provide a valid input."})

if __name__ == "__main__":
    app.run(debug=True)

