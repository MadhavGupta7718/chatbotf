from flask import Flask, render_template, request, jsonify
import json
import spacy

app = Flask(__name__)

# Load FAQs from a JSON file
with open('faqs.json') as f:
    faqs = json.load(f)

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    answer = "I'm sorry, I don't have an answer for that."
    found_answer = False  # Flag to track if an answer has been found

    # Check if the user message matches any FAQ
    for faq in faqs:
        # Check for exact question match
        if user_message.lower() in faq['question'].lower():
            answer = faq['answer']
            found_answer = True
            break
        
        # Check for keyword match
        keywords = faq.get('keywords', [])
        for keyword in keywords:
            if keyword.lower() in user_message.lower():
                answer = faq['answer']
                found_answer = True
                break
        
        # If an answer has been found, break out of the outer loop
        if found_answer:
            break

    # If no answer was found, use AI to find the closest match
    if not found_answer:
        user_doc = nlp(user_message)
        max_similarity = 0
        closest_faq = None

        for faq in faqs:
            faq_doc = nlp(faq['question'])
            similarity = user_doc.similarity(faq_doc)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_faq = faq

        if closest_faq and max_similarity > 0.5:  # Threshold for similarity
            answer = closest_faq['answer']

    return jsonify({'answer': answer})  # Return the answer as a JSON response

if __name__ == '__main__':
    app.run(debug=True)
    
