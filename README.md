# FlowGuard - Securing Every Packet in Your Network
### Developed By Cyber Catalyst 💀

## Index

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [How It Works](#how-it-works)
4. [Project Structure](#project-structure)
5. [How to Run](#how-to-run)
   1. [Prerequisites](#prerequisites)
   2. [Setup and Run the Benchmarking Tool](#setup-and-run-the-benchmarking-tool)
6. [How It Helps the Community](#how-it-helps-the-community)
7. [Scalability](#scalability)
8. [Conclusion](#conclusion)
9. [License](#license)

## Overview

**FlowGuard** is an innovative **IDS/IPS Performance Benchmarking solution** designed to evaluate the performance of **Intrusion Detection Systems (IDS)** and **Intrusion Prevention Systems (IPS)** under various traffic conditions, including both **Regular traffic**, **Attack traffic** & **Mixed Traffic**. The tool benchmarks key performance metrics such as **Throughput**, **Latency**, and **Packet Drops** by the IDS/IPS in the server, and visualizes the system’s performance degradation as traffic load increases.

This benchmarking tool simulates **real-world attack scenarios** using industry-standard traffic-generation tools such as **GoldenEye**, **LOIC**, and **XOIC**. It connects to a server running **Incognito Vault** and evaluates the server's performance, providing insights on how well the IDS/IPS handles **DDoS attacks** and heavy network loads. The system is designed to be **scalable** and can be customized to suit different network profiles, attack types, and traffic conditions.

## Key Features

- **Traffic Simulation**: Simulates attack traffic using **GoldenEye**, **LOIC**, and **XOIC**, tools commonly used for DDoS attacks by hackers.
- **Performance Metrics**: Monitors **throughput**, **latency**, and **packet drops** during attack simulations.
- **Real-time Monitoring**: Collects system performance metrics and visualizes degradation as traffic increases.
- **API Integration**: **Incognito Vault** exposes an API to allow seamless connection by the benchmarking tool for performance evaluation.
- **Log Parsing**: Aggregates and parses logs from the server, attack tools, and system metrics for deeper analysis.

## How It Works

**FlowGuard** operates across multiple systems:

1. **System A (Server)**:
   - Runs the **Incognito Vault** application on port 8800, hosting the target website.
   - Exposes an API to monitor server performance (throughput, latency, packet drops, CPU Usage, Memory, etc, etc) via the benchmarking tool.
   - Hosts the IDS/IPS that is being tested.

2. **System B (Monitoring System)**:
   - Runs the **Benchmarking Tool** which connects to **System A** and collects data on the server's performance.
   - Collects real-time metrics like **throughput**, **latency**, and **packet drops**.

3. **System C (Attacker's Machine)**:
   - Runs tools like **GoldenEye**, **LOIC**, or **XOIC** to generate DDoS attack targeting **System A**.
   - Simulates **DDoS** attacks to test how well the IDS/IPS on **System A** responds to high traffic loads and attack conditions.

</center><img src="System Diagram/FlowGuard1.png"></center>
<center><figcaption>Figure 1: Use Case Diagram of FlowGuard System Demonstrate how it's working</figcaption></center>
<br>

The benchmarking tool performs the following steps:
- Connects to **System A** (Incognito Vault) via its exposed API.
- Monitors the server’s performance metrics (throughput, latency, packet drops).
- Simulates different traffic profiles, including regular and attack traffic.
- Logs and visualizes the data to show how the IDS/IPS is performing as traffic increases.
- Provides detailed insights and metrics to help improve the IDS/IPS configuration and performance.

## Project Structure

Want to see the project structure? Then [Click Me](Project.md)

## How to Run

### Prerequisites

- **Triple Systems must have Python 3.10+**
- **System A or Server must be running Incognito Vault** if not download & configure it.
- **System B or Monitoring System** should have Benchmarking tool.
- **Traffic Generation Tools**: System C or Atacker must have **GoldenEye** or **LOIC** or **XOIC**.

### Setup and Run the Benchmarking Tool

1. **Download & Start the Incognito-Vault (on System A)**:
   - git clone `https://github.com/official-biswadeb941/IncognitoVault`
   - cd `Incognito-Vault`
   - `python -m venv .venv`
   - source `.venv/bin/activate`
   - `pip install -r requirements.txt`
   - `uwsgi --ini uwsgi.ini`.

2. **Start the Benchmarking Tool (on System B)**:
   - Navigate to the `benchmarking_tool/` folder and run `python benchmark.py`.

3. **Simulate DDoS Attack  (on System C)**:
   - Run **GoldenEye**, **LOIC**, or **XOIC** to generate attack traffic against **System A** (Incognito Vault server).

4. **View Results**:
   - Once the benchmark completes, the **visualization tool** will display performance degradation as traffic increases, and logs will be saved in the `logs/` directory.

## How It Helps the Community

**FlowGuard** addresses the need for **real-world performance testing** for **IDS/IPS devices**. It helps security professionals:
- **Evaluate system resilience**: Understand how IDS/IPS devices perform under heavy load and sophisticated attacks.
- **Optimize IDS/IPS configurations**: Identify weaknesses in IDS/IPS configurations and fine-tune them for better protection.
- **Simulate attack scenarios**: Test how well IDS/IPS can handle different types of **DDoS** or **network floods**.
- **Data-driven insights**: Gain performance data that helps in optimizing network security devices.

This project is particularly valuable for organizations looking to ensure their security infrastructure is **robust and responsive** to evolving threats.

## Scalability

The system is designed to be **scalable** for future needs:
- **Multiple Server Support**: The tool can be extended to test **multiple IDS/IPS devices** in parallel by adjusting the benchmarking system to connect to multiple servers.
- **Customizable Attack Profiles**: New types of attack simulations can be added easily by integrating additional traffic generation tools or creating custom attack profiles.
- **Advanced Visualizations**: The system can be enhanced with more sophisticated **real-time dashboards** and integration with platforms like **Grafana** for better performance tracking.
- **Cloud Integration**: The benchmarking tool could be integrated with cloud-based platforms for large-scale simulations and tests.

## Conclusion

**FlowGuard** - Securing Every Packet in Your Network, is a **comprehensive** and **scalable** solution for evaluating the performance of IDS/IPS devices under **realistic network conditions**. It is a powerful tool for security professionals and organizations seeking to understand and improve the effectiveness of their intrusion detection and prevention systems.

By benchmarking IDS/IPS devices, simulating realistic attacks, and visualizing performance data, **FlowGuard** helps ensure that security systems are optimized to defend against today's evolving threats.

---

## License

This project is licensed under the FAUL License - see the [LICENSE](License.md) file for details.
