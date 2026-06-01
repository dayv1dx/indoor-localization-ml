
from flask import Flask, request
import sqlite3
import time
import argparse
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--x', type=float, required=True, help='Coordenada X da quadra')
parser.add_argument('--y', type=float, required=True, help='Coordenada Y da quadra')
parser.add_argument('--quadra_id', type=int, required=True, help='ID numérico da quadra')
args = parser.parse_args()

# banco de dados
DB_FILE = 'fingerprint_base.db'

# armazenamento temporário
leituras = defaultdict(dict)
coletas_realizadas = 0
LIMITE_AMOSTRAS = 50

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fingerprint (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL,
            y REAL,
            quadra_id INTEGER,
            rssi_ap01 REAL,
            rssi_ap02 REAL,
            rssi_ap03 REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/rssi', methods=['POST'])
def receber_rssi():
    global coletas_realizadas
    if coletas_realizadas >= LIMITE_AMOSTRAS:
        return {'status': 'limite atingido'}

    data = request.get_json()
    scanner = data['scanner_id']
    rssi = float(data['rssi'])

    print(f"Recebido de {scanner}: RSSI = {rssi}")

    leituras['coleta'][scanner] = rssi

    if all(k in leituras['coleta'] for k in ['AP_01', 'AP_02', 'AP_03']):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO fingerprint (x, y, quadra_id, rssi_ap01, rssi_ap02, rssi_ap03, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            args.x,
            args.y,
            args.quadra_id,
            leituras['coleta']['AP_01'],
            leituras['coleta']['AP_02'],
            leituras['coleta']['AP_03'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()

        coletas_realizadas += 1
        print(f"registro salvo ({coletas_realizadas}/{LIMITE_AMOSTRAS})")
        leituras['coleta'].clear()

    return {'status': 'ok'}

if __name__ == '__main__':
    init_db()
    print(f"iniciando servidor para coleta da quadra {args.quadra_id} com limite de {LIMITE_AMOSTRAS} amostras...")
    app.run(host='0.0.0.0', port=5000)
