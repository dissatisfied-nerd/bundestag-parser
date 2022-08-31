import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from my_proxy import Proxy

import os

if __name__ == "__main__":

    path_pages = "/home/axr/prog/parsing/Bundestag/template_data/pages"
    path_items = "/home/axr/prog/parsing/Bundestag/template_data/items"

    proxy_object = Proxy()
    item_link = "https://icanhazip.com/"
    proxy_counter = 0

    for i in range(0, 732 + 1, 12):

        if proxy_counter % 5 == 0:
            proxies = proxy_object.get_random(item_link)
            print(f"Iteration #{i}, proxy:", {proxies.get("http")})
        
        proxy_counter += 1

        header = {
            "user-agent" : UserAgent().random
        }

        os.chdir(path_pages)
        
        with open(f"page_{i}.html") as file:
            response = file.read()

        soup = BeautifulSoup(response, "lxml")
        people = soup.find_all("a")

        for j in range(len(people)):

            item_link = people[j].get("href").replace("https", "http")
            
            item_response = requests.get(
                item_link,
                headers=header,
                proxies=proxies
            ).text

            if item_response.count("\n") == 0:
                print(f"Last iteration - {i}")
                exit()

            if os.path.exists(f"{path_items}/page_{i}") == False:
                
                os.chdir(path_items)
                os.mkdir(f"page_{i}")
                os.chdir(f"{path_items}/page_{i}")

            with open(f"item_{j}.html", "w") as file:
                file.write(item_response)


        '''data_base = []

        for elem in people:

            item_link = elem.get("href")
            item_response = requests.get(item_link, headers=header).text
            item_soup = BeautifulSoup(item_response, "lxml")

            item_info = item_soup.find("h3").text.strip().split(", ")
            item_name = item_info[0]
            item_party = item_info[1]

            item_bio = item_soup.find(
                "div",
                id="ptv1"
            )

            item_shrot_bio = item_bio.find("p").text.split(";")
            
            if len(item_shrot_bio) > 2:
                item_religion = item_shrot_bio[1].strip()
            else:
                item_religion = "Unknown"

            item_dict = {
                "Name" : item_name,
                "Party" : item_party,
                "Religion" : item_religion
            }

            contact_names = []
            contact_links = []

            item_socials = item_soup.find_all(
                "a",
                {"class" : "bt-link-extern"}
            )

            for contact in item_socials:

                contact_name = contact.text.strip()
                contact_link = contact.get("href").strip()

                contact_names.append(contact_name)
                contact_links.append(contact_link)

            contacts_dict = {
                contact_names[i] : contact_links[i] for i in range(len(contact_names))
            }
            item_dict.update(contacts_dict)

            data_base.append(item_dict)

    with open("data_base.json", "a") as file:
        json.dump(data_base, file, indent=4, ensure_ascii=False)'''
