import socket
import time
import subprocess
import matplotlib.pyplot as plt
import requests
import re
import threading
from urllib.parse import urlparse
import psutil  # New library for system resource monitoring
import numpy as np  # For filtering and smoothing data

class MetricsTool:
    def __init__(self, url, endpoint="", port=None, duration=60):
        self.url = url
        self.endpoint = endpoint
        self.port = port
        self.duration = duration
        self.latency_values = []
        self.timestamps = []
        self.throughputs = []
        self.cpu_usages = []  # New list for CPU usage
        self.memory_usages = []  # New list for memory usage
        self.ip_address = self.resolve_url_to_ip()
        if not self.port and self.ip_address:
            self.port = self.find_open_port()

    def resolve_url_to_ip(self):
        """Resolve URL to IP address."""
        try:
            parsed_url = urlparse(self.url)
            hostname = parsed_url.hostname or self.url
            return socket.gethostbyname(hostname)
        except socket.error:
            print(f"Error: Unable to resolve URL '{self.url}'. Please check the domain name.")
            return None

    def find_open_port(self):
        """Find an open port on the target IP."""
        print("No port provided or specified port not reachable. Scanning for an open port...")
        for port in range(1, 65536):
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

    @staticmethod
    def validate_url(url):
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.hostname:
                return True
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
            time.sleep(1)

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

    def measure_resources(self):
        """Measure CPU and memory usage."""
        start_time = time.time()
        while time.time() - start_time < self.duration:
            self.cpu_usages.append(psutil.cpu_percent(interval=1))
            self.memory_usages.append(psutil.virtual_memory().percent)

    def run(self):
        """Run latency, throughput, and resource measurements concurrently."""
        if not self.ip_address:
            print("Invalid URL or IP address.")
            return

        if not self.port:
            print("No suitable port found. Exiting.")
            return

        print(f"Starting metrics for {self.url} (IP: {self.ip_address}) on port {self.port}...")
        print(f"Starting latency, throughput, and resource measurement for {self.duration} seconds...")

        latency_thread = threading.Thread(target=self.measure_latency)
        throughput_thread = threading.Thread(target=self.measure_throughput)
        resource_thread = threading.Thread(target=self.measure_resources)

        latency_thread.start()
        throughput_thread.start()
        resource_thread.start()

        latency_thread.join()
        throughput_thread.join()
        resource_thread.join()

        self.plot_metrics()

    def filter_data(self, data, threshold=2.0):
        """Filter out noisy data points using z-score thresholding."""
        if len(data) == 0:
            return data
        mean = np.mean(data)
        std = np.std(data)
        return [x for x in data if abs(x - mean) / std <= threshold]

    def smooth_data(self, data, window_size=3):
        """Apply a simple moving average for smoothing."""
        if len(data) < window_size:
            return data
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

    def plot_metrics(self):
        """Plot latency, throughput, CPU, and memory usage."""
        # Filter and smooth the data
        latency_values = self.filter_data(self.latency_values)
        throughput_values = self.filter_data(self.throughputs)
        cpu_usages = self.smooth_data(self.cpu_usages)
        memory_usages = self.smooth_data(self.memory_usages)

        fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # 2x2 layout

        # Latency plot
        axs[0, 0].plot(range(len(latency_values)), latency_values, marker="o", label="Latency (ms)", color="blue")
        axs[0, 0].set_title("Latency over Tests")
        axs[0, 0].set_xlabel("Test Number")
        axs[0, 0].set_ylabel("Latency (ms)")
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # Throughput plot
        axs[0, 1].plot(self.timestamps[:len(throughput_values)], throughput_values, marker="o", label="Throughput (Mbps)", color="green")
        axs[0, 1].set_title("Throughput Over Time")
        axs[0, 1].set_xlabel("Time (seconds)")
        axs[0, 1].set_ylabel("Throughput (Mbps)")
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        # CPU usage plot
        axs[1, 0].plot(range(len(cpu_usages)), cpu_usages, marker="o", label="CPU Usage (%)", color="red")
        axs[1, 0].set_title("CPU Usage Over Time")
        axs[1, 0].set_xlabel("Time (seconds)")
        axs[1, 0].set_ylabel("CPU Usage (%)")
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        # Memory usage plot
        axs[1, 1].plot(range(len(memory_usages)), memory_usages, marker="o", label="Memory Usage (%)", color="purple")
        axs[1, 1].set_title("Memory Usage Over Time")
        axs[1, 1].set_xlabel("Time (seconds)")
        axs[1, 1].set_ylabel("Memory Usage (%)")
        axs[1, 1].legend()
        axs[1, 1].grid(True)

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
