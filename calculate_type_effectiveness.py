"""The purpose of this script is to create a matchup of all the types against eachother
by using Bulbapedias type effective chart."""
from bs4 import SoupStrainer, BeautifulSoup
from collections.abc import Iterable

class TypeMatchup:
        
        type_order = ["normal",
              "fighting",
              "flying",
              "poison",
              "ground",
              "rock",
              "bug",
              "ghost",
              "steel",
              "fire",
              "water",
              "grass",
              "electric",
              "psychic",
              "ice",
              "dragon",
              "dark",
              "fairy"]


        def __init__(self):
                self.OffensiveType = ""
                self.defenses = {}
                self.offenses = {}
                # initialize the type effectiveness to be 1 for each type
                for pokemon_type in TypeMatchup.type_order:
                        self.defenses[pokemon_type] = 1
                        self.offenses[pokemon_type] = 1

# Values in the chart are stored as a number or a character such as ½
# Note the × is the muliplication symbol not an x
convert_to_float = lambda tag: float(str(tag.string).strip().replace("×","").replace("½","0.5"))


# the chart is saved locally 
html_doc = ""
with open("type_effective_chart.html", "r") as fil:
        html_doc = "".join(fil.readlines())



only_rows = SoupStrainer("tr")
parser = BeautifulSoup(html_doc, "html.parser", parse_only=only_rows)
type_matchup_info = {}
types = set() 
for row in parser.contents:
        first_col = True
        type_matchup = TypeMatchup()

 
        if row.find("td") is None:
                continue
        type_matchup.OffensiveType = str(row.find("a")["title"]).lower()
        #not sure why but this always appears last and is not a type
        if type_matchup.OffensiveType == 'generation vi':
                break
        types.add(type_matchup.OffensiveType)
        
        # loop through each row and determine the offensive type matchup for a type
        for i,child in enumerate(row.find_all("td")):
                if child.string is None:
                        continue
                cell = str(child.string).strip()
                # this is actually the multiplication symbol not the letter
                if "×" in cell:      
                        float_strength = convert_to_float(child)
                        type_matchup.offenses[TypeMatchup.type_order[i]] = float_strength
        
        type_matchup_info[type_matchup.OffensiveType] = type_matchup

# determine the defensive matchup by looking at all other type effective lists 
for pokemon_type in TypeMatchup.type_order:
        for key, value in type_matchup_info.items():
                type_matchup_info[pokemon_type].defenses[key] = value.offenses[pokemon_type]      
                


def get_defensive_list(type_name: str):
        """Returns the list of matchup values defensive typing in order of TypeMatchup.type_order"""
        return type_matchup_info[type_name].defenses.values()


def get_offensive_list(type_name: str):
        """Returns a list of values for offesive typing in order of TypeMatchup.type_order"""
        return type_matchup_info[type_name].offenses.values()

                




        