import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self) -> None:
        pass

    def __update(self):
        header = {
            "user-agent" : UserAgent().random
        }

        self.proxies = []

        link = "https://free-proxy-list.net/"
        response = requests.get(link, headers=header).text
        soup = BeautifulSoup(response, "lxml")

        tbody = soup.find("tbody")
        items = tbody.find_all("tr")
        
        for item in items:

            item_info = item.find_all("td")

            item_ip = item_info[0].text.strip()
            item_port = item_info[1].text.strip()
            item_anonimity = item_info[4].text.strip()

            if item_anonimity == "elite proxy" or item_anonimity == "anonymous":
                self.proxies.append(f"http://{item_ip}:{item_port}")

    def get_random(self, link):
        link = link.replace("https", "http")

        self.__update()
        
        for proxy in self.proxies:

            proxy_list = {
                "http" : proxy,
                "https" : proxy
            }

            try:
                response = requests.get(
                    link,
                    proxies=proxy_list,
                    timeout=3
                )
                if response.status_code == 200:
                    return proxy_list

            except:
                pass

if __name__ == "__main__":
    pass



