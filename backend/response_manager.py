import os
import subprocess


class ResponseManager:
    def __init__(self, honeypot_manager):
        """Initialize the ResponseManager with a HoneypotManager."""
        self.honeypot_manager = honeypot_manager

    def handle_threat(self, threat_type, attacker_ip):
        """Take actions based on the type of threat."""
        if threat_type == 'brute_force':
            self.deploy_fake_credentials(attacker_ip)
        elif threat_type == 'DDoS':
            self.redirect_ddos_traffic(attacker_ip)
        elif threat_type == 'honeypot':
            self.honeypot_manager.deploy_honeypot()

    def deploy_fake_credentials(self, attacker_ip):
        """Deploy fake SSH credentials to the attacker."""
        print(f"Deploying fake credentials for IP: {attacker_ip}")
        fake_ssh_dir = "/tmp/fake_ssh_credentials"
        os.makedirs(fake_ssh_dir, exist_ok=True)

        # Paths for fake keys
        private_key = os.path.join(fake_ssh_dir, "id_rsa")
        public_key = os.path.join(fake_ssh_dir, "id_rsa.pub")

        # Fake key contents
        private_key_content = """<your_private_key_content>"""
        public_key_content = "<your_public_key_content>"

        with open(private_key, "w") as private_file:
            private_file.write(private_key_content)
        with open(public_key, "w") as public_file:
            public_file.write(public_key_content)

        subprocess.run(f"chmod 600 {private_key}", shell=True)
        print(f"Fake SSH credentials deployed for IP: {attacker_ip}")

    def redirect_ddos_traffic(self, attacker_ip):
        """Redirect DDoS traffic to decoy system."""
        print(f"Redirecting DDoS attack to decoy for IP: {attacker_ip}")
        subprocess.run(f"iptables -A INPUT -s {attacker_ip} -j REJECT", shell=True)