"""The purpose of this script is to flatten each row of the pokemon data
into a pandas dataframe, and clean/remove any invalid data"""

import json
import pandas as pd
import calculate_type_effectiveness as cte
from typing import Optional

def load_info(filepath):
        """load in the json object"""
        with open(filepath, "r") as fil:
                return json.load(fil)

def sort_info(json_obj):
        """sort the list of information from the summary,
        every summary contains a list of all the types, all the tiers, and
        then summary of every pokemon available for that generation"""
        types = json_obj["types"]
        tiers = json_obj["tiers"]
        pokemon = json_obj["pokemon"]
        return (types, tiers, pokemon)

def get_offensive_score(type1: str, type2:Optional[str] = None) -> float:
        """Returns the offensive score by the list of type effectiveness, the
        higher the score, the more potential super effective hits the pokemon has"""
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
        """Returns the defensive score by the list of type resistances, the
        lower the score the more resistances a pokemon has"""
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


def pokemon_to_row(poke_json, generation_num):
        """compacts the information for a pokemon into a dictionary
        the dictionary contains the following information
        Gen# -- the Generation the info is from
        Name -- Name of the Pokemon
        Type1 -- Primary Pokemon Type
        Type2 -- Secondary Pokemon Type
        Ability1 -- First Ability of a Pokemon
        Ability2 -- Second Ability of a Pokemon
        Ability3 -- Third Ability of a Pokemon
        Tier -- the tier the pokemon is in
        HP -- HP Stat
        Attack -- Attack Stat
        Defense -- Defense Stat
        Sp. Atk -- Special Attack Stat
        Sp. Def -- Special Defense Stat
        Speed -- Speed Stat
        O-Score -- Offensive scoring based off type(s)
        D-Score -- Defensive scoring based off type(s)
        """
        if poke_json is None:
                return None
        name = poke_json["name"]
        type1 = poke_json["types"][0]
        type2 = poke_json["types"][1] if (len(poke_json["types"]) >= 2) else None
        ability1 = poke_json["abilities"][0] if(len(poke_json["abilities"])) else None
        ability2 = poke_json["abilities"][1] if(len(poke_json["abilities"])>=2) else None
        ability3 = poke_json["abilities"][2] if(len(poke_json["abilities"])>=3) else None
        tier = poke_json["tiers"][0] if(len(poke_json["tiers"])) else None
        hp = poke_json["stats"]["HP"]
        attack = poke_json["stats"]["Attack"]
        defense = poke_json["stats"]["Defense"]
        spa = poke_json["stats"]["Sp. Atk"]
        spd = poke_json["stats"]["Sp. Def"]
        speed = poke_json["stats"]["Speed"]

        off_score = get_offensive_score(type1, type2=type2)
        def_score = get_defensive_score(type1, type2=type2)

        return {             "Gen#": generation_num,
                             "Name": name,
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


def create_data_set(file_name:str, genNum:int) -> type(pd.DataFrame):
        """Creates a individual Panadas Data frame for a generation"""
        obj = load_info(file_name)
        types, tiers, pokemon = sort_info(obj)
        data = []
        for pk in pokemon:
               if pk is None:
                       continue
               data.append(pokemon_to_row(pk, genNum))

        dataset = pd.DataFrame(data)
        return dataset

def create_bulk_data_set() -> type(pd.DataFrame):
        """Loads all the data from every generaton into one dataframe"""
        data = []
        for i in range(1, 8+1):  
                obj = load_info(f"gen{i}_info.json")
                types, tiers, pokemon = sort_info(obj)
                for pk in pokemon:
                        if pk is None:
                                continue
                        data.append(pokemon_to_row(pk, i))
        return pd.DataFrame(data)

if __name__ == "__main__":
       ds =  create_bulk_data_set()
       print(ds.tail())