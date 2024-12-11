import socket
import time
import subprocess
import matplotlib.pyplot as plt
import requests
import re
import threading
from urllib.parse import urlparse

class MetricsTool:
    def __init__(self, url, endpoint="", port=None, duration=60):
        self.url = url
        self.endpoint = endpoint
        self.port = port
        self.duration = duration
        self.latency_values = []
        self.timestamps = []
        self.throughputs = []
        self.ip_address = self.resolve_url_to_ip()
        if not self.port and self.ip_address:
            self.port = self.find_open_port()

    def resolve_url_to_ip(self):
        """Resolve URL to IP address."""
        try:
            # Parse the URL and extract the hostname
            parsed_url = urlparse(self.url)
            hostname = parsed_url.hostname or self.url  # If parsing fails, fallback to raw input
            # Resolve hostname to IP
            return socket.gethostbyname(hostname)
        except socket.error:
            print(f"Error: Unable to resolve URL '{self.url}'. Please check the domain name.")
            return None

    def find_open_port(self):
        """Find an open port on the target IP."""
        print("No port provided or specified port not reachable. Scanning for an open port...")
        for port in range(1, 65536):  # Scan all possible ports
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.1)
                    if s.connect_ex((self.ip_address, port)) == 0:
                        print(f"Found open port: {port}")
                        return port
            except Exception:
                continue
        print("No open ports found.")
        return None
    
    def validate_url(url):
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.hostname:
                return True
            # Check if it is a bare domain name or IP
            if socket.gethostbyname(url):
                return True
        except Exception:
            pass
        print(f"Invalid URL format: '{url}'. Please enter a valid URL or IP address.")
        return False


    def normalize_url(self):
        """Normalize the URL with the endpoint."""
        base_url = re.sub(r'^(http://|https://|www\.)', '', self.url)
        return f"http://{base_url}/{self.endpoint.lstrip('/')}" if self.endpoint else f"http://{base_url}"

    def measure_latency(self):
        """Measure latency using ICMP ping."""
        start_time = time.time()
        while time.time() - start_time < self.duration:
            try:
                process = subprocess.run(
                    ["ping", "-c", "1", self.ip_address],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )
                if process.returncode == 0:
                    output = process.stdout
                    for line in output.split("\n"):
                        if "time=" in line:
                            latency = float(line.split("time=")[1].split(" ms")[0])
                            self.latency_values.append(latency)
                else:
                    self.latency_values.append(0)
            except Exception as e:
                print(f"Error measuring latency: {e}")
                self.latency_values.append(0)
            time.sleep(1)  # Measure latency every second

    def measure_throughput(self):
        """Measure throughput by downloading data from the target URL."""
        normalized_url = self.normalize_url()
        start_time = time.time()
        while time.time() - start_time < self.duration:
            try:
                download_start = time.time()
                response = requests.get(normalized_url, stream=True)
                total_bytes = 0
                for chunk in response.iter_content(chunk_size=8192):
                    total_bytes += len(chunk)
                    if time.time() - start_time >= self.duration:
                        break
                download_end = time.time()
                elapsed_time = download_end - download_start
                throughput = (total_bytes * 8) / (elapsed_time * 1e6)  # Mbps
                self.timestamps.append(time.time() - start_time)
                self.throughputs.append(throughput)
            except Exception as e:
                print(f"Error during throughput measurement: {e}")

    def run(self):
        """Run latency and throughput measurements concurrently."""
        if not self.ip_address:
            print("Invalid URL or IP address.")
            return

        if not self.port:
            print("No suitable port found. Exiting.")
            return

        print(f"Starting metrics for {self.url} (IP: {self.ip_address}) on port {self.port}...")
        print(f"Starting latency and throughput measurement for {self.duration} seconds...")

        latency_thread = threading.Thread(target=self.measure_latency)
        throughput_thread = threading.Thread(target=self.measure_throughput)

        latency_thread.start()
        throughput_thread.start()

        latency_thread.join()
        throughput_thread.join()

        self.plot_metrics()

    def plot_metrics(self):
        """Plot latency and throughput results side by side."""
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))  # Side-by-side layout

        # Latency plot
        axs[0].plot(range(len(self.latency_values)), self.latency_values, marker="o", label="Latency (ms)", color="blue")
        axs[0].set_title("Latency over Tests")
        axs[0].set_xlabel("Test Number")
        axs[0].set_ylabel("Latency (ms)")
        axs[0].legend()
        axs[0].grid(True)

        # Throughput plot
        axs[1].plot(self.timestamps, self.throughputs, marker="o", label="Throughput (Mbps)", color="green")
        axs[1].set_title("Throughput Over Time")
        axs[1].set_xlabel("Time (seconds)")
        axs[1].set_ylabel("Throughput (Mbps)")
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()


def convert_duration(duration_str):
    """Convert duration string to seconds."""
    if duration_str.lower().endswith('m'):
        return int(duration_str[:-1]) * 60
    elif duration_str.lower().endswith('s'):
        return int(duration_str[:-1])
    else:
        return int(duration_str)


if __name__ == "__main__":
    while True:
        url = input("Enter the base URL or IP to test (e.g., google.com, https://google.com, 192.168.1.2): ").strip()
        if MetricsTool.validate_url(url):
            break
    endpoint = input("Enter the URL endpoint (optional, e.g., api/v1/resource): ").strip()
    port_input = input("Enter the target port (optional): ").strip()
    port = int(port_input) if port_input.isdigit() else None
    duration_str = input("Enter the duration of the test (e.g., 60s or 2m): ").strip()
    duration = convert_duration(duration_str)

    metrics_tool = MetricsTool(url, endpoint, port, duration)
    metrics_tool.run()

