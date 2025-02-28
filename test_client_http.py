import socket

# Configurare client
HOST = 'localhost'  # Adresa serverului (în acest caz, local)
PORT = 12345        # Portul serverului

# Crearea unui socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarea la server
client_socket.connect((HOST, PORT))

# Trimiterea unui mesaj către server
message = "Salutare, server!"
client_socket.sendall(message.encode())

# Primirea răspunsului de la server
response = client_socket.recv(1024).decode()
print(f"Răspuns de la server: {response}")

# Închiderea conexiunii
client_socket.close()