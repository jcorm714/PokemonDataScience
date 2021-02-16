"""The purpose of this script is to return a list of all pokemon names 
and save them to a JSON file"""

from bs4 import BeautifulSoup, SoupStrainer
import requests
import json
import re

NAMES_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_name"


def get_names():
        """Parses only links from Bulbapedia list of pokemon names, pulls the text from it"""
        only_links = SoupStrainer("a")
        names = set()
        doc = requests.get(NAMES_URL).content
        links = BeautifulSoup(doc, "html.parser", parse_only=only_links)
        pokemon = links.find_all(title=re.compile("(\w+)(\s){1}(\(Pokémon\))"))
        for cell in pokemon:
                names.add(str(cell.string))
        

        return names


def save_names_to_json(names):
        """Save list of names to a local json file"""
        with open("names.json", "w") as fil:
                name_list = list(names)
                name_list.sort()
                json.dump(name_list, fil, indent=4)


def main():
        save_names_to_json(get_names())

if __name__ == "__main__":
        main()