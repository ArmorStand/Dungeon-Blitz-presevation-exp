# Pet Related Packets
#===================================
const_1262 = 0xF0 # PKTTYPE_PET_HATCH_OR_TRAIN
const_1134 = 0x37 # PKTTYPE_RECEIVE_NEW_PET
const_849 = 0xe4 # PKTTYPE_REQUEST_EGG_UPDATE
const_1081 = 0xef # PKTTYPE_PET_TRAINING_COMPLETE
const_1036 = 0xed  # PKTTYPE_CANCEL_PET_TRAINING - Cancels the pet training process
const_981 = 0xE5 # PKTTYPE_EGG_PET_UPDATE
const_1104 = 0xf2  # PKTTYPE_PET_EXPERIENCE_UPDATE
const_877 = 0xe8  # PKTTYPE_EGG_HATCH_CANCEL - Sent by the client to cancel an egg hatching process
const_939 = 0xe7  # PKTTYPE_EGG_HATCH_START - Sent by the server to notify the client that a new pet egg has started hatching
const_1114 = 0xec  # PKTTYPE_PET_TRAIN_START - Sent by the client to start training a pet
const_947 = 0xe6  # PKTTYPE_BARN_HATCH_OR_TRAIN - Client sends this when the player clicks to hatch a new egg or train a pet; payload includes egg ID/type for hatching, boolean flag for action type.
const_1190 = 0xE9  # PKTTYPE_PET_EGG_SPEEDUP - Client requests to accelerate egg hatching using Mammoth Idols (consumes idols based on remaining hatch time).
const_962 = 0xee  # PKTTYPE_PET_TRAINING_COMPLETE - Notifies the client that a pet has finished training; triggers a notification and updates pet training status.
const_709 = 0xb2  # PKTTYPE_MOUNT_EQUIP - Notifies the client to equip a specific mount for a given entity, or sent by the client to equip a mount for the player.
const_1209 = 0xb3  # PKTTYPE_PET_INFO_UPDATE - Sent by the client to update the server with the current active pet and resting pets, including their type IDs and unique instance IDs.
const_978 = 0xea  # PKTTYPE_PET_TRAINING_COMPLETE - Sent by the client to notify the server that the player's pet training or egg incubation has finished and the results should be applied.
const_1001 = 0xff  # PKTTYPE_NEW_HATCHERY_EGGS - Server notifies the client that new eggs are ready in the Hatchery
#===================================

# Inventory and Currency Related Packets
#===================================
const_1266 = 0x104 # PKTTYPE_UPDATE_LOCKBOX_INVENTORY
const_1023 = 0x10f # PKTTYPE_SPEND_ROYAL_SIGILS
const_1201 = 0x10c  # updates players consumables inventory when a  consumable is used
const_1028 = 0xb5  # updates players MammothIdols
const_1157 = 0xA1 # PKTTYPE_PREMIUM_CURRENCY_UPDATE
const_1219 = 0x106  # PKTTYPE_BUY_ROYAL_SIGIL_STORE
const_1115 = 0x105  # PKTTYPE_BUY_LOCKBOX_KEYS - Client requests to buy Lockbox/Dragon keys
const_1235 = 0xb4  # PKTTYPE_MONEY_LOSS - Server notifies client that the player lost gold
const_1303 = 0x10b  # PKTTYPE_CONSUMABLE_GAIN - Server notifies the client that the player has obtained consumable items; includes item ID, stack count, and whether to suppress pickup notification.
const_898 = 0x112  # PKTTYPE_ROYAL_SIGIL_REWARD - Server grants the player Royal Sigils (lockbox currency); updates total and caches amount earned.
const_1164 = 0x114  # PKTTYPE_LOCKBOX_OPEN - Client request sent to server when the player attempts to open a lockbox; includes lockbox ID and selected option index.
const_1289 = 0x107  # PKTTYPE_OPEN_LOCKBOX - Sent by the client to notify the server that the player is opening a lockbox, consuming one lockbox and one key. The server then processes rewards and updates the player's inventory accordingly.
const_884 = 0x108  # PKTTYPE_LOCKBOX_CONTENT - Sent by the server to the client to provide information about a specific lockbox's contents. Includes the lockbox type, item IDs, and optionally a custom name or description. The client then updates the lockbox UI accordingly.
PKTTYPE_RECEIVE_GOLD = 0x35
PKTTYPE_RECEIVE_GEAR = 0x33
PKTTYPE_RECEIVE_LOOTDROP = 0x32
PKTTYPE_RECEIVE_REWARD = 0x2b
const_1010 = 0x34  # PKTTYPE_MATERIAL_PICKUP - Server notifies the client that the player has acquired materials; client updates inventory and optionally shows a notification.
const_956 = 0x36  # PKTTYPE_GAIN_MOUNT - Server notifies client that the player has obtained a new mount; includes mount ID and a flag for whether to suppress notification.
const_1182 = 0x109  # PKTTYPE_GAIN_CHARM - Server notifies the client that the player gained a charm or respec stone; payload includes encoded charm ID and quantity/flags.
#===================================

# Combat and Health Related Packets
#===================================
const_1271 = 0x3b # PKTTYPE_ENTITY_HEAL
const_1142 = 0xf7 # PKTTYPE_RECALC_HEALTH
const_969 = 0xfc # PKTTYPE_SEND_COMBAT_STATS
const_1037 = 0xF9 # PKTTYPE_REQUEST_CLIENT_HP
const_1099 = 0xF6 # PKTTYPE_CLIENT_HP_REPORT
const_958 = 0x100  # PKTTYPE_CHAR_REGEN - Server packet sent when a character regenerates health; includes entity ID and amount of HP restored.
const_252 = 0x10d  # PKTTYPE_QUEUE_POTION - Notifies the client that a potion/consumable has been queued for use by a specific entity; triggers updating the next active potion.
const_909 = 0x10e # PKTTYPE_QUEUE_POTION
const_1255 = 0xfb  # PKTTYPE_SYNC_PLAYER_STATS - Server requests the client to resend its current melee, magic, and max HP stats; used to synchronize player stats between client and server.
PKTTYPE_SERVER_ADJUST_HP = 0x3a
PKTTYPE_ENT_DESTROY = 0xd
PKTTYPE_BUFF_TICK_DOT = 0x79
PKTTYPE_REQUEST_RESPAWN = 0x77
PKTTYPE_ENT_POWER_HIT = 0xa
PKTTYPE_PROJECTILE_EXPLODE = 0xe
PKTTYPE_ENT_ADD_BUFF = 0xb
PKTTYPE_ENT_REMOVE_BUFF = 0xc
PKTTYPE_RESPAWN_COMPLETE = 0x80
PKTTYPE_CHAR_REGEN = 0x78
const_743 = 0x82  # PKTTYPE_REVIVE - Sent by the server to the client to indicate that a player/entity has been revived
const_760 = 0x8a # PKTTYPE_UPDATE_SPEED - Sent by the server to update an entity's movement speed
const_1127 = 0xbb  # PKTTYPE_REPORT_MAX_HP_CHANGE - Client informs the server that the player's maximum HP has changed, so the server can adjust stats or apply over-heal corrections
const_1300 = 0xcb  # PKTTYPE_POWER_USE_START - Sent by the client to the server when a player begins using a power that consumes mana
const_1239 = 0xcc  # PKTTYPE_HOTBAR_ABILITY_SWITCH - Client notifies the server that the player switched active abilities; payload is empty, server infers new state from current hotbar.
PKTTYPE_GRANT_REWARD = 0x2a
#===================================

# Room and Zone Related Packets
#===================================
const_805 = 0xAC # PKTTYPE_ROOM_BOSS_INFO
const_683 = 0xA5 # PKTTYPE_ROOM_EVENT_START
const_648 = 0xA9 # PKTTYPE_ROOM_STATE_UPDATE
const_762 = 0xa6  # PKTTYPE_ROOM_CLOSE / ROOM_RESET
const_823 = 0xad  # PKTTYPE_ROOM_UNLOCK - Notifies client that a room is now unlocked or accessible
const_788 = 0xAB  # PKTTYPE_ROOM_INFO_UPDATE - Updates room state: player count, room name, capacity, and owner name.
const_996 = 0xf4  # PKTTYPE_ZONE_ENTER - Client notifies server that the player has entered a new zone/room
const_1158 = 0xDA # PKTTYPE_ROOM_SCAFFOLDING_UPDATE
const_694 = 0xC2 # PKTTYPE_FLAMETHROWER_ROR_TRIGGER
const_1256 = 0x96  # PKTTYPE_ZONE_PLAYERS_UPDATE - Server sends the client the list of players currently in the same zone/area; client updates the Zone panel with this information.
const_1302 = 0x95  # PKTTYPE_ZONE_PANEL_REQUEST - Client requests the current players in the same zone/area
#===================================

# Entity Update Related Packets
#===================================
const_928 = 0xF1 # PKTTYPE_PLAYER_EQUIPMENT_UPDATE
const_1061 = 0xaf  # PKTTYPE_ENT_GEAR_UPDATE - Updates an entity's equipped gear (armor, weapons, accessories) on the client
const_1126 = 0x88  # PKTTYPE_SET_ENTITY_LEVELS - Server notifies the client of the new level for entities; client updates maxHP and related stats for all entities accordingly.
const_691 = 0xae  # PKTTYPE_SET_UNTARGETABLE
PKTTYPE_CHANGE_OFFSET_Y = 0x7d
PKTTYPE_ENT_INCREMENTAL_UPDATE = 0x7
const_1090 = 0xa2 # PKTTYPE_CLIENT_SYNC - Sent by the client to the server to synchronize the player's position, movement state, and tick timing
PKTTYPE_ENT_POWER_CAST = 0x9
PKTTYPE_ENT_FULL_UPDATE = 0x8
PKTTYPE_NEWLY_RELEVANT_ENTITY = 0xf
const_1152 = 0x8e # PKTTYPE_WRITE_CHANGE_LOOK - when the user changes his looks at the mirror
const_1175 = 0xba # PKTTYPE_APPLY_DYE - when the user dyes his gear or shirt/pants
const_941 = 0x8f # PKTTYPE_SEND_UPDATED_LOOK needs to be send by the server to update the players visuals  when PKTTYPE_WRITE_CHANGE_LOOK is received by the server
const_1041 = 0x111 # PKTTYPE_UPDATE_DYE - Sent by the server to the client to update an entity's equipped gear and shirt/pants
#===================================

# Mission and Level Related Packets
#===================================
const_990 = 0x86  # PKTTYPE_COMPLETE_MISSION - Marks a mission as complete
const_1031 = 0x89 # PKTTYPE_UPDATE_BONUS_LEVELS
PKTTYPE_MISSION_ADDED = 0x85
PKTTYPE_MISSION_COMPLETE = 0x84
PKTTYPE_LEVEL_STATE = 0x40
PKTTYPE_SET_LEVEL_COMPLETE = 0x3f
PKTTYPE_MISSION_PROGRESS = 0x83
PKTTYPE_CHANGE_LEVEL = 0x39
PKTTYPE_RECV_LEVEL_COMPLETE = 0x87
const_791 = 0xB7 # PKTTYPE_QUEST_PROGRESS_UPDATE
#===================================

# Emote and Sound Related Packets
#===================================
const_808 = 0xA7 # PKTTYPE_EMOTE
const_716 = 0xa8  # PKTTYPE_PLAY_SOUND - Plays a sound in the client's current room
PKTTYPE_EMOTE_BEGIN = 0x7e
PKTTYPE_EMOTE_END = 0x7f
#===================================

# Player Interaction Related Packets
#===================================
const_1197 = 0xF3 # PKTTYPE_REQUEST_VISIT_PLAYER_HOUSE
const_1020 = 0x6A # PKTTYPE_REQUEST_JOIN_PARTY
const_1161 = 0x8D # PKTTYPE_BADGE_INTERACT
const_1211 = 0x10A # PKTTYPE_DYE_UNLOCK
const_874 = 0x8b  # PKTTYPE_SEND_MAP_POSITION
const_617 = 0xaa  # PKTTYPE_ACTION_UPDATE - Server notifies client of a player action/input (jump, fire, drop, etc.) in a room
const_1171 = 0xa3  # PKTTYPE_ACTIVE_FIRE_HEARTBEAT - Sent periodically while player is firing/using abilities
const_1014 = 0xbc  # PKTTYPE_SAVE_KEYBINDS - Client sends updated keybinding configuration to the server; payload includes whether defaults are used and all custom keybind mappings.
const_905 = 0x3C # PKTTYPE_START_SKIT
const_1065 = 0x7b  # PKTTYPE_INTERACT_SKIT - Server tells the client that an entity should start a skit/dialogue; payload contains entity ID and optional skit ID to play.
PKTTYPE_TALK_TO_NPC = 0x7a
PKTTYPE_QUERYMESSAGE_QUESTION = 0x58
PKTTYPE_QUERYMESSAGE_ANSWER = 0x59
PKTTYPE_QUERYMESSAGE_INTERPRET = 0x5a
PKTTYPE_PICKUP_LOOTDROP = 0x38
#===================================

# Gear and Equipment Related Packets
#===================================
const_1280 = 0xF5 # PKTTYPE_LEVEL_GEAR_LIST - populates the Armory with the Gear that the player owns
const_773 = 0xb0  # PKTTYPE_EQUIP_RUNNES Send by the client when runnes are added to a weapon
const_1029 = 0x31 # PKTTYPE_EQUIP_GEAR - send by the client
PKTTYPE_UPDATE_EQUIPMENT = 0x30
#===================================

# Talent and Skill Related Packets
#===================================
const_1089 = 0xd2 # PKTTYPE_RESPEC_TALENT_TREE
const_987 = 0xd6
const_1284 = 0xe0
const_1044 = 0xd4
const_1220 = 0xdf
const_1047 = 0xd3
const_878 = 0xd9
const_920 = 0xd5
const_929 = 0xbd
const_1077 = 0xbe
const_1205 = 0xd1
const_1129 = 0xdd
const_1111 = 0xde
const_966 = 0xbf
const_1133 = 0xc0
#===================================

# Forge Related Packets
#===================================
const_889 = 0xe2
const_1273 = 0xd0
const_937 = 0xb1
const_1192 = 0xe1
const_789 = 0x110
const_1153 = 0xcd
const_1105 = 0xcf  # PKTTYPE_MAGIC_FORGE_REROLL - Client requests the server to reroll the currently crafting Magic Forge item
#===================================

# Gear Set Related Packets
#===================================
const_976 = 0xc8
const_843 = 0xc7
const_893 = 0xc6
#===================================

# Buildings Upgrade Packets
#===================================
const_1032 = 0xdb
const_1187 = 0xdc
const_861 = 0xd7
const_838 = 0xd8
const_1027 = 0xe3
#===================================

# Master Class Related Packets
#===================================
const_767 = 0xc3
const_1137 = 0xc1
#===================================

# Login Screen Related Packets
#===================================
PKTTYPE_LOGIN_VERSION = 0x11
PKTTYPE_LOGIN_CHALLENGE = 0x12
PKTTYPE_LOGIN_CREATE = 0x13
PKTTYPE_LOGIN_CHARACTER_LIST = 0x15
PKTTYPE_LOGIN_AUTHENTICATE = 0x14
PKTTYPE_LOGIN_CHARACTER_SELECT = 0x16
PKTTYPE_LOGIN_CHARACTER_CREATE = 0x17
PKTTYPE_LOGIN_FAILURE = 0x1b
const_1263 = 0x1a
const_840 = 0x19
const_897 = 0xb6  # PKTTYPE_MAX_CHARACTERS - Server tells client the maximum number of characters (login slots) the account is allowed.
#===================================

# Enter Game World / Level Transfer Related Packets
#===================================
const_945 = 0x21
PKTTYPE_WELCOME = 0x10
PKTTYPE_GAMESERVER_LOGIN = 0x1f
PKTTYPE_TRANSFER_READY = 0x1d
PKTTYPE_OPEN_DOOR = 0x2d
PKTTYPE_DOOR_TARGET = 0x2e
PKTTYPE_REQUEST_DOOR_STATE = 0x41
PKTTYPE_DOOR_STATE = 0x42
#===================================

# Standalone and Developer Mode Related Packets
#===================================
PKTTYPE_GAME_TO_MASTER_END_LEVEL = 0x25
PKTTYPE_MASTER_CLIENT = 0x1e
PKTTYPE_GAME_TO_MASTER_START_LEVEL = 0x24
PKTTYPE_GAME_TO_MASTER_PORT = 0x23
#===================================

# Social Related Packets
#===================================
PKTTYPE_FRIEND_REMOVED = 0x93
PKTTYPE_CHAT_MESSAGE = 0x2c
PKTTYPE_ROOM_THOUGHT = 0x76
PKTTYPE_RECV_CHAT_PRIVATE = 0x47
PKTTYPE_CHAT_STATUS = 0x44 # Gray chat text
PKTTYPE_SEND_CHAT_OFFICER = 0x61
PKTTYPE_SEND_CHAT_PRIVATE = 0x46
PKTTYPE_RECV_CHAT_OFFICER = 0x62
const_1141 = 0x3d # Gray chat text
const_985 = 0x102 # Admin chat Announcement # yellow color
const_839 = 0x81  # PKTTYPE_STATUS_TEXT_UNSAFE - Server sends a raw/unfiltered status message to the client (possibly containing unsafe or special formatting); displayed directly in the chat window.
const_1183 = 0x48  # PKTTYPE_SEND_WHISPER - Server notifies client of a private message (whisper) from another player
const_616 = 0x90 # PKTTYPES_SEND_FRIEND_REQUEST
const_610 = 0x91 # PKTTYPES_UNFRIEND - client sends request to remove player from the friend list
const_913 = 0xc9 # PKTTYPE_REQUEST_FRIEND_LIST
const_1178 = 0xca  # PKTTYPE_FRIENDLIST_UPDATE - Server sends the full friend list and updates friend statuses
const_1298 = 0x92  # PKTTYPE_FRIEND_UPDATE - Sent by the server when a friend’s status changes (online/offline, friend request, accepted, etc.)
const_901 = 0x98 # PKTTYPE_FRIEND_LOGGED_OFF
const_1039 = 0x43 # PKTTYPE_CHAT_IGNORE - sends a request to the server to ignore a player
const_1165 = 0x9d  # PKTTYPE_PLAYER_IGNORE_RECEIVE - received by the server when the player has been ignored
const_1052 = 0x9e  # PKTTYPE_IGNORE_LIST_REQUEST - Sent by the client to request the current list of ignored players from the server
const_1241 = 0x9f  # PKTTYPE_IGNORE_LIST_UPDATE - Server sends the client the current list of ignored players, which the client then displays in the ignore panel.
const_1229 = 0x9c  # PKTTYPE_IGNORE_REMOVE - Server confirms a player has been removed from your ignore list
const_451 = 0xc5
#===================================

# Guild Related Packets
#===================================
PKTTYPE_CMD_GUILD_DEMOTE = 0x52
PKTTYPE_CMD_GUILD_QUIT = 0x54
PKTTYPE_GUILD_UPDATE = 0x56
PKTTYPE_RECV_CHAT_GUILD = 0x60
PKTTYPE_CMD_GUILD_LEADER = 0x53
PKTTYPE_CMD_GUILD_DISBAND = 0x4e
PKTTYPE_CMD_GUILD_INVITE = 0x4f
PKTTYPE_CMD_GUILD_KICK = 0x50
PKTTYPE_CLEAR_GUILDCACHE = 0x55
PKTTYPE_CMD_GUILD_CREATE = 0x4d
PKTTYPE_GUILD_REFRESH_MEMBERSHIP = 0x57
PKTTYPE_CMD_GUILD_PROMOTE = 0x51
PKTTYPE_SEND_CHAT_GUILD = 0x5f
PKTTYPE_ONLINE_USER_GUILD_STATUS = 0x5d
const_1008 = 0x9a  # PKTTYPE_GUILD_MEMBER_JOINED - Server notifies the client that a new player has joined the guild; client updates the guild member list and shows a chat notification.
const_1260 = 0x99  # PKTTYPE_GUILD_RANK_CHANGE - Notifies the client of a guild member's promotion, demotion, or leadership change; updates rank display and chat notifications.
const_1112 = 0x9b  # PKTTYPE_GUILD_MEMBER_LEFT - Notifies the client when a guild member leaves or is kicked
const_879 = 0x97  # PKTTYPE_GUILD_MEMBER_ONLINE - Sent by the server when a guild member logs in to notify the client
#===================================

# Party Related Packets
#===================================
PKTTYPE_CMD_GROUP_INVITE = 0x65
PKTTYPE_GROUP_UPDATE = 0x75
PKTTYPE_TOLOGIN_GROUP_INVITE = 0x6c
PKTTYPE_SEND_CHAT_GROUP = 0x63
PKTTYPE_CMD_GROUP_LEADER = 0x68
PKTTYPE_TOLOGIN_GROUP_REMOVE = 0x6e
PKTTYPE_CMD_GROUP_KICK = 0x67
PKTTYPE_TOLOGIN_GROUP_LEADER = 0x6f
PKTTYPE_TOLOGIN_GROUP_ADD = 0x6d
PKTTYPE_CMD_GROUP_LEAVE = 0x66
PKTTYPE_RECV_CHAT_GROUP = 0x64
const_876 = 0x8c  # PKTTYPE_PARTY_UPDATE (likely)
const_1276 = 0x6b # PKTTYPE_TELEPORT_TO_PLAYER
#===================================

# Miscellaneous Packets
#===================================
const_894 = 0x3e  # PKTTYPE_TRADE_MODE_ENABLE - Server notifies the client that transfer/trade mode has been enabled
PKTTYPE_CLIENT_ERROR = 0x7c # client crash Reports
const_975 = 0xfa # PKTTYPE_UPDATE_CYCLE
const_924 = 0xA4 # PKTTYPE_HEARTBEAT
const_707 = 0x69 # PKTTYPE_LOCK/UNLOCK Command
const_1295 = 0x103  # PKTTYPE_NEWS_UPDATE
const_1214 = 0x101  # PKTTYPE_SERVER_MAINT_WARNING
const_1208 = 0xC4 # PKTTYPE_SESSION_STATS
const_1272 = 0x113 # Alert State update
const_900 = 0xf8 # PKTTYPE_UPDATE_COMBAT_STATS - Sent by the client to the server to update the entity's current combat stats, including health, gear bonuses, and magic-related calculations.
#===================================

# Unused or Legacy Packets
#===================================
PKTTYPE_TRANSFER_BEGIN = 0x1c
PKTTYPE_GAME_TO_LOGIN_USER_TRANSFER = 0x2f
PKTTYPE_GAME_TO_LOGIN_READY = 0x26
PKTTYPE_RELAY_TO_CHARNAME = 0x4a
PKTTYPE_RELAY_PACKET_SENDTOCLIENT = 0x4c
PKTTYPE_RELAY_TO_CHARID = 0x49
PKTTYPE_GAME_TO_LOGIN_USER_LEFT = 0x28
PKTTYPE_GAME_TO_LOGIN_USER_JOINED = 0x27
PKTTYPE_RELAY_PACKET_PROCESS = 0x4b
PKTTYPE_LOGIN_TO_GAME_NOTIFY_OFFLINE = 0x5c
PKTTYPE_LOGIN_TO_GAME_NOTIFY_ONLINE = 0x5b
PKTTYPE_LOGIN_TO_GAME_LOAD_LEVEL = 0x20
PKTTYPE_LOGIN_TO_GAME_KICK_USER = 0x45
PKTTYPE_GAME_TO_LOGIN_MAP_CLOSED = 0x29
const_1397 = 0x70
const_1395 = 0xfe
const_1377 = 0x5e
const_1321 = 0x22
const_1378 = 0xfd
const_1329 = 0x72
const_1306 = 0x74
const_1347 = 0x73
const_1348 = 0xa0
const_1368 = 0x94
const_1369 = 0xeb
const_1353 = 0xb8
const_1337 = 0x71
const_1358 = 0xb9
const_1415 = 0xce
const_933 = 0x18
#===================================