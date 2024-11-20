import pyshark
import asyncio
import threading

class TrafficAnalyzer:
    def __init__(self, ai_model, honeypot_manager, response_manager, interface='eth0'):
        self.ai_model = ai_model
        self.honeypot_manager = honeypot_manager
        self.response_manager = response_manager
        self.interface = interface  # Network interface to capture packets from, e.g., 'eth0'

    def capture_traffic(self):
        """
        Capture traffic using a separate thread.
        """
        loop = asyncio.new_event_loop()  # Create a new event loop for this thread
        asyncio.set_event_loop(loop)  # Set this loop as the current event loop

        capture_thread = threading.Thread(target=self._start_capture, args=(loop,))
        capture_thread.start()
        capture_thread.join()  # Wait for the capture thread to complete

    def _start_capture(self, loop):
        """
        Start packet capture in the background.
        """
        cap = pyshark.LiveCapture(interface=self.interface)
        cap.sniff(timeout=10)  # Capture packets for 10 seconds (adjust as needed)
        
        # After capturing, process the packets
        for packet in cap:
            traffic_data = str(packet)  # Convert packet to string for analysis
            print(f"Captured traffic: {traffic_data}")  # Log the captured traffic for debugging
            
            # Analyze the traffic
            self.analyze_traffic(traffic_data)  # Analyze the captured traffic

    def analyze_traffic(self, traffic_data):
        """Analyze traffic data to detect threats using AI model."""
        print(f"Analyzing traffic: {traffic_data}")  # Debug the traffic data

        # Assuming the AI model can predict based on traffic data
        threat_type = self.ai_model.predict(traffic_data)  # Get threat type from AI model
        
        # Debugging: Print out the result of the AI model's prediction
        print(f"AI model predicted threat type: {threat_type}")
        
        if threat_type == 'malicious':
            # If threat is malicious, extract IP and handle it
            attacker_ip = self.extract_ip(traffic_data)
            print(f"Malicious traffic detected from IP: {attacker_ip}")
            self.handle_threat(threat_type, attacker_ip)
            return 'malicious', attacker_ip
        else:
            print("Traffic is benign.")
            return 'benign', None

    def extract_ip(self, traffic_data):
        """Extract the source IP address from captured traffic data."""
        try:
            # Sample logic to extract IP from packet data
            ip = traffic_data.split(" ")[1].split("=")[1]
            return ip
        except IndexError:
            return None

    def handle_threat(self, threat_type, attacker_ip):
        """Take appropriate actions based on the detected threat."""
        if threat_type == 'malicious':
            if 'SSH' in attacker_ip:
                self.honeypot_manager.deploy_honeypots()  # Deploy honeypot if SSH attack detected
                self.response_manager.deploy_fake_credentials(attacker_ip)  # Deploy fake credentials to attacker
            self.response_manager.redirect_ddos_traffic(attacker_ip)
