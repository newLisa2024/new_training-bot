import json
from config import BOT_NAME


def load_valid_codes():
    with open('params.json', 'r') as file:
        data = json.load(file)
    return data['valid_codes']

def generate_links(bot_name, valid_codes):
    links = {}
    base_url = f"https://t.me/{bot_name}?start="
    for code, access_level in valid_codes.items():
        links[access_level] = base_url + code
    return links

def save_links_to_file(links, filename="links.txt"):
    with open(filename, 'w') as file:
        for code, link in links.items():
            file.write(f"{code}: {link}\n")

def create_links():
    valid_codes = load_valid_codes()
    links = generate_links(BOT_NAME, valid_codes)
    save_links_to_file(links)
    print("Ссылки сгенерированы и сохранены в links.txt")

create_links()