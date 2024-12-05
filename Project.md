# Project Directory Structure

```zsh
FlowGuard - Securing Every Packet in Your Network (Developed By Cyber Commandos)
│
├── Docs/                               # Project documentation
│   ├── setup_guide.md                  # Setup instructions
│   ├── user_manual.md                  # Guide to execute benchmark tests
│   └── troubleshooting.md              # Troubleshooting common issues
│
├── src/                                # Source code for tools and utilities
│   ├── Traffic_generator/              # DDOS Attack scripts
│   │   ├── goldeneye.py                # GoldenEye DDoS tool integration
│   │   ├── loic.py                     # LOIC tool integration
│   │   ├── xoic.py                     # XOIC tool integration
│   │   └── config.yaml                 # Traffic generation configuration
│   │
│   ├── Benchmarking_tool/              # Benchmarking and monitoring scripts
│   │   ├── benchmark.py                # Main script for benchmarking
│   │   ├── performance_metrics.py      # Functions to collect metrics
│   │   └── config.yaml                 # Benchmark configuration
│   │
│   ├── Server/                         # Server Setup
│   │   ├── Incognito-Vault             # Website Which will be running in server 
│   │
│   └── Utilities/                      # Helper scripts and functions
│       ├── network_utils.py            # Network configuration utilities
│       ├── log_parser.py               # IDS/IPS log parser
│       └── data_visualization.py       # Visualization utilities
│
├── Data/                               # Generated data and logs
│   ├── logs/                           # System A logs
│   │   └── system_a_logs.txt           # Example log file
│   ├── metrics/                        # Collected performance metrics
│   │   └── throughput_results.csv      # Throughput metrics (example)
│   └── attack_data/                    # Attack traffic profiles
│       └── attack_traffic.json         # Example profile
│
├── Results/                            # Benchmarking results and analysis
│   ├── visualizations/                 # Performance graphs
│   │   └── throughput_vs_latency.png   # Example visualization
│   ├── reports/                        # Detailed performance reports
│   │   └── benchmark_report_1.pdf      # Example report
│   └── raw_data/                       # Raw performance data
│       └── raw_throughput_data.csv     # Example raw data
│
├── Tests/                              # Unit tests for components
│   ├── test_traffic_generator.py       # Traffic generator tests
│   ├── test_benchmarking_tool.py       # Benchmarking tool tests
│   └── test_server_monitor.py          # Monitoring tool tests
│
├── .gitignore                          # Git exclusion rules
├── README.md                           # Project overview and usage guide
└── LICENSE                             # License for the project
```
[Go Back](README.md)