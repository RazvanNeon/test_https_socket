import socket

# Configurare server
HOST = '0.0.0.0'  # Ascultă pe toate interfețele de rețea
PORT = 52345      # Portul pe care rulează serverul

# Crearea unui socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Ascultă o conexiune

print(f"Serverul este pornit și ascultă pe portul {PORT}...")

while True:
    # Acceptarea conexiunii de la un client
    client_socket, client_address = server_socket.accept()
    print(f"Conexiune acceptată de la: {client_address}")

    # Primirea datelor de la client
    data = client_socket.recv(1024).decode()
    print(f"Mesaj primit: {data}")

    # Procesarea și trimiterea unui răspuns înapoi
    response = f"Serverul a primit: {data}"
    client_socket.sendall(response.encode())

    # Închiderea conexiunii cu clientul
    client_socket.close()