import psutil
import time
import json
import requests
from ping3 import ping
import matplotlib.pyplot as plt


def get_api_metric(endpoint_url, metric, duration):
    try:
        params = {"metric": metric, "duration": duration}
        response = requests.get(endpoint_url, params=params, timeout=5)  # 5-second timeout
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None


def measure_metrics(endpoint_url, duration=10, throughput_threshold=1e6):
    metrics = ["cpu_usage", "memory_usage", "latency", "throughput"]
    results = {metric: [] for metric in metrics}
    results["timestamps"] = []
    results["attack_phases"] = []
    start_time = time.time()
    with open("client_metrics.log", "w") as log_file:
        log_file.write("Timestamp,CPU_Usage(%),Memory_Usage(%),Latency(s),Throughput(Bytes/sec)\n")
        while time.time() - start_time < duration:
            try:
                timestamp = time.time() - start_time
                results["timestamps"].append(timestamp)
                cpu_data = get_api_metric(endpoint_url, "cpu_usage", 1)
                memory_data = get_api_metric(endpoint_url, "memory_usage", 1)
                throughput_data = get_api_metric(endpoint_url, "throughput", 1)
                cpu = cpu_data.get("cpu_usage_avg_percent", 0) if cpu_data else 0
                memory = memory_data.get("memory_used_avg_percent", 0) if memory_data else 0
                target_ip = "8.8.8.8"  
                latency = ping(target_ip)

                latency = latency / 1000 if latency else 0  # Convert ms to seconds
                throughput = throughput_data.get("throughput_sent_avg_bytes_per_sec", 0) if throughput_data else 0
                results["cpu_usage"].append(cpu)
                results["memory_usage"].append(memory)
                results["latency"].append(latency)
                is_attack = throughput > throughput_threshold
                results["attack_phases"].append(is_attack)
                log_file.write(f"{timestamp:.2f},{cpu:.2f},{memory:.2f},{latency:.4f},{throughput:.2f}\n")
                
            except Exception as e:
                print(f"Error during measurement: {e}")
            time.sleep(0.5)
    return results


def visualize_results(results, filename_prefix):
    time_points = results["timestamps"]
    cpu_usage = results["cpu_usage"]
    memory_usage = results["memory_usage"]
    latency = results["latency"]
    throughput = results["throughput"]
    attack_phases = results["attack_phases"]
    plt.figure(figsize=(16, 10))

    plt.plot(
        time_points,
        cpu_usage,
        label="CPU Usage (%)",
        color="red",
        linestyle="--",
        linewidth=2.5
    )
    plt.plot(
        time_points,
        memory_usage,
        label="Memory Usage (%)",
        color="green",
        linestyle="-.",
        linewidth=2.5
    )

    plt.plot(
        time_points,
        latency,
        label="Latency (s)",
        color="blue",
        linestyle="-",
        marker="o",
        markersize=6,
        linewidth=2.5
    )

    for i in range(1, len(attack_phases)):
        if attack_phases[i]:
            plt.axvspan(
                time_points[i - 1],
                time_points[i],
                color="orange",
                alpha=0.3,
                label="Attack Phase" if i == 1 else None
            )

    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(
        time_points,
        throughput,
        label="Throughput (Bytes/sec)",
        color="purple",
        linestyle="-",
        linewidth=3,
        alpha=0.8
    )

    plt.title("Enhanced System Performance Metrics Visualization", fontsize=18, weight="bold")
    plt.xlabel("Time (s)", fontsize=14, weight="bold")
    plt.ylabel("CPU/Memory/Latency", fontsize=14, weight="bold")
    ax2.set_ylabel("Throughput (Bytes/sec)", color="purple", fontsize=14, weight="bold")

    plt.grid(alpha=0.6, linestyle="--", linewidth=0.8)

    ax.legend(loc="upper left", fontsize=12)
    ax2.legend(loc="upper right", fontsize=12)

    plt.tight_layout()
    plt.savefig(f"{filename_prefix}_visualization.png", dpi=300) 
    plt.show()


# Main script
if __name__ == "__main__":
    endpoint_url = input("Enter the API endpoint URL (e.g., http://127.0.0.1:5000/api): ")
    duration = int(input("Enter the monitoring duration (seconds): "))
    throughput_threshold = int(input("Enter throughput threshold for attack detection (Bytes/sec): "))

    print("\nMonitoring system metrics via server API...")
    results = measure_metrics(endpoint_url, duration, throughput_threshold)
    with open("client_metrics.json", "w") as f:
        json.dump(results, f)
    print("Results saved to 'client_metrics.json' and 'client_metrics.log'")

    visualize_results(results, "client_metrics")
    print("Visualization saved as 'client_metrics_visualization.png'")
