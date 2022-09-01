import requests
import multiprocessing
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self) -> None:
        global abort
        abort = multiprocessing.Event()

        global checked_proxies
        checked_proxies = []

    def __update(self):
        
        self.__header = {
            "user-agent" : UserAgent().random
        }
        self.__proxies = []

        link = "https://free-proxy-list.net/"
        response = requests.get(
            link,
            headers=self.__header
        ).text
        soup = BeautifulSoup(response, "lxml")

        tbody = soup.find("tbody")
        items = tbody.find_all("tr")
        
        for item in items:

            item_info = item.find_all("td")

            item_ip = item_info[0].text.strip()
            item_port = item_info[1].text.strip()
            item_anonimity = item_info[4].text.strip()

            if item_anonimity == "elite proxy" or item_anonimity == "anonymous":
                self.__proxies.append(f"http://{item_ip}:{item_port}")


    def try_proxy(self, proxy):

        if abort.is_set() == False:

            proxy_dict = {
                "http" : proxy,
                "https" : proxy
            }

            try:
                response = requests.get(
                    self.__link,
                    headers=self.__header,
                    proxies=proxy_dict,
                    timeout=1
                )
                if response.status_code == 200:
                    abort.set()   
                    return (response, proxy)
                    
            except:
                pass


    def __get_proxy(self):
        
        self.__update()
        abort.clear()

        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            list_of_pairs = process.map(
                self.try_proxy, 
                self.__proxies
            )
            
        for elem in list_of_pairs:
            if elem != None:
                response = elem[0]
                checked_proxies.append(elem[1])

        if len(checked_proxies) == 0:
            print("ALARM: NO PROXIES!")

        return response


    def __check_proxies_again(self):

        for proxy in checked_proxies:

            proxy_dict = {
                "http" : proxy,
                "https" : proxy
            }

            try:
                response = requests.get(
                    self.__link,
                    headers=self.__header,
                    proxies=proxy_dict,
                    timeout=1
                )
                if response.status_code == 200:
                    return response
                    
            except:
                checked_proxies.remove(proxy)


    def get_response(self, link):

        self.__link = link.replace("https", "http")

        if len(checked_proxies):
            response = self.__check_proxies_again()
            
            if response != None:
                return response

        response = self.__get_proxy()
    
        return response
        


if __name__ == "__main__":
    a = Proxy()
    link = "https://icanhazip.com/"
    
    for i in range(5):
        rsp = a.get_response(link)
        print(rsp.text.strip())
