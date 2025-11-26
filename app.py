from flask import Flask, request, jsonify
from email_agent import review_email
from flask_cors import CORS
import sys
import io

app = Flask(__name__)
CORS(app)

@app.route('/api/review', methods=['POST'])
def api_review():
    data = request.get_json()
    email = data.get('email', '')
    mode = data.get('mode', 'huggingface')
    # Capture stdout to get the suggestion printed by review_email
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        review_email(email, mode)
        output = mystdout.getvalue()
    finally:
        sys.stdout = old_stdout
    # Extract only the suggestion from output
    suggestion = ''
    for line in output.split('\n'):
        if line.strip().startswith('Suggestion:'):
            suggestion = line.split('Suggestion:',1)[-1].strip()
            break
    if not suggestion:
        # fallback: try to find the last non-empty line
        lines = [l.strip() for l in output.split('\n') if l.strip()]
        if lines:
            suggestion = lines[-1]
    return jsonify({'suggestion': output.split('Suggestion:   ')[-1]})
    #return jsonify({'suggestion': output.split('Suggestion:')[-1])

if __name__ == '__main__':
    app.run(debug=True, port=5050)
