from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load holes data from JSON file
with open('data/holes.json') as f:
    holes = json.load(f)


@app.route('/')
def index():
    holes_json = json.dumps(holes)
    return render_template('index.html', holes=holes, holes_json=holes_json)


@app.route('/advice', methods=['POST'])
def advice():
    data = request.json
    hole_number = data['hole']
    disc_type = data['disc_type']
    hole = next((h for h in holes if h['hole'] == hole_number), None)

    if not hole:
        return jsonify({"advice": "Hole not found."})

    advice_text = "Consider the following:"

    # Determine advice based on hole details
    if hole['par'] <= 3:
        advice_text += " Use a mid-range disc and focus on accuracy."
    else:
        advice_text += " Use a driver for long distance."

    if "water" in hole['obstacles']:
        advice_text += " Be cautious of water hazards."

    if hole['elevation_change'] > 0:
        advice_text += " The hole has an uphill slope."

    if hole['elevation_change'] < 0:
        advice_text += " The hole has a downhill slope."

    # Determine throw style based on direction
    if hole['direction'] == 'right':
        advice_text += " Consider throwing a flick to curve right."
    elif hole['direction'] == 'left':
        advice_text += " Consider throwing a backhand to curve left."
    else:
        advice_text += " Keep your throw flat to fly as straight as possible."

    # Add specific disc type advice
    if disc_type == "putter":
        advice_text += " Use a putter for short distance and precision."
    elif disc_type == "mid-range":
        advice_text += " Use a mid-range disc for moderate distance and accuracy."
    elif disc_type == "driver":
        advice_text += " Use a driver for maximum distance."

    return jsonify({"advice": advice_text})


if __name__ == '__main__':
    app.run(debug=True)
