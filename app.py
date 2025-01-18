from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load FAQs from a JSON file
with open('faqs.json') as f:
    faqs = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    answer = "I'm sorry, I don't have an answer for that."

    # Check if the user message matches any FAQ
    for faq in faqs:
        if user_message.lower() in faq['question'].lower():
            answer = faq['answer']
            break

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)