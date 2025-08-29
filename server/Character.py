# Character.py

import os
import json
import struct

from BitUtils import BitBuffer
from Items import inventory_gears, default_learned_abilities, starting_dyes, \
    Active_master_Class, Mastery_Class, Active_Abilities, Starting_Mounts, \
    Starting_Pets, Starter_Weapons, Buildings, Starting_Charms, \
    Starting_Materials, Starting_Consumables, Starting_Missions
from constants import GearType, GEARTYPE_BITS


def build_level_gears_packet(gears_list: list[tuple[int, int]]) -> bytes:
    """
    Build packet 0xF5 with list of (gear_id, tier) tuples.
    Args:
        gears_list: List of tuples containing (gear_id, tier).
    """
    buf = BitBuffer()
    buf.write_method_4(len(gears_list))  # Write number of gears
    for gear_id, tier in gears_list:
        buf.write_method_6(gear_id, GEARTYPE_BITS)  # 11 bits for gearID
        buf.write_method_6(tier, GearType.const_176)  # 2 bits for tier
    payload = buf.to_bytes()
    return struct.pack(">HH", 0xF5, len(payload)) + payload

def get_inventory_gears(char: dict) -> list[tuple[int, int]]:
    """
    Extract gear_id and tier from character's inventoryGears.
    Args:
        char: Character dictionary containing inventoryGears.
    Returns:
        List of (gear_id, tier) tuples.
    """
    inventory_gears = char.get("inventoryGears", [])
    return [(gear.get("gearID", 0), gear.get("tier", 0)) for gear in inventory_gears]

# Hints Do not delete
"""
  "gearSets": [
    {
      "name": "PvP Build",    
        "slots": [4 1181, (ChestPlate)
                  5 1180, (Gloves)
                  6 1182, (Boots)
                  3 1181, (Hat)
                  1 1177, (Sword)
                  2 1178  (Shield)
        ]
    }
  ]
  "magicForge": {
  "stats_by_building": {
          "1": 10, # "Tome"
          "2": 10, # "Forge"
          
          "3": 10, # "JusticarTower"
          "4": 10, # "SentinelTower"
          "5": 10, # "TemplarTower"
          
          "6": 10, # "FrostwardenTower"
          "7": 10, # "FlameseerTower"
          "8": 10, # "NecromancerTower"
          
          "9": 10, # "ExecutionerTower"
          "10": 10, # "ShadowwalkerTower"
          "11": 10, # "SoulthiefTower"
          
          "12": 0, # "Keep"
          "13": 10 # "Barn"
        },
  "hasSession": true,    // 1bit: whether a forge session exists (controls reading the session block)
  "primary": 90,         // primary gem/charm type ID (6 bits)
  "secondary": 5,        // secondary buff ID (only read if status==2 and var_8==1)
  "status": 1,           // 1=in‑progress (timer), 2=completed (secondary buffs)
  "duration": 900000,    // remaining time in ms (used to compute endtime when status==1)
  "var_8": 1,            // flag for “secondary present” (1 bit, read only when status!=1)
  "usedlist": 2,         // number of items/idols used or buff count (read if var_8==1)
  "var_2675": 2,         // extra small stat #1 (16 bits, always read)
  "var_2316": 2,         // extra small stat #2 (16 bits, always read)
  "var_2434": true       // final continuation flag (1 bit; often used to toggle UI)
}
  
"""
# ──────────────── Default full gear definitions ────────────────
# Each sub-list is [GearID, Rune1, Rune2, Rune3, Color1, Color2]
DEFAULT_GEAR = {
    "paladin": [
        [1, 0, 0, 0, 0, 0],  # Shield
        [13, 0, 0, 0, 0, 0],  # Sword
        [0, 0, 0, 0, 0, 0],  # Gloves
        [0, 0, 0, 0, 0, 0],  # Hat
        [0, 0, 0, 0, 0, 0],  # Armor
        [0, 0, 0, 0, 0, 0],  # Boots
    ],
    "rogue": [
        [39, 0, 0, 0, 0, 0],  # Off Hand/Shield
        [27, 0, 0, 0, 0, 0],  # Sword
        [0, 0, 0, 0, 0, 0],  # Gloves
        [0, 0, 0, 0, 0, 0],  # Hat
        [0, 0, 0, 0, 0, 0],  # Armor
        [0, 0, 0, 0, 0, 0],  # Boots
    ],
    "mage": [
        [53, 0, 0, 0, 0, 0],  # Staff
        [65, 0, 0, 0, 0, 0],  # Focus/Shield
        [0, 0, 0, 0, 0, 0],  # Gloves
        [0, 0, 0, 0, 0, 0],  # Hat
        [0, 0, 0, 0, 0, 0],  # Robe
        [0, 0, 0, 0, 0, 0],  # Boots
    ],
}

CHAR_SAVE_DIR = "saves"


def load_characters(user_id: str) -> list[dict]:
    """Load the list of characters for a given user_id."""
    path = os.path.join(CHAR_SAVE_DIR, f"{user_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("characters", [])


def save_characters(user_id: str, char_list: list[dict]):
    """Save the list of characters for a given user_id, preserving other fields."""
    os.makedirs(CHAR_SAVE_DIR, exist_ok=True)
    path = os.path.join(CHAR_SAVE_DIR, f"{user_id}.json")
    # Load existing to preserve email and other fields
    if user_id is None:
        print("Warning: Attempted to save characters with user_id=None")
        return
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"email": None, "characters": []}
    data["characters"] = char_list
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def make_character_dict_from_tuple(character):
    """
    character is a tuple of:
      (name, class_name, level,
       gender, head, hair, mouth, face,
       hair_color, skin_color, shirt_color, pant_color,
       equipped_gear)
    where equipped_gear can be:
      - None → use DEFAULT_GEAR for that class
      - a list of six 6-element lists → use directly
    """
    (name, class_name, level,
     gender, head, hair, mouth, face,
     hair_color, skin_color, shirt_color, pant_color,
     equipped_gear) = character

    cls = class_name.lower()

    # If provided a full 6×6 structure, validate and use it:
    if (isinstance(equipped_gear, (list, tuple))
            and len(equipped_gear) == 6
            and all(isinstance(slot, (list, tuple)) and len(slot) == 6
                    for slot in equipped_gear)):
        gear_list = [list(slot) for slot in equipped_gear]
    else:
        # Otherwise, pull from our per-class defaults
        default = DEFAULT_GEAR.get(cls, [[0] * 6] * 6)
        gear_list = [list(slot) for slot in default]

    starting_inventory = inventory_gears.get(cls, [])
    starting_abilities = default_learned_abilities.get(cls, [])
    starting_talent = Active_master_Class.get(cls, [])
    Starting_Mastery = Mastery_Class.get(cls, [])
    starter_gear = Starter_Weapons.get(cls, [])
    Starting_Active_Abilities = Active_Abilities.get(cls, [])
    Starting_Buildings = Buildings.get(cls, [])

    char_dict = {
        "name": name,
        "class": class_name,
        "level": level,
        "xp": 29116890,
        "gold": 100000,
        "craftXP": 100000,
        "DragonOre": 100000,
        "mammothIdols": 100000,
        "DragonKeys": 100000,
        "SilverSigils": 100000,
        "gender": gender or "Male",
        "headSet": head or "Head01",
        "hairSet": hair or "Hair01",
        "mouthSet": mouth or "Mouth01",
        "faceSet": face or "Face01",
        "hairColor": hair_color,
        "skinColor": skin_color,
        "shirtColor": shirt_color,
        "pantColor": pant_color,
        "equippedGears": starter_gear,
        "CurrentLevel": {"name": "CraftTown", "x": 360, "y": 1458.99},
        "PreviousLevel": {"name": "NewbieRoad", "x": 0, "y": 0},
        "inventoryGears": starting_inventory,
        "gearSets": [],
        "mounts": Starting_Mounts,
        "pets": Starting_Pets,
        "charms": Starting_Charms,
        "materials": Starting_Materials,
        "lockboxes": [{"lockboxID": 1, "count": 100}],
        "OwnedDyes": starting_dyes,
        "consumables": Starting_Consumables,
        "missions": Starting_Missions,
        "friends": [
            {
                "name": "Neutral",
                "className": "Paladin",
                "level": 40,
                "stateVersion": 5,
                "isRequest": True,
                "isOnline": True
            },
            {
                "name": "Neo",
                "className": "Mage",
                "level": 20,
                "stateVersion": 5,
                "isRequest": True,
                "isOnline": True
            },
            {
                "name": "Tired",
                "className": "Rogue",
                "level": 23,
                "stateVersion": 5,
                "isRequest": False,
                "isOnline": True
            },
            {
                "name": "Telahair",
                "className": "Mage",
                "level": 23,
                "stateVersion": 5,
                "isRequest": False,
                "isOnline": False
            },
            {
                "name": "twig",
                "className": "Rogue",
                "level": 50,
                "stateVersion": 5,
                "isRequest": False,
                "isOnline": True
            }
        ],
        "learnedAbilities": starting_abilities,
        "activeAbilities": Starting_Active_Abilities,
        "craftTalentPoints": [5, 5, 5, 5, 5],  # these are the Magic Forge upgrade points Max value is 10 each
        "talentPoints": {
            "1": 1,
            "2": 1,
            "3": 1
        },  # Talent upgrade 50 Max each
        # =================
        "magicForge": {
            "stats_by_building": Starting_Buildings,
            "hasSession": False,
            "primary": 0,
            "secondary": 0,
            "status": 0,
            "duration": 0,
            "_start_time": 0,
            "var_8": 0,
            "usedlist": 0,
            "var_2675": 0,
            "var_2316": 0,
            "var_2434": False
        },
        # ===================
        "research": {
            "abilityID": 0,
            "ReadyTime": 0,
            "done": True
        },
        "buildingUpgrade": {
            "buildingID": 0,
            "rank": 0,
            "ReadyTime": 0,
            "done": True,
            "isInstant": False
        },
        "talentResearch": {
            "classIndex": None,
            "ReadyTime": 0,
            "done": True,
            "isInstant": False
        },
        "EggHachery": {
             "EggID": 0,
             "ReadyTime": 0,
             "done": True
        },
        "OwnedEggsID": [1, 2, 30, 27, 5, 35, 20, 17],
        "activeEggCount": 5,
        "restingPets": [
            {
                "typeID": 2
            },
            {
                "typeID": 3
            },
            {
                "typeID": 4
            }
        ],
        "trainingPet": [
            {
                "typeID": 0,
                "trainingTime": 0
            }
        ],
        "MasterClass": starting_talent,
        "Mastery": Starting_Mastery,
        "equippedMount": 1,
        "equippedPetID": 1,
        "activeConsumableID": 13,
        "queuedConsumableID": 12,
        "guild": {
            "name": "KnightsOfValor",
            "rank": 2,
            "onlineMembers": [
                {
                    "name": "ProGooner",
                    "classID": 1,
                    "level": 50,
                    "status": 3
                },
                {
                    "name": "FriendlyNephit",
                    "classID": 1,
                    "level": 43,
                    "status": 3
                }
            ]
        },

    }
    return char_dict


def build_paperdoll_packet(character_dict):
    buf = BitBuffer(debug=True)  # Enable debug for tracing
    buf.write_utf_string(character_dict["name"])
    buf.write_utf_string(character_dict["class"])
    buf.write_utf_string(character_dict["gender"])
    buf.write_utf_string(character_dict["headSet"])
    buf.write_utf_string(character_dict["hairSet"])
    buf.write_utf_string(character_dict["mouthSet"])
    buf.write_utf_string(character_dict["faceSet"])
    buf.write_bits(character_dict["hairColor"], 24)
    buf.write_bits(character_dict["skinColor"], 24)
    buf.write_bits(character_dict["shirtColor"], 24)
    buf.write_bits(character_dict["pantColor"], 24)

    # Add gear slots (slots 1 to 6, as slot 0 is skipped)
    cls = character_dict["class"].lower()
    # Prefer equippedGears if available, else fall back to DEFAULT_GEAR
    gear_list = character_dict.get("equippedGears", DEFAULT_GEAR.get(cls, [[0] * 6] * 6))

    for i in range(6):  # Process exactly 6 slots (1 to 6)
        if i < len(gear_list):
            slot = gear_list[i]
            # Handle both dictionary (equippedGears) and list (DEFAULT_GEAR) formats
            if isinstance(slot, dict):
                gear_id = slot.get("gearID", 0)
            elif isinstance(slot, (list, tuple)) and len(slot) > 0:
                gear_id = slot[0]
            else:
                gear_id = 0
        else:
            gear_id = 0
        buf.write_bits(gear_id, 11)  # GearType.GEARTYPE_BITSTOSEND = 11
        if buf.debug:
            buf.debug_log.append(f"gear_slot_{i + 1}_gearID={gear_id}")

    return buf.to_bytes()


def build_login_character_list_bitpacked(characters):
    """
    Builds the 0x15 login-character-list packet.
    """
    buf = BitBuffer()
    user_id = 1  # you’ll overwrite this per-session
    max_chars = 8
    char_count = len(characters)

    buf.write_method_4(user_id)
    buf.write_method_393(max_chars)
    buf.write_method_393(char_count)

    for char in characters:
        buf.write_utf_string(char["name"])
        buf.write_utf_string(char["class"])
        buf.write_method_6(char["level"], 6)

    import struct
    header = struct.pack(">HH", 0x15, len(buf.to_bytes()))
    return header + buf.to_bytes()
