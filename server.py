from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CSV_FILE = 'survey_results.csv'

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'participant',
                'effect',
                'ai_uncertainty',
                'ai_trust',
                'ai_confidence',
                'ai_visualization_clarity',
                'ai_engagement'
            ])
        print(f"Initialized {CSV_FILE} with header.")

@app.route('/save-survey', methods=['POST'])
def save_survey():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        participant = data.get('participant')
        responses_list = data.get('responses', [])

        if not participant or not responses_list:
            print("Error: Missing participant or responses")
            return jsonify({'message': 'Missing participant ID or responses'}), 400

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            for response in responses_list:
                effect = response.get('effect')
                answers = response.get('responses', {})

                print(f"Saving response for effect {effect}: {answers}")

                writer.writerow([
                    participant,
                    effect,
                    answers.get('ai_uncertainty', ''),
                    answers.get('ai_trust', ''),
                    answers.get('ai_confidence', ''),
                    answers.get('ai_visualization_clarity', ''),
                    answers.get('ai_engagement', '')
                ])

        print(f"Saved {len(responses_list)} responses for participant {participant}")
        return jsonify({'message': 'Survey responses saved successfully'}), 200

    except Exception as e:
        print("Error in save_survey():", e)
        return jsonify({'message': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)
