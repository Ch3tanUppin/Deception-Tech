class MockAIModel:
    def predict(self, traffic_data):
        """A mock prediction function."""
        # Check for common malicious indicators in the traffic data
        if "SSH" in traffic_data:
            return 'malicious'  # Simulating a malicious traffic detection for SSH
        elif "DDoS" in traffic_data:
            return 'malicious'  # Simulating a DDoS attack detection
        elif "404 Not Found" in traffic_data:
            return 'malicious'  # Simulate detecting a web scanning attempt
        elif "192.168.1.1" in traffic_data:  # Example: suspicious IP
            return 'malicious'  # Detect traffic from a known bad IP
        else:
            return 'benign'  # Default to benign if no malicious pattern is found
