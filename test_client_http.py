import socket

# Introduce URL-ul serverului (de exemplu, www.example.com)
# url = input("Introduceți URL-ul (de exemplu, www.example.com): ")
url = "https://test-https-socket.onrender.com"
port = 5000  # Portul standard pentru HTTP

try:
    # Crearea unui socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Rezolvarea adresei serverului și conectarea la acesta
    print(f"Conectare la {url}:{port}...")
    client_socket.connect((url, port))

    # Crearea cererii HTTP
    request = f"GET / HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n"
    client_socket.sendall(request.encode())

    # Primirea răspunsului de la server
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # Afișarea răspunsului complet (header + body)
    print("Răspuns primit de la server:\n")
    print(response.decode())

except Exception as e:
    print(f"A apărut o eroare: {e}")
finally:
    # Închiderea conexiunii
    client_socket.close()