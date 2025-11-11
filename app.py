from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
from database import init_db, get_all_events, add_event

app = Flask(__name__, template_folder="templates")
CORS(app)

init_db()

@app.route("/api/events", methods=["GET"])
def get_events():
    city = request.args.get("city")
    return jsonify(get_all_events(city))

@app.route("/api/events", methods=["POST"])
def add_event_api():
    new_event = request.get_json(force=True)
    if not new_event:
        return jsonify({"error": "No data"}), 400
    if "time" not in new_event:
        new_event["time"] = datetime.now().isoformat()
    add_event(new_event)
    return jsonify({"status": "success", "added": new_event}), 201

@app.route("/admin")
def admin_page():
    data = get_all_events()
    return render_template("admin.html", events=data, count=len(data))

@app.route("/")
def index():
    return "<h2>🚨 Server cứu hộ đang chạy!</h2><p>Xem dữ liệu tại <a href='/admin'>/admin</a></p>"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
