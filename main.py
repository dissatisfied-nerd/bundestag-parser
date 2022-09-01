import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from my_proxy import Proxy

import os
import multiprocessing
import json

def get_items(i):

    global proxy
    proxy = Proxy() 

    print(f"Parsing page #{i}...", end="")

    header = {
        "user-agent" : UserAgent().random
    }

    os.chdir(path_pages)
    
    with open(f"page_{i}.html") as file:
        response = file.read()

    soup = BeautifulSoup(response, "lxml")
    people = soup.find_all("a")

    for j in range(len(people)):

        item_link = people[j].get("href")
        item_response = requests.get(item_link, headers=header)
        #item_response = proxy.get_response(item_link)

        if item_response.text.count("\n") == 0:
            item_response = proxy.get_response(item_link)
    
        if os.path.exists(f"{path_items}/page_{i}") == False:
            
            os.chdir(path_items)
            os.mkdir(f"page_{i}")
            os.chdir(f"{path_items}/page_{i}")
    
        with open(f"item_{j}.html", "w") as file:
            file.write(item_response.text)

    print("succesfully.")


def item_sort(elem):
    return int(
        elem.replace("item_", "").replace(".html", "")
    )


def make_db(page):

    os.chdir(f"{path_items}/{page}")

    items = os.listdir(os.getcwd())
    items.sort(
        key=item_sort
    )

    data = []

    for item in items:

        with open(item) as file:
            item_response = file.read()

        try:

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

            data.append(item_dict)

        except:
            os.chdir(path_template_data)

            with open("errors.txt", "a") as file:
                file.write(f"Error: {page}, {item}.\n")

            os.chdir(f"{path_items}/{page}")

    return data


def page_sort(elem):
    return int(elem.replace("page_", ""))


if __name__ == "__main__":

    global path_pages, path_items

    path_pages = "/home/axr/projects/Bundestag/template_data/pages"
    path_items = "/home/axr/projects/Bundestag/template_data/items"
    path_template_data = "/home/axr/projects/Bundestag/template_data"

    os.chdir(path_items)
    pages = os.listdir(path_items)
    pages.sort(
        key=page_sort
    )
    
    with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
        template_data_base = [elem for elem in
            process.map(
                make_db,
                pages
            )
        ]

    data_base = []

    for elem in template_data_base:
        for value in elem:
            data_base.append(value)

    os.chdir(path_template_data)

    with open("data_base.json", "w") as file:
        json.dump(data_base, file, indent=4, ensure_ascii=False)
