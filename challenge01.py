#!/usr/bin/python3
"""Reviewing how to parse json | Alta3 Research"""

# JSON is part of the Python Standard Library
import json

def main():
    """runtime code"""
    ## create a blob of data to work with
    hitchhikers = [
            {
                "name": "Zaphod Beeblebrox", 
                "species": "Betelgeusian", 
                "has_towel": "nope", 
                "travel_count": "41", 
                "home_planet": "venutia"
            },
            {
                "name": "Arthur Dent", 
                "species": "Human",
                "has_towel": "1", 
                "travel_count": "7", 
                "home_planet": "Earth"
            },
            {
                "name": "Belore Higgins", 
                "species": "Traxian",
                "has_towel": "four", 
                "travel_count": "21", 
                "home_planet": "Montico"
                }
            ]

    ## display our Python data (a list containing two dictionaries)
    print(hitchhikers)

    ## open a new file in write mode
    with open("galaxyguide.json", "w") as zfile:
        ## use the JSON library
        ## USAGE: json.dump(input data, file like object) ##
        json.dump(hitchhikers, zfile)

if __name__ == "__main__":
    main()
