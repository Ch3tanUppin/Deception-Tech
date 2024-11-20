from flask import Flask, Response, render_template, request, jsonify
import threading

from backend.honeypot_manager import HoneypotManager
from backend.response_manager import ResponseManager

app = Flask(__name__)

# Initialize the HoneypotManager and ResponseManager
honeypot_manager = HoneypotManager(
    container_name="cowrie/cowrie",
    container_id="7b7906c708b448afbf85e9941f10f2c1a8956136700396c0e8ee788a052a62c9"
)

# Pass the HoneypotManager instance to ResponseManager
response_manager = ResponseManager(honeypot_manager=honeypot_manager)

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
