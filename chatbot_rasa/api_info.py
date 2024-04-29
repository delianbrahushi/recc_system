from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Sample list of events
events = [
    {
        "name": "Engineering Innovation Symposium",
        "date": "2023-12-15",
        "time": "3:00 PM",
        "location": "Auditorium",
        "topic": "Advancements in Sustainable Energy Technologies",
        "speakers": ["Expert 1", "Expert 2"]
    },
    {
        "name": "International Cultural Exchange",
        "date": "2023-12-30",
        "time": "6:00 PM",
        "location": "Student Lounge",
        "focus": "Cultural Sharing and Discussions",
        "activities": ["Music", "Food"]
    }
]

@app.route('/api/events', methods=['GET'])
def get_random_event():
    # Get a random event from the list
    random_event = random.choice(events)
    return jsonify({'event': random_event})

@app.route('/api/documents', methods=['GET'])
def get_documents():
    documents = [
        "Acceptance letter",
        "Proof of financial means",
        "Valid passport",
        "Proof of enrollment"
    ]
    return jsonify({'documents': documents})

if __name__ == '__main__':
    app.run(debug=True)
