Here is the complete, professional `README.md` for **Chaos-Stack**. It is formatted exactly like a top-tier open-source Site Reliability Engineering (SRE) tool, ready to be pushed to your GitHub.

Copy and paste this entire block into your `README.md`:

```markdown
# ⚠️ Chaos-Stack

> A local Chaos Engineering CLI built to intentionally break Docker and emulated AWS infrastructure to validate system resilience.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-SDK-2496ED)
![AWS](https://img.shields.io/badge/AWS-boto3-FF9900)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-FFD000)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 Overview

Standard applications are built for the happy path. **Chaos-Stack** ensures your architecture survives the worst-case scenario. 

Instead of waiting for a random server failure or network drop in production, Chaos-Stack acts as a localized "Chaos Monkey," executing controlled fire drills on your architecture. By combining `boto3`, the Docker SDK, and DuckDB into a single modular CLI, it injects faults into containers, networks, and cloud resources to validate auto-recovery mechanisms and application fallback states.

---

## 🧠 Core Capabilities

* **🐋 The Docker Assassin (`--target docker`)**: Connects to the host Docker daemon and executes randomized container terminations (`SIGKILL`). Proves that orchestrators can seamlessly detect and spin up replacements.
* **🕸️ Network Sabotage (`--target network`)**: Injects artificial latency (up to 1000ms) directly into a running container's network interface using Linux Traffic Control (`tc qdisc`). Proves application timeout handlers and offline-mode caching.
* **☁️ Cloud IAM Lockout (`--target aws`)**: Connects to local AWS mocking servers (like Moto or MinIO) via `boto3` and forcefully injects `DenyAll` IAM policies onto active S3 buckets. Proves the application can survive sudden cloud misconfigurations.
* **📊 Resilience Analytics (`report`)**: Logs all strikes, blast radii, and target layers into a lightning-fast, zero-dependency **DuckDB** database to track system vulnerability over time.
* **🩹 System Healing (`heal`)**: Automatically rolls back injected AWS IAM policies and prepares the environment for the next test cycle.

---

## 📁 Repository Structure

```text
chaos-stack/
├── cli/
│   └── main.py              # Main CLI entrypoint and argument parser
├── attacks/
│   ├── aws_strike.py        # boto3 S3 IAM policy injection logic
│   ├── docker_strike.py     # Docker SDK SIGKILL execution
│   └── network_strike.py    # tc netem latency injection logic
├── analytics/
│   └── logger.py            # DuckDB historical execution tracking
├── .gitignore               # Privacy & clean version control rules
└── README.md                # Project documentation

```

---

## ⚙️ Prerequisites & Installation

**Prerequisites:**

* Python 3.10+
* Docker Daemon running locally (`sudo systemctl start docker`)
* Emulated AWS environment (Moto or MinIO) running locally for cloud testing.

**Installation:**
Clone the repository and run it within an isolated virtual environment:

```bash
git clone [https://github.com/Braveen811/chaos-stack.git](https://github.com/Braveen811/chaos-stack.git)
cd chaos-stack
python -m venv venv
source venv/bin/activate
pip install boto3 docker duckdb rich

```

---

## 🚀 Quick Start Guide

**1. Unleash Chaos:**
Use the `strike` command to target specific infrastructure layers. You can configure the blast radius using the `--severity` flag.

```bash
# Terminate a random running container
python cli/main.py strike --target docker --severity high

# Inject 1000ms latency into a container's network
python cli/main.py strike --target network --severity high

# Lock down emulated S3 buckets with DenyAll policies
python cli/main.py strike --target aws --severity high

```

**2. Analyze the Damage:**
View your historical test data directly from the DuckDB logger.

```bash
python cli/main.py report

```

*Output Example:*

```text
📊 Chaos Resilience Analytics (DuckDB)
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Target Layer    ┃ Severity        ┃       Hits ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ NETWORK         │ HIGH            │          1 │
│ AWS             │ HIGH            │          3 │
│ DOCKER          │ HIGH            │          2 │
└─────────────────┴─────────────────┴────────────┘

```

**3. Heal the Infrastructure:**
Reverse the cloud infrastructure damage and remove injected IAM policies.

```bash
python cli/main.py heal

```

---

## 🛡️ Cloud Emulation Setup

For the AWS strike to function locally without incurring cloud costs, `chaos-stack` points to port `5000` by default. We highly recommend using **Moto** for lightweight, instant AWS mocking:

```bash
# Start the Moto server
docker run -d --name moto -p 5000:5000 motoserver/moto

# Create a test bucket
python -c "import boto3; boto3.client('s3', endpoint_url='http://localhost:5000', aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1').create_bucket(Bucket='test-bucket')"

```

---

## 🗺️ Roadmap & Contributing

**Planned Features:**
- Integration with LocalStack for extended AWS service sabotage (EC2, RDS).
- JSON export for DuckDB analytics to power React-based capstone dashboards.

**Contributing:**
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

**License:**
Distributed under the MIT License.

**Author:** [Braveen R](https://braveenr.linklee.in/)

---

## ✌️ Wrapping Up & Operational Modes

`chaos-stack` bridges the gap between theoretical reliability and actual production readiness, turning disaster recovery testing into an automated, seamless experience across its core execution modes:

- **Strike Mode (`chaos-stack strike`)**: Instant, targeted fault injection for developers simulating container deaths, network latency, and cloud outages.
- **Analytics & Healing Mode (`chaos-stack report` & `chaos-stack heal`)**: Comprehensive tracking of infrastructure resilience via DuckDB, and immediate automated rollback of injected cloud configurations.

See you in the terminal!
