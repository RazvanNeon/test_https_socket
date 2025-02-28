import requests

url = "http://localhost:5000"  # Nu este necesar să specifici portul 443 https://test-https-socket.onrender.com
# Mesajul care trebuie trimis către server
# Mesajul pe care vrei să-l trimiți
message = "Salut, server!"

# Construiți URL-ul cu parametru (query string)
params = {'msg': message}  

try:
    # Trimitem o cerere GET către server
    response = requests.get(url, params=params)        # , params=params

    # Verificăm dacă cererea a fost un succes
    if response.status_code == 200:
        print(f"Răspuns primit de la server: {response.text}")
    else:
        print(f"Eroare: {response.status_code} - {response.reason}")

except requests.exceptions.RequestException as e:
    print(f"A aparut o eroare în timpul conectării: {e}")
