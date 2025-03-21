﻿import os
import socket
import threading
import urllib.parse
import time
from flask import Flask, request, jsonify

# Configurare aplicație Flask
app = Flask(__name__)

# Configurare server socket
HOST = '0.0.0.0'
PORT = 12345

memo_msg = '10'
active_clients = []

def start_socket_server():
    global active_clients
    """Serverul socket care ascultă pe un port specific."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Serverul socket este pornit și ascultă pe {HOST}:{PORT}...")
    
    while True:
        client_socket, client_address = server_socket.accept()

        client_key = str(client_address)
        
        active_clients.append(client_address)
        print(f"Conexiune acceptată de la: {client_address}")
        
        # Primirea și procesarea datelor de la client
        data = client_socket.recv(1024).decode('latin1')
        print(f"Mesaj primit: {data}")
        
        # 1. Extragem partea URL dintre "GET" și "HTTP/1.1"
        url = data.split(" ")[1]

        # 2. Parsăm URL-ul pentru a obține parametrii query
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Extragem valoarea parametrului 'msg'
        message = query_params.get("msg", [""])[0]
        print(f"Mesajul extras: {message}")

        # Stocăm memo_msg-ul primit pentru acest client
        # De exemplu, stocăm și timpul ultimei activități
        active_clients[client_key] = {
            "memo_msg": message,
            "last_activity": time.time()
        }
        
        # 3. Extragem valoarea parametrului 'msg'
        message = query_params.get("msg", [""])[0]  # Implicit, un string gol dacă 'msg' nu există
        print(f"Mesajul extras: {message}")

        # Răspuns către client
        response = f"Salut! Mesajul tău a fost primit: {data}"
        client_socket.sendall(response.encode())
        
        client_socket.close()
        active_clients.remove(client_address)

# Pornirea serverului socket într-un fir de execuție separat
socket_thread = threading.Thread(target=start_socket_server, daemon=True)
socket_thread.start()

@app.route('/post', methods=['POST'])
def handle_post():
    # Extrage corpul mesajului POST
    # data = request.json  # Dacă datele sunt trimise ca JSON
    # Sau:
    # data = request.form  # Dacă datele sunt trimise ca form-data
    data = request.get_data(as_text=True)
    # Prelucrează datele extrase
    return f"Informația recepționată: {data}", 200
    
# Endpoint HTTP simplu
@app.route('/')
def home():
    global memo_msg
    message_a = request.args.get('msg', 'Mesajul a lipsește')  # Default dacă "msg" lipsește
    message_b = request.args.get('msgb', 'Mesajul b lipsește')  # Default dacă "msg" lipsește
    if message_a == '250':
        memo_msg = message_b
            
    print(f"Mesaj primit (GET): {message_a}")
    print("Anteturi cerere:", request.headers)
    msg_2 = request.args
    print("Parametri GET:", request.args)  # Parametri trimiși în query string
    print("Metodă HTTP:", request.method)
    return f"Server HTTP și socket este în funcțiune! msg_A={message_a}; msg_A={message_b}; memo = {memo_msg}"

@app.route('/status', methods=['GET'])
def status():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    return jsonify({
        'client_ip': client_ip,
        'active_clients': active_clients
    })

@app.route('/poll_status', methods=['GET'])
def poll_status():
    global memo_msg
    """
    Endpoint pentru long polling.
    Se păstrează conexiunea deschisă până când:
      - se detectează cel puțin un client conectat,
      - sau expiră un timeout (de exemplu, 30 secunde).
    """
    timeout = 30  # secunde
    interval = 1  # intervalul de verificare (1 secunda)
    waited = 0

    message_a = request.args.get('msg', 'Mesajul a lipsește')  # Default dacă "msg" lipsește
    message_b = request.args.get('msgb', 'Mesajul b lipsește')  # Default dacă "msg" lipsește
    if message_a == '250':
        memo_msg = message_b
        
    while waited < timeout:
        if active_clients:  # Dacă există cel puțin un client conectat
            break
        time.sleep(interval)
        waited += interval

    return jsonify({
        'active_clients': active_clients,
        'memo_msg': memo_msg,
        'waited': waited  # cât a așteptat până când a răspuns
    })
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Portul pentru Flask
    app.run(host='0.0.0.0', port=port)
