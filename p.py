import requests
from bs4 import BeautifulSoup

def scrape_proxies():
    urls = [
        "https://www.sslproxies.org/",
        "https://free-proxy-list.net/",
        "https://www.us-proxy.org/",
        "https://www.proxy-list.download/HTTPS"
    ]
    
    proxies = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    ip, port = cols[0].text, cols[1].text
                    proxies.append(f"{ip}:{port}")
        except:
            pass  # Skip failed fetches

    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))
    
    print(f"✅ {len(proxies)} proxies saved to proxies.txt!")

scrape_proxies()
