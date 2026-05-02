# 🌐 Network Traffic Monitoring & Analysis Platform

> A lightweight, browser-based, Wireshark-style real-time packet analyzer built with Python and Flask.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![Scapy](https://img.shields.io/badge/Scapy-2.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

This project captures live network packets directly from the host machine's active interface, classifies them by protocol (TCP / UDP / ICMP), persists them to a CSV log, and presents a real-time filterable dashboard — all accessible from any web browser without client-side installation.

Built as a Computer Networks course project (BCSF24A041 — Javeria Javaid).

---

## ✨ Features

- 🔴 **Live packet capture** using Scapy — start and stop from the browser
- 📊 **Real-time statistics** — total packets, TCP/UDP/ICMP counts, average packet size
- 🔍 **Protocol & IP filtering** — filter by TCP/UDP/ICMP and source/destination IP
- 🗂️ **Persistent CSV logging** — `traffic_data.csv` survives across sessions
- 🏷️ **Service name mapping** — port numbers auto-resolved to HTTP, HTTPS, DNS, SSH, FTP, SMTP, MySQL
- 🌑 **Dark-themed dashboard** — colour-coded protocol rows, auto-refreshes every 2 seconds
- 🔁 **Non-blocking capture** — background thread keeps the web server responsive

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Flask (Python) | HTTP server & REST API |
| Packet Capture | Scapy | Low-level packet sniffing |
| Data Processing | Pandas | CSV loading, filtering, statistics |
| Data Storage | CSV File | Persistent packet log |
| Frontend | HTML5 / CSS3 / JavaScript | Dashboard & live display |
| Concurrency | Python `threading` | Non-blocking background capture |

---

## 📁 Project Structure

```
network-traffic-analyzer/
│
├── app.py                 # Flask backend — capture engine, REST API, data processing
├── traffic_data.csv       # Auto-generated packet log (created on first run)
│
└── templates/
    └── index.html         # Frontend dashboard (dark theme, live stats, filter UI)
```

---

## 📋 Dataset Description

The tool generates `traffic_data.csv` automatically during capture. Each row represents one captured IP packet.

| Field | Type | Example | Description |
|---|---|---|---|
| `time` | String (HH:MM:SS) | `14:32:07` | Wall-clock timestamp at capture |
| `src_ip` | String (IPv4) | `192.168.0.108` | Source IP address |
| `dst_ip` | String (IPv4) | `13.89.178.27` | Destination IP address |
| `protocol` | Categorical | `TCP` | TCP, UDP, ICMP, or Unknown |
| `src_port` | Integer | `52314` | Source port (0 for ICMP) |
| `dst_port` | Integer | `443` | Destination port; used for service mapping |
| `packet_size` | Integer (bytes) | `1420` | Total length of the captured packet |

> A derived `service` column is appended at query time by mapping `dst_port` → service name (e.g. 443 → HTTPS).

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- Administrator / root privileges (required for raw packet capture)
- Npcap (Windows) or libpcap (Linux/macOS)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/network-traffic-analyzer.git
cd network-traffic-analyzer
```

### 2. Install dependencies

```bash
pip install flask scapy pandas
```

> On Windows, also install [Npcap](https://npcap.com/) with "WinPcap API compatibility" enabled.

### 3. Run the application

**Linux / macOS** (requires sudo for raw socket access):

```bash
sudo python app.py
```

**Windows** (run as Administrator):

```bash
python app.py
```

### 4. Open the dashboard

Navigate to `http://127.0.0.1:5000` in your browser.

---

## 🚀 Usage

1. Open the dashboard at `http://127.0.0.1:5000`
2. Click **Start** — packet capture begins immediately in the background
3. The table auto-refreshes every **2 seconds** with the latest captured packets
4. Use the **Protocol**, **Source IP**, and **Destination IP** filters and click **Apply**
5. Click **Stop** to end the capture session
6. The `traffic_data.csv` file retains all captured data for offline analysis

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the dashboard UI |
| `POST` | `/start` | Starts the packet capture thread |
| `POST` | `/stop` | Stops the packet capture thread |
| `GET` | `/data` | Returns packets + stats (supports `?protocol=`, `?src_ip=`, `?dst_ip=` filters) |

**Example filter request:**
```
GET /data?protocol=TCP&src_ip=192.168.0
```

---

## 📊 Sample Results

From a real capture session (2,285 packets):

| Metric | Value |
|---|---|
| Total Packets | 2,285 |
| TCP | 1,357 (59.4%) |
| UDP | 920 (40.3%) |
| ICMP | 8 (0.3%) |
| Average Packet Size | 842.69 bytes |
| Most Active Remote Host | 13.89.178.27 (Microsoft Azure CDN) |
| Dominant Service | HTTPS (Port 443) — 1,025 packets |

---

## 🔭 Scope & Limitations

**In scope:** Single-host monitoring, TCP/UDP/ICMP capture, CSV logging, web dashboard, port-to-service mapping.

**Out of scope:** Deep packet inspection, multi-host monitoring, anomaly alerting, user authentication, GeoIP resolution.

---

## 🔮 Future Enhancements

- GeoIP resolution to map IP addresses to countries/cities on a live map
- Anomaly detection and threshold-based alerting
- Protocol deep inspection (HTTP method, DNS query name, etc.)
- Multi-session analytics and historical trend charts
- Export captured data to PCAP format for Wireshark compatibility

---

## 👩‍💻 Author

**Javeria Javaid**  
Roll No: BCSF24A041 | CS Self-Support  
Computer Networks — April 2026

---

## 📄 License

This project is for educational purposes. Feel free to fork and extend.
