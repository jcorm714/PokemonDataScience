import json
import pandas as pd
import calculate_type_effectiveness as cte
from typing import Optional

def load_info(filepath):
        with open(filepath, "r") as fil:
                return json.load(fil)

def sort_info(json_obj):
        types = json_obj["types"]
        tiers = json_obj["tiers"]
        pokemon = json_obj["pokemon"]
        return (types, tiers, pokemon)

def get_offensive_score(type1: str, type2:Optional[str] = None) -> float:
        score = -1
        if type2 is not None:
                type1_off = cte.get_offensive_list(type1.lower())
                type2_off = cte.get_offensive_list(type2.lower())
                joined_offensives = []
                type1_off = list(type1_off)
                type2_off = list(type2_off)
                for i in range(len(type1_off)):
                        higher_value = type1_off[i] if(type1_off[i] >= type2_off[i]) else type2_off[i]
                        joined_offensives.append(higher_value)
                score = sum(joined_offensives)
        else:
                offenses = cte.get_offensive_list(type1.lower())
                score = sum(offenses)
        
        return score


def get_defensive_score(type1: str, type2: Optional[str] = None) -> float:
        score = -1
        if type2 is not None:
                t1_defs = cte.get_defensive_list(type1.lower())
                t2_defs = cte.get_defensive_list(type2.lower())
                joined_defs = []
                t1_defs = list(t1_defs)
                t2_defs = list(t2_defs)
                for i in range(len(t1_defs)):
                        joined_defs.append(t1_defs[i]*t2_defs[i])
                score = sum(joined_defs)
                
        else:
                defenses = cte.get_defensive_list(type1.lower())
                score = sum(defenses)
        return score


def pokemon_to_row(poke_json):

        if poke_json is None:
                return None
        name = poke_json["name"]
        type1 = poke_json["types"][0]
        type2 = poke_json["types"][1] if (len(poke_json["types"]) >= 2) else None
        ability1 = poke_json["abilities"][0]
        ability2 = poke_json["abilities"][1] if(len(poke_json["abilities"])>=2) else None
        ability3 = poke_json["abilities"][2] if(len(poke_json["abilities"])>=3) else None
        tier = poke_json["tiers"][0]
        hp = poke_json["stats"]["HP"]
        attack = poke_json["stats"]["Attack"]
        defense = poke_json["stats"]["Defense"]
        spa = poke_json["stats"]["Sp. Atk"]
        spd = poke_json["stats"]["Sp. Def"]
        speed = poke_json["stats"]["Speed"]

        off_score = get_offensive_score(type1, type2=type2)
        def_score = get_defensive_score(type1, type2=type2)

        return {             "Name": name,
                             "Type1": type1,
                             "Type2": type2,
                             "Ability1":ability1,
                             "Ability2":ability2,
                             "Ability3":ability3,
                             "Tier": tier,
                             "HP": hp,
                             "Attack": attack,
                             "Defense": defense,
                             "Sp. Atk": spa,
                             "Sp. Def": spd,
                             "Speed": speed,
                             "O-Score": off_score,
                             "D-Score": def_score
                             }


def create_data_set(file_name:str) -> type(pd.DataFrame):
        obj = load_info(file_name)
        types, tiers, pokemon = sort_info(obj)
        data = []
        for pk in pokemon:
               if pk is None:
                       continue
               data.append(pokemon_to_row(pk))

        dataset = pd.DataFrame(data)
        return dataset

if __name__ == "__main__":
       ds =  create_data_set("gen8_info.json")
       print(ds.tail())