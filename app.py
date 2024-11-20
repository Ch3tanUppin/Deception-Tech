from flask import Flask, Response, render_template, request, jsonify
import threading
from backend.honeypot_manager import HoneypotManager
from backend.response_manager import ResponseManager
from backend.traffic_analyzer import TrafficAnalyzer
from backend.ai_model import MockAIModel

app = Flask(__name__)

# Initialize the HoneypotManager and ResponseManager
honeypot_manager = HoneypotManager(
    container_name="busy_krich",
    container_id="6bfeafa97ecd6d506200c2e53e1fa718dd452137e6c16fa77c12d78416ff0a7b"
)

response_manager = ResponseManager(honeypot_manager=honeypot_manager)

# Initialize Traffic Analyzer
ai_model = MockAIModel()  # You can replace this with your actual AI model
traffic_analyzer = TrafficAnalyzer(ai_model=ai_model, honeypot_manager=honeypot_manager, response_manager=response_manager)

@app.route('/')
def home():
    """
    Render the main page to display logs and manage honeypots.
    """
    return render_template('index.html')

@app.route('/logs')
def stream_logs():
    """
    Stream logs from the honeypot container.
    """
    def generate_logs():
        """
        Generator function to fetch logs in real-time.
        """
        if honeypot_manager.is_container_running():
            for line in honeypot_manager.stream_logs():
                yield f"data: {line.strip()}\n\n"
        else:
            yield "data: Honeypot container is not running.\n\n"

    return Response(generate_logs(), content_type='text/event-stream')

@app.route('/deploy', methods=['POST'])
def deploy_honeypot():
    """
    Endpoint to deploy the honeypot.
    """
    honeypot_manager.deploy_honeypot()
    return jsonify({"message": "Honeypot deployed successfully!"})

@app.route('/remove', methods=['POST'])
def remove_honeypot():
    """
    Endpoint to remove the honeypot.
    """
    honeypot_manager.remove_honeypot()
    return jsonify({"message": "Honeypot removed successfully!"})

@app.route('/capture_traffic', methods=['GET'])
def capture_traffic():
    """
    Endpoint to capture traffic and analyze it.
    """
    # Capture traffic using TrafficAnalyzer
    traffic_analyzer.capture_traffic()
    return jsonify({"message": "Traffic capture started."})

@app.route('/respond', methods=['POST'])
def handle_threat():
    """
    Endpoint to handle a detected threat.
    """
    data = request.json
    threat_type = data.get('threat_type')
    attacker_ip = data.get('attacker_ip')

    if not threat_type or not attacker_ip:
        return jsonify({"error": "Invalid input. Provide 'threat_type' and 'attacker_ip'."}), 400

    response_manager.handle_threat(threat_type, attacker_ip)
    return jsonify({"message": f"Threat of type '{threat_type}' handled for IP {attacker_ip}."})

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
