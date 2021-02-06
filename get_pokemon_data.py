import json

import find_all_pokemon_names
from web_driver import WebAccessor
from time import sleep
from bs4 import BeautifulSoup



GEN_VIII_URL = "https://www.smogon.com/dex/ss/pokemon/"
GEN_VII_URL = "https://www.smogon.com/dex/sm/pokemon/"
GEN_VI_URL = "https://www.smogon.com/dex/xy/pokemon/"
GEN_V_URL = "https://www.smogon.com/dex/bw/pokemon/"
GEN_IV_URL = "https://www.smogon.com/dex/dp/pokemon/"
GEN_III_URL = "https://www.smogon.com/dex/rs/pokemon/"
GEN_II_URL = "https://www.smogon.com/dex/gs/pokemon/"
GEN_I_URL = "https://www.smogon.com/dex/rb/pokemon/"

all_types = set()
all_tiers = set()

def get_pokemon_types(dom):
        pokemon_types = dom.find( "div", class_="PokemonSummary-types" )
        links = pokemon_types.find_all("a")
        links = [str(link.string) for link in links if link.has_attr("class") and "Type" in link["class"]]
        for link in links:
                all_types.add(link)
        return links

def get_pokemon_abilities(dom):
        links = dom.find_all("a", class_="AbilityLink")
        abilities = []
        for link in links:
                children = [child for child in link.findChildren()]
                abilities.append(str(children[0].string))
        return abilities

def get_pokemon_tiers(dom):
        tiers = dom.find("ul", class_="FormatList" )
        tiers = [str(tier.string) for tier in tiers.contents if tier.string is not None]
        for tier in tiers:
                all_tiers.add(tier)
        return tiers

def get_pokemon_stats(dom):
        stats = {}
        rows = dom.find_all("tr")
        for i, row in enumerate(rows):
                if(i == 6):
                        break
                stat = str(row.contents[0].string)
                value = int(row.contents[1].string)
     
                stat = stat.replace(":", "")
                stats[stat] = value
        # only speed displays as None
        stats["Speed"] = stats['None']
        del stats["None"]
        return stats

def get_pokemon_page(name, accessor, gen_url = GEN_VIII_URL):
        result = ""
        resp = accessor.get(gen_url + name.lower(), logging=True)
        if resp is None:
                return
        main_container = resp.find_element_by_id("container")

        if name in resp.title:
                result = main_container.get_attribute("innerHTML")
                
        return result



def get_pokemon_info(name, accessor, url = GEN_VIII_URL):
        html = get_pokemon_page(name, accessor, gen_url=url)
        if not html:
                return
        parser = BeautifulSoup(html, "html.parser")
        summary_table = parser.find("table", class_="PokemonSummary")
        stats_table = parser.find("table", class_="PokemonStats")
        types = get_pokemon_types(summary_table)
        abilities = get_pokemon_abilities(summary_table)
        tiers = get_pokemon_tiers(summary_table)
        stats = get_pokemon_stats(stats_table)

        return {"name": name, 
         "types": types,
         "abilities": abilities,
         "tiers": tiers,
         "stats": stats}


def main():
        names = find_all_pokemon_names.get_names()
        names = list(names)
        names.sort()
        accessor = WebAccessor.instance()
        pokemon_list = []
        for i, name in enumerate(names):
                print(f"{i + 1}/{len(names)}", end="\t")
                info = get_pokemon_info(name, accessor, url=GEN_VII_URL)
                pokemon_list.append(info)
        accessor.instance().close()

        with open("gen7_info.json", "w") as fil:
                json.dump({"types": list(all_types),"tiers": list(all_tiers), "pokemon":pokemon_list}, fil, indent=4)

if __name__ == "__main__":
        main()








