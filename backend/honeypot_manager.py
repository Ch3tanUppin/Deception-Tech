import subprocess
import time

class HoneypotManager:
    def __init__(self, container_name='cowrie/cowrie', container_id=None):
        self.container_name = container_name
        self.container_id = container_id

    def is_container_running(self):
        """Check if the honeypot container is running."""
        print(f"Checking if container {self.container_id} is running...")
        try:
            # Check if the container ID is running
            result = subprocess.run(
                ['docker', 'ps', '-q', '-f', f'id={self.container_id}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            is_running = bool(result.stdout.strip())
            print(f"Container {self.container_id} running: {is_running}")
            return is_running
        except subprocess.CalledProcessError as e:
            print(f"Error checking container status: {e.stderr}")
            return False
        
    def stream_logs(self):
        """Stream logs from the Docker container."""
        try:
            # Use Docker CLI to stream logs from the container
            process = subprocess.Popen(
                ['docker', 'logs', '-f', self.container_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Ensures logs are returned as strings, not bytes
            )
            for line in process.stdout:
                yield line.strip()  # Stream logs line-by-line
        except Exception as e:
            print(f"Error streaming logs: {e}")
            yield f"Error streaming logs: {e}"

    def deploy_honeypot(self):
        """Deploy the honeypot container dynamically."""
        if self.is_container_running():
            print(f"The container {self.container_id} is already running.")
            return
        
        print(f"Deploying honeypot with image '{self.image_name}'...")
        try:
            # Deploy the honeypot container
            result = subprocess.run(
                ['docker', 'run', '-d', '--name', self.container_id, self.image_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            deployed_container_id = result.stdout.strip()
            if deployed_container_id == self.container_id:
                print(f"Container {self.container_id} deployed successfully.")
            else:
                print(f"Deployed container ID mismatch. Expected: {self.container_id}, Got: {deployed_container_id}")
        except subprocess.CalledProcessError as e:
            print(f"Error deploying honeypot container: {e.stderr}")

    def remove_honeypot(self):
        """Stop and remove the honeypot container."""
        if not self.is_container_running():
            print(f"The container {self.container_id} is not running.")
            return
        
        print(f"Removing honeypot container {self.container_id}...")
        try:
            # Stop and remove the container
            subprocess.run(['docker', 'stop', self.container_id], check=True)
            subprocess.run(['docker', 'rm', self.container_id], check=True)
            print(f"Container {self.container_id} removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error removing container: {e.stderr}")

# Example usage
if __name__ == "__main__":
    # Initialize the honeypot manager with the specific image and container ID
    honeypot_manager = HoneypotManager()

    # Deploy the honeypot
    honeypot_manager.deploy_honeypot()

    # Simulate some time before removal
    time.sleep(20)

    # Check if the container is running
    honeypot_manager.is_container_running()

    # Remove the honeypot
    honeypot_manager.remove_honeypot()
