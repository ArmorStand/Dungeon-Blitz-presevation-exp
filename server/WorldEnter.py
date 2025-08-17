# WorldEnter.py
from typing import Dict

from BitUtils import BitBuffer
import struct
import time
from constants import (
    GS_BITS,
    MAX_CHAR_LEVEL_BITS,
    class_10_const_83,
    GearType,
    class_10_const_665,
    CLASS_NAME_TO_ID,
    ENTITY_CONST_244,
    class_64,
    class_9_const_28,
    class_1_const_254,
    class_64_const_499,
    class_111_const_432,
    class_64_const_218,
    class_9_const_129,
    class_16_const_167,
    class_7_const_19,
    NEWS_EVENTS,
    GAME_CONST_209,
    CLASS_118_CONST_127,
    SLOT_BIT_WIDTHS,
    NUM_TALENT_SLOTS,
    GEARTYPE_BITS,
    class_119, class_111, class_9, class_66, MASTERCLASS_TO_BUILDING, class_21, Game, Mission,

)
from missions import get_total_mission_defs, get_mission_def

CLASS_BUILD_ORDER = {
    "paladin": [2, 12, 3, 4, 5, 1, 13],
    "mage":    [2, 12, 6, 7, 8, 1, 13],
    "rogue":   [2, 12, 9, 10,11, 1, 13],
}

def Player_Data_Packet(char: dict,
                      event_index: int = 0,
                      transfer_token: int = 0,
                      scaling_factor: int = 0,# Unknown
                      bonus_levels: int = 0,# this is to scale the players Level on dungeons if the player joins a friends dungeon who is higher level
                      target_level: str = None,
                      new_x: int = None,
                      new_y: int = None,
                      new_has_coord: bool = True) -> bytes:

    buf = BitBuffer()

    # ──────────────(Preamble)──────────────
    buf.write_method_4(transfer_token)  # _loc2_
    current_game_time = int(time.time())  # seconds
    buf.write_method_4(current_game_time)
    # _loc3_
    scaling_factor = max(0, min(scaling_factor, 3))  # Clamp to 0–3 (2-bit range)
    buf.write_method_6(scaling_factor, GS_BITS)  # _loc4_
    bonus_levels = max(0, min(bonus_levels, 0xFFFFFFFF))  # Clamp to uint32
    buf.write_method_4(bonus_levels)  # _loc5_

    # ──────────────(Customization)──────────────
    buf.write_utf_string(char.get("name", "") or "")
    buf._append_bits(1, 1)  # hasCustomization
    buf.write_utf_string(char.get("class", "") or "")
    buf.write_utf_string(char.get("gender", "") or "")
    buf.write_utf_string(char.get("headSet", "") or "")
    buf.write_utf_string(char.get("hairSet", "") or "")
    buf.write_utf_string(char.get("mouthSet", "") or "")
    buf.write_utf_string(char.get("faceSet", "") or "")
    buf._append_bits(char.get("hairColor", 0), 24)
    buf._append_bits(char.get("skinColor", 0), 24)
    buf._append_bits(char.get("shirtColor", 0), 24)
    buf._append_bits(char.get("pantColor", 0), 24)

    # ──────────────(Gear Slots)──────────────
    gear_list = char.get("equippedGears", [])
    for gear in gear_list:
        gear_id = gear.get("gearID", 0)
        rune1, rune2, rune3 = gear.get("runes", [0, 0, 0])
        color1, color2 = gear.get("colors", [0, 0])

        if gear_id:
            buf._append_bits(1, 1)  # presence bit
            buf._append_bits(gear_id, 11)  # Gear ID (11 bits)
            buf._append_bits(0, 2)  # reserved/flags (still hardcoded to 0)
            buf._append_bits(rune1, 16)
            buf._append_bits(rune2, 16)
            buf._append_bits(rune3, 16)
            buf._append_bits(color1, 8)
            buf._append_bits(color2, 8)
        else:
            buf._append_bits(0, 1)  # no item in this slot

    # ──────────────(Numeric fields)──────────────
    char_level = char.get("level", 1) or 1
    buf.write_method_6(char_level, MAX_CHAR_LEVEL_BITS)
    buf.write_method_4(char.get("xp", 0))  # xp
    buf.write_method_4(char.get("gold", 0))  # gold
    buf.write_method_4(char.get("craftXP", 0))  # Gems
    buf.write_method_4(char.get("DragonOre", 0))  # DragonOre
    buf.write_method_4(char.get("mammothIdols", 0))  # mammoth idols



    buf._append_bits(int(char.get("showHigher", True)), 1)# Unknown

    # ──────────────(Quest-tracker)──────────────
    # updates the current percentage of the current Dungeon this was likely used when the player join a in progress dungeon
    quest_val = char.get("questTrackerState", 0)
    if quest_val is not None:
        buf._append_bits(1, 1)
        buf.write_method_4(quest_val)
    else:
        buf._append_bits(0, 1)

    # ──────────────(Position‐presence)──────────────
    #buf._append_bits(0, 1)  # no door/teleport update
    if new_has_coord and target_level and new_x is not None and new_y is not None:
        buf._append_bits(1, 1)
        buf.write_signed_method_45(new_x)
        buf.write_signed_method_45(new_y)
    else:
        buf._append_bits(0, 1)

    # ──────────────(Extended‐data‐presence)──────────────
    buf._append_bits(1, 1)  # yes, sending extended data

    # ──────────────(Extended data block)──────────────


    # ──────────────(Inventory Gears)──────────────
    inventory_gears = char.get("inventoryGears", [])
    buf.write_method_6(len(inventory_gears), GearType.GEARTYPE_BITSTOSEND)  # Number of gears (11 bits)
    for gear in inventory_gears:
        gear_id = gear.get("gearID", 0)
        tier = gear.get("tier", 0)
        runes = gear.get("runes", [0, 0, 0])
        colors = gear.get("colors", [0, 0])

        buf._append_bits(gear_id, 11)  # Gear ID (11 bits)
        buf._append_bits(tier, GearType.const_176)  # Tier (2 bits)

        has_modifiers = any(rune != 0 for rune in runes) or any(color != 0 for color in colors)
        buf._append_bits(1 if has_modifiers else 0, 1)  # has_modifiers bit

        if has_modifiers:
            for i in range(3):
                rune = runes[i]
                rune_present = rune != 0
                buf._append_bits(1 if rune_present else 0, 1)
                if rune_present:
                    buf._append_bits(rune, 16)  # Rune ID (16 bits)
            for i in range(2):
                color = colors[i]
                color_present = color != 0
                buf._append_bits(1 if color_present else 0, 1)
                if color_present:
                    buf._append_bits(color, 8)  # Color value (8 bits)


    # ──────────────(Gear Sets)──────────────
    gear_sets = char.get("gearSets", [])
    buf.write_method_6(len(gear_sets), GearType.const_348)
    for gs in gear_sets:
        buf.write_utf_string(gs.get("name", ""))
        slots = gs.get("slots", [])
        slots = (slots + [0] * 6)[:6]  # pad/truncate to 6
        for gear_id in slots:
            buf._append_bits(gear_id, GearType.GEARTYPE_BITSTOSEND)

    #TODO...
    #no point on working on this :/
    # ──────────────(Keybinds)──────────────
    buf._append_bits(0, 1)  # no keybinds

    # ──────────────(Mounts)──────────────
    mounts = char.get("mounts", [])
    buf.write_method_4(len(mounts))  # Number of mounts
    for mount_id in mounts:
        buf.write_method_4(mount_id)

    # ──────────────(Pets)──────────────
    pets = char.get("pets", [])
    buf.write_method_4(len(pets))  # Number of pets
    for pet in pets:
        type_id = pet.get("typeID", 0)
        iteration = pet.get("level", 0)
        attr1 = pet.get("xp", 0)
        attr2 = pet.get("iteration", 0)
        type_id = max(0, min(type_id, 127))
        iteration = max(0, min(iteration, 63))
        buf.write_method_6(type_id, 7)  # Type ID (7 bits)
        buf.write_method_6(iteration, 6)  # Iteration (6 bits)
        buf.write_method_4(attr1)  # Attribute 1
        buf.write_method_4(attr2)  # Attribute 2


    # ──────────────(Charms)──────────────
    charms = char.get("charms", [])
    for charm in charms:
        charm_id = charm.get("charmID", 0)
        count = charm.get("count", 1)
        buf._append_bits(1, 1)
        buf._append_bits(charm_id, class_64.const_101)
        if count != 1:
            buf._append_bits(1, 1)
            buf.write_method_4(count)
        else:
            buf._append_bits(0, 1)
    buf._append_bits(0, 1)  # no more charms

    # ──────────────(Materials)──────────────
    materials = char.get("materials", [])
    for mat in materials:
        mat_id = mat.get("materialID", 0)
        count = mat.get("count", 1)
        buf._append_bits(1, 1)
        buf.write_method_4(mat_id)
        if count != 1:
            buf._append_bits(1, 1)
            buf.write_method_4(count)
        else:
            buf._append_bits(0, 1)
    buf._append_bits(0, 1)  # no more materials


    # ──────────────(Lockboxes)──────────────
    lockboxes = char.get("lockboxes", [])
    for box in lockboxes:
        box_id = box.get("lockboxID", 0)
        count = box.get("count", 1)
        buf._append_bits(1, 1)
        buf.write_method_4(box_id)
        buf.write_method_4(count)
    buf._append_bits(0, 1)  # no more lockboxes

    # ──────────────(lockboxKeys) and (royalSigils)──────────────
    buf.write_method_4(char.get("DragonKeys", 0))  # lockboxKeys
    buf.write_method_4(char.get("SilverSigils", 0))  # royalSigils


    # this just effects the tutorial tips value 0 will show the "Dyeing Gear available" tip although im not exactly  sure if this is working correctly
    buf.write_method_6(10, Game.const_646)  # alert state = 0


    # ──────────────(dyes)──────────────
    owned_dyes = set(char.get("OwnedDyes", []))  # fast membership checking

    for dye_id in range(1, class_21.const_763 + 1):
        has_dye = 1 if dye_id in owned_dyes else 0
        buf._append_bits(has_dye, 1)


    # ──────────────(consumables)──────────────
    consumables = char.get("consumables", [])
    for item in consumables:
        cid = item.get("consumableID", 0)
        count = item.get("count", 1)
        buf._append_bits(1, 1)
        buf.write_method_4(cid)
        buf.write_method_4(count)
    buf._append_bits(0, 1)  # no more consumables


    # ──────────────(Missions)──────────────
    missions_state: Dict[str, dict] = char.get("missions", {}) or {}

    total_defs = get_total_mission_defs()
    buf.write_method_4(total_defs)  # _loc56_

    for mid in range(1, total_defs + 1):
        mdef = get_mission_def(mid)
        mstate = missions_state.get(str(mid))

        if mdef["Tier"]:
            # Achievement/special → exactly one bit: 1 means create Mission(id, READY, 0)
            ready = (mstate is not None) and (mstate.get("state") == Mission.const_72)
            buf._append_bits(1 if ready else 0, 1)
            continue

        # Regular missions
        has_entry = mstate is not None
        buf._append_bits(1 if has_entry else 0, 1)  # presence bit
        if not has_entry:
            continue

        state = mstate.get("state", Mission.const_213)

        # Second bit: ready vs. not-ready
        is_ready = (state == Mission.const_72)
        buf._append_bits(1 if is_ready else 0, 1)

        if not is_ready:
            # In-progress path: if CompleteCount > 1, send currCount
            if mdef["highscore"] > 1:
                buf.write_method_4(int(mstate.get("currCount", 0)))
        else:
            # Third bit: 1 → READY (turn-in), 0 → CLAIMED (already collected)
            # (client uses this to choose const_72 vs const_58)
            is_turnin = 1 if state == Mission.const_72 else 0
            buf._append_bits(is_turnin, 1)

            # Timed/Ranked extras — only if the *client’s* def has Time set (we mirror that here)
            if mdef["Time"]:
                # Tier 1 to 7 is bronze tier 8 to 9 is silver tier 10 is gold tier
                buf._append_bits(int(mstate.get("Tier", 0)), class_119.const_228)
                buf.write_method_4(int(mstate.get("highscore", 0)))
                buf.write_method_4(int(mstate.get("Time", 0)))

    # ──────────────(Friends)──────────────
    friends = char.get("friends", [])

    # 1) Friend count
    buf.write_method_4(len(friends))

    # 2) Friend entries
    for friend in friends:
        # var_207 → account name
        buf.write_utf_string(friend["name"])

        # var_276 → isRequest
        buf._append_bits(1 if friend.get("isRequest", False) else 0, 1)

        # bOnline
        online = friend.get("isOnline", False)
        buf._append_bits(1 if online else 0, 1)

        if online:
            # Has custom char name?
            custom_name = friend.get("name", "") != friend["name"]
            buf._append_bits(1 if custom_name else 0, 1)
            if custom_name:
                buf.write_utf_string(friend["name"])

            # Class + Level
            class_id = CLASS_NAME_TO_ID.get(friend.get("className", ""), 0)
            buf._append_bits(class_id, ENTITY_CONST_244)
            buf._append_bits(friend.get("level", 1), MAX_CHAR_LEVEL_BITS)


    # ──────────────(Abilities)──────────────
    learned_abilities = char.get("learnedAbilities", [])
    buf.write_method_6(len(learned_abilities), class_10_const_83)
    for ability in learned_abilities:
        ability_id = ability.get("abilityID", 0)
        rank = ability.get("rank", 0)
        buf.write_method_6(ability_id, class_10_const_83)
        buf.write_method_6(rank, class_10_const_665)

    # ──────────────(activeAbilities)──────────────
    active_slots = char.get("activeAbilities", [0, 0, 0])
    while len(active_slots) < 3:
        active_slots.append(0)
    for slot_id in active_slots[:3]:
        buf.write_method_6(slot_id, class_10_const_83)

    # ──────────────(craftTalentPoints)──────────────
    craft_talent_points = char.get("craftTalentPoints", [0, 0, 0, 0, 0])  # List of 5 values, each 0-15
    packed_value = 0
    for i in range(5):
        packed_value |= (craft_talent_points[i] & 0xF) << (i * 4)
    buf.write_method_4(packed_value)

    # ──────────────(talentPoints)──────────────
    tp_dict = char.get("talentPoints", {})
    # send exactly three 6‑bit values, one per class index 1,2,3
    for class_idx in (1, 2, 3):
        val = tp_dict.get(str(class_idx), 0)
        buf.write_method_6(val, 6)  # 6‑bit field

    # ──────────────(magicForge)──────────────
    mf = char.get("magicForge", {})
    stats_dict = mf.get("stats_by_building", {})
    has_stats = bool(stats_dict)
    buf._append_bits(1 if has_stats else 0, 1)
    if has_stats:
        cls = char.get("class", "").lower()
        seq = CLASS_BUILD_ORDER.get(cls, CLASS_BUILD_ORDER["paladin"])
        # write exactly 7 values in that order:
        for bid in seq:
            val = stats_dict.get(str(bid), 0)
            buf.write_method_6(val, class_9_const_28)

    # 2) Session flag
    has_session = mf.get("hasSession", False)
    buf._append_bits(1 if has_session else 0, 1)

    if has_session:
        # 2a) Primary gem ID
        primary = mf.get("primary", 0)
        buf.write_method_6(primary, class_1_const_254)

        # 2b) In‑progress or completed?
        status = mf.get("status", class_111.const_509)
        if status == class_111.const_286:  # in-progress
            buf._append_bits(1, 1)
            buf.write_method_4(mf.get("ReadyTime", 0))
        else:
            buf._append_bits(0, 1)
            var_8 = mf.get("var_8", 0)
            buf.write_method_6(var_8, class_64_const_499)
            if var_8:
                buf.write_method_6(mf.get("secondary", 0), class_64_const_218)
                buf.write_method_6(mf.get("usedlist", 0), class_111_const_432)

        # 2c) Always send these two when a session exists
        buf.write_method_91(min(mf.get("var_2675", 0), 65535))
        buf.write_method_91(min(mf.get("var_2316", 0), 65535))

    # 3) Final continuation flag (var_2434)
    buf._append_bits(1 if mf.get("var_2434", False) else 0, 1)


    # ──────────────(Skill Research)──────────────
    research = char.get("research")
    if research:
        buf._append_bits(1, 1)
        buf.write_method_6(research["abilityID"], class_10_const_83)

        end_sec = research.get("ReadyTime", 0)

        # If marked done, set time to 0 to signal "ready to collect"
        if research.get("done"):
            buf.write_method_4(0)
        else:
            buf.write_method_4(end_sec)
    else:
        buf._append_bits(0, 1)


    # ──────────────(buildingResearch)──────────────
    bu = char.get("buildingUpgrade")
    if bu and not bu.get("done", False):
        buf._append_bits(1, 1)  # flag: upgrade in progress
        buf.write_method_6(bu["buildingID"], class_9.const_129)  # 5‑bit field
        buf.write_method_4(bu["ReadyTime"])  # 32‑bit (variable) field
    else:
        buf._append_bits(0, 1)


    # ──────────────(towerResearch)──────────────
    tr = char.get("talentResearch", {})
    # present if there's an active or pending research
    has_tr = isinstance(tr, dict) and not tr.get("done", False) and tr.get("ReadyTime", 0) > 0
    buf._append_bits(1 if has_tr else 0, 1)

    if has_tr:
        # write the 2‑bit classIndex (use the same const the client does)
        buf.write_bits(tr.get("classIndex", 0), class_66.const_571)
        # then the 32‑bit ReadyTime
        buf.write_method_4(tr.get("ReadyTime", 0))

    # ──────────────(EggHachery)──────────────
    # “SetEggData” (egg type + reset timer)
    egg_data = char.get("EggHachery")
    if egg_data:
        buf._append_bits(1, 1)  # egg data present
        buf.write_method_6(egg_data["EggID"], class_16_const_167)

        if egg_data.get("done", False):
            # Egg finished — client will show it as ready
            buf.write_method_4(0)
        else:
            # Egg in progress — send remaining time
            buf.write_method_4(egg_data.get("ReadyTime", 0))

    # ──────────────(Owned Eggs)──────────────
    eggPetIDs = char.get("OwnedEggsID", [])
    buf.write_method_6(len(eggPetIDs), class_16_const_167)
    for eid in eggPetIDs:
        buf.write_method_6(eid, class_16_const_167)

    # ──────────────(Active Egg Count)──────────────
    activeEggCount = char.get("activeEggCount", 0)
    buf.write_method_4(activeEggCount)


    # ──────────────(Resting pets)──────────────
    # Resting Pets (3 slots max)
    rest = char.get("restingPets", [])[:3]

    for i in range(3):
        if i < len(rest):
            r = rest[i]
            buf._append_bits(1, 1)
            buf.write_method_6(r["typeID"], class_7_const_19)
            buf.write_method_4(0)  # a value bigger than 0 will cause the pet not to show in the resting slot not sure what the actual function of this so im just going to leave it 0
        else:
            buf._append_bits(0, 1)


    # ──────────────(Training pets)──────────────
    tp_list = char.get("trainingPet", [])
    if tp_list and isinstance(tp_list, list) and len(tp_list) > 0:
        tp = tp_list[0]
        buf._append_bits(1, 1)
        buf.write_method_6(tp["typeID"], class_7_const_19)
        buf.write_method_4(0)  # a value bigger than 0 will cause the pet not to show in the training slot not sure what the actual function of this so im just going to leave it 0
        buf.write_method_4(tp.get("trainingTime", 0))  # extra value
    else:
        buf._append_bits(0, 1)

    # ──────────────(Event News)──────────────
    icon, url, body, tooltip, start_ts = NEWS_EVENTS.get(
        event_index,
        ["", "", "", "", 0]
    )
    buf.write_utf_string(icon)  # a_NewsGoldIcon, etc.
    buf.write_utf_string(url)  # e.g. "http://www.dungeonblitz.com/"
    buf.write_utf_string(body)  # "Double Gold Event"
    buf.write_utf_string(tooltip)  # "While this event is in place ..."
    buf.write_method_4(start_ts)  # Epoch timestamp

    # ──────────────(MasterClass)──────────────
    selected = str(char.get("MasterClass", 0))
    mastery_data = char.get("Mastery", {}).get(selected, {"classID": 0, "slots": []})

    # Write the chosen classID & slots exactly as before:
    buf.write_method_6(mastery_data["classID"], GAME_CONST_209)
    buf._append_bits(1, 1)  # we always send a tree
    for i in range(NUM_TALENT_SLOTS):
        slot = mastery_data["slots"][i] if i < len(mastery_data["slots"]) else {"filled": False}
        if slot["filled"]:
            buf._append_bits(1, 1)  # presence bit

            # === NODE INDEX FIRST ===
            buf.write_method_6(slot["nodeIdx"], CLASS_118_CONST_127)

            # === POINTS-MINUS-ONE SECOND ===
            bits = SLOT_BIT_WIDTHS[i]
            buf.write_method_6(slot["points"] - 1, bits)
        else:
            buf._append_bits(0, 1)


    # ──────────────(Equipped Gears)──────────────
    equip = char.get("equippedGears", [])
    for slot_id in range(1, 7):  # Slots 1 to 6
        gear = equip[slot_id - 1] if slot_id - 1 < len(equip) else {}
        gear_id = gear.get("gearID", 0)
        if gear_id:
            buf._append_bits(1, 1)
            buf.write_method_6(gear_id, GEARTYPE_BITS)
        else:
            buf._append_bits(0, 1)


    # ──────────────(Equipped Mount)──────────────
    equipped = char.get("equippedMount", 0)
    buf.write_method_4(equipped)

    # ──────────────(equippedPetID)──────────────
    pet_type_id = char.get("equippedPetID", 0)
    buf.write_method_4(pet_type_id)
    buf.write_method_4(0)  # Always zero, no iteration data

    # ──────────────(activeConsumableID and queuedConsumableID)──────────────
    active_consumable_id = char.get("activeConsumableID", 0)
    queued_consumable_id = char.get("queuedConsumableID", 0)
    buf.write_method_4(active_consumable_id)
    buf.write_method_4(queued_consumable_id)


    # ──────────────(Guild‐panel data)──────────────
    guild = char.get("guild", None)
    in_guild = guild is not None
    buf._append_bits(1 if in_guild else 0, 1)

    if in_guild:
        buf.write_utf_string(guild["name"])
        buf.write_method_6(guild.get("rank", 0), 3)

        members = guild.get("onlineMembers", [])
        buf.write_method_4(len(members))
        for m in members:
            buf.write_utf_string(m["name"])
            buf.write_method_6(m["classID"], 2)
            buf.write_method_6(m["level"], 6)
            buf.write_method_6(m["status"], 3)

        # your own entry
        buf.write_utf_string(char["name"])
        buf.write_method_6(CLASS_NAME_TO_ID[char["class"]], 2)
        buf.write_method_6(char["level"], 6)
        buf.write_method_6(guild.get("rank", 0), 3)

    payload = buf.to_bytes()
    return struct.pack(">HH", 0x10, len(payload)) + payload


#TODO... all this does is just update the building visuals when the player join the game from a saved account nothing important
# it should be send as a response on (0x1f) packet
def send_building_update(session, char):
    mf_stats = char.get("magicForge", {}).get("stats_by_building", {})

    def _stat(bid):
        return int(mf_stats.get(str(bid), mf_stats.get(bid, 0) or 0))

    master_class_id = int(char.get("MasterClass", 0))
    tower_building_id = MASTERCLASS_TO_BUILDING.get(master_class_id, 3)

    # First building: current tower building type & its level
    first_building_id = tower_building_id
    first_building_level = _stat(tower_building_id)

    # Second building: maybe same as first but with target upgrade level
    second_building_id = tower_building_id
    second_building_level = first_building_level  # Could be higher if upgrading

    scaffolding_id = int(char.get("buildingUpgrade", {}).get("buildingID", 0) or 0)

    buf = BitBuffer()
    buf.write_method_6(first_building_id, class_9_const_129)
    buf.write_method_6(first_building_level, class_9_const_28)
    buf.write_method_6(second_building_id, class_9_const_129)
    buf.write_method_6(second_building_level, class_9_const_28)
    buf.write_method_6(scaffolding_id, class_9_const_129)

    pkt = struct.pack(">HH", 0xDA, len(buf.to_bytes())) + buf.to_bytes()
    session.conn.sendall(pkt)



def build_enter_world_packet(
    transfer_token: int,
    old_level_id: int,
    old_swf: str,
    has_old_coord: bool,
    old_x: int,
    old_y: int,
    host: str,
    port: int,
    new_level_swf: str,
    new_map_lvl: int,
    new_base_lvl: int,
    new_internal: str,
    new_moment: str,
    new_alter: str,
    new_is_inst: bool,
    new_has_coord: bool = False,
    new_x: int = 0,
    new_y: int = 0,
    char: dict = None,
) -> bytes:
    buf = BitBuffer()

    # 1) transferToken (_loc4_)
    buf.write_method_4(transfer_token)

    # 2) oldLevelId (_loc5_)
    buf.write_method_4(old_level_id)

    # 3) old SWF path (_loc6_)
    buf.write_utf_string(old_swf)

    # 4) old coords? + values (_loc8_, _loc2_, _loc3_)
    buf._append_bits(1 if has_old_coord else 0, 1)
    if has_old_coord:
        buf.write_method_4(old_x)
        buf.write_method_4(old_y)

    # 5) host (_loc9_)
    buf.write_utf_string(host)

    # 6) port (_loc10_)
    buf.write_method_4(port)

    # 7) new SWF path (_loc11_)
    buf.write_utf_string(new_level_swf)

    # 8) new_map_lvl, new_base_lvl (_loc12_, _loc13_, 6 bits each)
    buf.write_method_6(new_map_lvl, MAX_CHAR_LEVEL_BITS)
    buf.write_method_6(new_base_lvl, MAX_CHAR_LEVEL_BITS)

    # 9) new strings (_loc14_, _loc15_, _loc16_)
    buf.write_utf_string(new_internal)
    buf.write_utf_string(new_moment)
    buf.write_utf_string(new_alter)

    # 10) new_is_instanced flag (_loc17_)
    buf._append_bits(1 if new_is_inst else 0, 1)

    # 11) spawn-point flag (_loc18_) + coords (_loc20_, _loc21_)
    buf._append_bits(1 if new_has_coord else 0, 1)
    if new_has_coord:
        buf.write_signed_method_45(new_x)
        buf.write_signed_method_45(new_y)

    # --- SPECIAL CASE: only send building data when player loads/visits "CraftTown" ---
    # determine if we are entering CraftTown (case-insensitive)
    _is_crafttown = False
    if new_level_swf and "crafttown" in new_level_swf.lower():
        _is_crafttown = True
    if new_internal and "crafttown" in new_internal.lower():
        _is_crafttown = True

    # 12) Extended data presence (_loc19_) -> only set when CraftTown
    buf._append_bits(1 if _is_crafttown else 0, 1)

    if _is_crafttown:
        # 13) Buildings data block
        # New level ID (_loc22_, same as transfer_token)
        new_level_id = transfer_token
        buf.write_method_4(new_level_id)

        # --- WRITE master class id so the client parses the following fields correctly ---
        master_class_id = int(char.get("MasterClass", 0) if char else 0)
        buf.write_method_6(master_class_id, GAME_CONST_209)

        # Map MasterClass -> building id for tower lookup (ensure MASTERCLASS_TO_BUILDING exists)
        tower_building_id = MASTERCLASS_TO_BUILDING.get(master_class_id, 0)

        # Get building stats from the new save structure
        stats_by_building = {}
        if char:
            mf = char.get("magicForge", {})
            # support both "stats" (old array) and "stats_by_building" (new dict)
            if isinstance(mf, dict):
                stats_by_building = mf.get("stats_by_building", {}) or {}
            else:
                # fallback if mf is provided in unexpected format
                stats_by_building = {}

        stats_by_building = char.get("magicForge", {}).get("stats_by_building", {}) if char else {}

        def _stat(bid):
            return int(stats_by_building.get(str(bid), stats_by_building.get(bid, 0) or 0))

        # Mapping based on provided sample:
        # 1: Tome, 2: Forge, 3..11: Towers, 12: Keep, 13: Barn
        tome_level = _stat(1)   # _loc26_ in some examples; here we treat Tome as id 1
        forge_level = _stat(2)  # forge
        # Tower: choose the tower matching master_class_id if in tower range, fallback to first tower id 3
        stats_by_building = char.get("magicForge", {}).get("stats_by_building", {})
        tower_level = _stat(tower_building_id)
        keep_level = _stat(12)
        barn_level = _stat(13)

        # scaffolding_level: use buildingUpgrade.buildingID if present (0 otherwise)
        scaffolding_level = 0
        if char:
            bu = char.get("buildingUpgrade", {}) or {}
            # if buildingUpgrade contains buildingID -> that is the building currently upgrading
            scaffolding_level = int(bu.get("buildingID", 0) or 0)

        # write building levels using the same bit sizes/constants the client expects
        buf.write_method_6(forge_level, class_9_const_28)
        buf.write_method_6(keep_level, class_9_const_28)
        buf.write_method_6(tower_level, class_9_const_28)
        buf.write_method_6(tome_level, class_9_const_28)
        buf.write_method_6(barn_level, class_9_const_28)
        buf.write_method_6(scaffolding_level, class_9_const_129)

    # Build final packet
    payload = buf.to_bytes()
    return struct.pack(">HH", 0x21, len(payload)) + payload


