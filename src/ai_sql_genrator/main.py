#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from flask import Flask, request, jsonify
from ai_sql_genrator.crew import AiSqlGenrator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Initialize Flask app
app = Flask(__name__)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the Flask server so it works with crewai run.
    """
    app.run(host='0.0.0.0', port=5001)


# Flask route to handle POST requests
@app.route('/run', methods=['POST'])
def run_api():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Missing "question" in request body'}), 400

    try:
        AiSqlGenrator().crew().kickoff(inputs={'question': data['question']})
        # Read and return the content from final_answer.md
        with open("final_answer.md", "r", encoding="utf-8") as f:
            answer = f.read()
        return jsonify({'status': 'success', 'answer': answer}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
