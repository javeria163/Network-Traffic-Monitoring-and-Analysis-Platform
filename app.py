from flask import Flask, render_template, jsonify, request
import pandas as pd
import csv
import os
import threading
import time
from scapy.all import sniff, IP, TCP, UDP, ICMP

app = Flask(__name__)

# Monitoring state
monitoring = False
capture_thread = None
capture_stop_event = threading.Event()

DATA_FILE = 'traffic_data.csv'

# Port mapping
PORT_MAP = {
    80: 'HTTP', 443: 'HTTPS', 53: 'DNS',
    22: 'SSH', 21: 'FTP', 25: 'SMTP',
    8080: 'HTTP-Alt', 3306: 'MySQL', 0: 'ICMP'
}

CSV_FIELDS = [
    'time', 'src_ip', 'dst_ip',
    'protocol', 'src_port', 'dst_port',
    'packet_size'
]


# =========================
# INIT CSV FILE
# =========================
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


# =========================
# PACKET HANDLER
# =========================
def packet_callback(pkt):
    if IP not in pkt:
        return

    protocol = (
        'TCP' if TCP in pkt else
        'UDP' if UDP in pkt else
        'ICMP' if ICMP in pkt else
        'Unknown'
    )

    src_port = pkt.sport if hasattr(pkt, 'sport') else 0
    dst_port = pkt.dport if hasattr(pkt, 'dport') else 0

    row = {
        'time': time.strftime('%H:%M:%S'),
        'src_ip': pkt[IP].src,
        'dst_ip': pkt[IP].dst,
        'protocol': protocol,
        'src_port': src_port,
        'dst_port': dst_port,
        'packet_size': len(pkt)
    }

    print("Captured:", row)

    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(row)


# =========================
# SNIFF LOOP
# =========================
def capture_loop():
    sniff(
        prn=packet_callback,
        store=False,
        stop_filter=lambda x: capture_stop_event.is_set()
    )


# =========================
# LOAD CSV DATA
# =========================
def load_data():
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)

    if len(df) == 0:
        return df

    df['service'] = df['dst_port'].map(PORT_MAP).fillna('Unknown')
    return df


# =========================
# ROUTES
# =========================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    global monitoring, capture_thread

    if not monitoring:
        monitoring = True
        capture_stop_event.clear()

        ensure_data_file()

        capture_thread = threading.Thread(
            target=capture_loop,
            daemon=True
        )
        capture_thread.start()

    return jsonify({'status': 'started'})


@app.route('/stop', methods=['POST'])
def stop():
    global monitoring

    monitoring = False
    capture_stop_event.set()

    return jsonify({'status': 'stopped'})


# =========================
# DATA + FILTERING (IMPORTANT)
# =========================
@app.route('/data')
def get_data():
    df = load_data()

    # Filters
    protocol = request.args.get('protocol', '')
    src_ip = request.args.get('src_ip', '')
    dst_ip = request.args.get('dst_ip', '')

    if protocol:
        df = df[df['protocol'] == protocol]

    if src_ip:
        df = df[df['src_ip'].str.contains(src_ip, na=False)]

    if dst_ip:
        df = df[df['dst_ip'].str.contains(dst_ip, na=False)]

    # Stats
    stats = {
        'total_packets': len(df),
        'tcp_count': int((df['protocol'] == 'TCP').sum()),
        'udp_count': int((df['protocol'] == 'UDP').sum()),
        'icmp_count': int((df['protocol'] == 'ICMP').sum()),
        'avg_size': round(df['packet_size'].mean(), 2) if len(df) > 0 else 0
    }

    return jsonify({
        'packets': df.to_dict(orient='records'),
        'stats': stats,
        'monitoring': monitoring
    })


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)