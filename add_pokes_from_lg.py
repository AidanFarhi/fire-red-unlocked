"""
The purpose of this script is to simply add all of the pokes that are
exclusive to Leaf Green to Fire Red
"""

import json

VERSION_FIRE_RED = "_FireRed"
VERSION_LEAF_GREEN = "_LeafGreen"
ENCOUNTER_TYPES = ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons")


def is_version_fire_red(encounter: dict) -> bool:
    return encounter["base_label"].endswith(VERSION_FIRE_RED)


def is_version_leaf_green(encounter: dict) -> bool:
    return encounter["base_label"].endswith(VERSION_LEAF_GREEN)


def poke_exists_in_list(pokes: list, poke_to_check: dict) -> bool:
    for poke in pokes:
        if poke == poke_to_check:
            return True
    return False


def add_lg_mons_to_fr_encounter(fr_encounters: list, lg_encounters: list):
    for fr_enc in fr_encounters:
        fr_enc_base_label = fr_enc["base_label"].removesuffix(VERSION_FIRE_RED)
        for lg_enc in lg_encounters:
            lg_enc_base_label = lg_enc["base_label"].removesuffix(VERSION_LEAF_GREEN)
            if fr_enc_base_label == lg_enc_base_label:
                for key in fr_enc:
                    if key in ENCOUNTER_TYPES:
                        fr_mons = fr_enc[key]["mons"]
                        lg_mons = lg_enc[key]["mons"]
                        for poke in lg_mons:
                            if not poke_exists_in_list(fr_mons, poke):
                                fr_enc[key]["mons"].append(poke)


def main():

    input_file = open("./src/data/wild_encounters.json", "r")
    original_wild_encounters = json.load(input_file)
    encounters = original_wild_encounters["wild_encounter_groups"][0]["encounters"]
    fr_encounters = list(filter(is_version_fire_red, encounters))
    lg_encounters = list(filter(is_version_leaf_green, encounters))
    add_lg_mons_to_fr_encounter(fr_encounters, lg_encounters)
    input_file.close()

    output_file = open("./src/data/wild_encounters.json", "w")
    json.dump(original_wild_encounters, output_file, indent=2)
    output_file.close()


if __name__ == "__main__":
    main()
