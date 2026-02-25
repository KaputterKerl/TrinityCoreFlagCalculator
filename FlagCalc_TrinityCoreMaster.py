import os
import sys

class WoWFlagDecoder:
    def __init__(self):
        # Creature Template Flags
        self.npc_flags = {
            1: "Gossip", 2: "Quest Giver", 16: "Trainer", 32: "Class Trainer",
            64: "Profession Trainer", 128: "Vendor", 256: "Vendor Ammo",
            512: "Vendor Food", 1024: "Vendor Poison", 2048: "Vendor Reagent",
            4096: "Repairer", 8192: "Flight Master", 16384: "Spirit Healer",
            32768: "Spirit Guide", 65536: "Innkeeper", 131072: "Banker",
            262144: "Petitioner", 524288: "Tabard Designer", 1048576: "Battlemaster",
            2097152: "Auctioneer", 4194304: "Stable Master", 8388608: "Guild Banker",
            16777216: "Spellclick", 33554432: "PlayerVehicle", 67108864: "Mailbox"
        }
        
        self.unit_flags = {
            2: "UNIT_FLAG_NON_ATTACKABLE", 8: "UNIT_FLAG_PLAYER_CONTROLLED",
            64: "UNIT_FLAG_UNK_6", 128: "UNIT_FLAG_NOT_ATTACKABLE_1",
            256: "UNIT_FLAG_IMMUNE_TO_PC", 512: "UNIT_FLAG_IMMUNE_TO_NPC",
            1024: "UNIT_FLAG_LOOTING", 2048: "UNIT_FLAG_PET_IN_COMBAT",
            4096: "UNIT_FLAG_PVP_ENABLING", 8192: "UNIT_FLAG_SILENCED",
            16384: "UNIT_FLAG_CANNOT_SWIM", 32768: "UNIT_FLAG_CAN_SWIM",
            65536: "UNIT_FLAG_NON_ATTACKABLE_2", 131072: "UNIT_FLAG_PACIFIED",
            262144: "UNIT_FLAG_STUNNED", 524288: "UNIT_FLAG_IN_COMBAT",
            2097152: "UNIT_FLAG_DISARMED", 4194304: "UNIT_FLAG_CONFUSED",
            8388608: "UNIT_FLAG_FLEEING", 16777216: "UNIT_FLAG_POSSESSED",
            33554432: "UNIT_FLAG_UNINTERACTIBLE", 67108864: "UNIT_FLAG_SKINNABLE",
            134217728: "UNIT_FLAG_MOUNT", 1073741824: "UNIT_FLAG_SHEATHE",
            2147483648: "UNIT_FLAG_IMMUNE"
        }
        
        self.unit_flags2 = {
            1: "UNIT_FLAG2_FEIGN_DEATH", 2: "UNIT_FLAG2_HIDE_BODY",
            4: "UNIT_FLAG2_IGNORE_REPUTATION", 8: "UNIT_FLAG2_COMPREHEND_LANG",
            16: "UNIT_FLAG2_MIRROR_IMAGE", 32: "UNIT_FLAG2_DO_NOT_FADE_IN",
            64: "UNIT_FLAG2_FORCE_MOVEMENT", 128: "UNIT_FLAG2_DISARM_OFFHAND",
            256: "UNIT_FLAG2_DISABLE_PRED_STATS", 1024: "UNIT_FLAG2_DISARM_RANGED",
            2048: "UNIT_FLAG2_REGENERATE_POWER", 4096: "UNIT_FLAG2_RESTRICT_PARTY_INTERACTION",
            8192: "UNIT_FLAG2_PREVENT_SPELL_CLICK", 16384: "UNIT_FLAG2_ALLOW_ENEMY_INTERACT",
            32768: "UNIT_FLAG2_CANNOT_TURN", 131072: "UNIT_FLAG2_PLAY_DEATH_ANIM",
            262144: "UNIT_FLAG2_ALLOW_CHEAT_SPELLS"
        }
        
        self.dynamic_flags = {
            1: "UNIT_DYNFLAG_LOOTABLE", 2: "UNIT_DYNFLAG_TRACK_UNIT",
            4: "UNIT_DYNFLAG_TAPPED", 8: "UNIT_DYNFLAG_TAPPED_BY_PLAYER",
            16: "UNIT_DYNFLAG_SPECIALINFO", 32: "UNIT_DYNFLAG_DEAD",
            64: "UNIT_DYNFLAG_REFER_A_FRIEND", 128: "UNIT_DYNFLAG_TAPPED_BY_ALL_THREAT_LIST"
        }
        
        self.type_flags = {
            1: "CREATURE_TYPE_FLAG_TAMEABLE", 2: "CREATURE_TYPE_FLAG_VISIBLE_TO_GHOSTS",
            4: "CREATURE_TYPE_FLAG_BOSS_MOB", 8: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_WOUND_ANIM",
            16: "CREATURE_TYPE_FLAG_NO_FACTION_TOOLTIP", 32: "CREATURE_TYPE_FLAG_MORE_AUDIBLE",
            64: "CREATURE_TYPE_FLAG_SPELL_ATTACKABLE", 128: "CREATURE_TYPE_FLAG_INTERACT_WHILE_DEAD",
            256: "CREATURE_TYPE_FLAG_SKIN_WITH_HERBALISM", 512: "CREATURE_TYPE_FLAG_SKIN_WITH_MINING",
            1024: "CREATURE_TYPE_FLAG_NO_DEATH_MESSAGE", 2048: "CREATURE_TYPE_FLAG_ALLOW_MOUNTED_COMBAT",
            4096: "CREATURE_TYPE_FLAG_CAN_ASSIST", 8192: "CREATURE_TYPE_FLAG_NO_PET_BAR",
            16384: "CREATURE_TYPE_FLAG_MASK_UID", 32768: "CREATURE_TYPE_FLAG_SKIN_WITH_ENGINEERING",
            65536: "CREATURE_TYPE_FLAG_EXOTIC_PET", 131072: "CREATURE_TYPE_FLAG_USE_MODEL_COLLISION_SIZE",
            262144: "CREATURE_TYPE_FLAG_ALLOW_INTERACTION_WHILE_IN_COMBAT", 524288: "CREATURE_TYPE_FLAG_COLLIDE_WITH_MISSILES",
            1048576: "CREATURE_TYPE_FLAG_NO_NAME_PLATE", 2097152: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_MOUNTED_ANIMATIONS",
            4194304: "CREATURE_TYPE_FLAG_LINK_ALL", 8388608: "CREATURE_TYPE_FLAG_INTERACT_ONLY_WITH_CREATOR",
            16777216: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_UNIT_EVENT_SOUNDS", 33554432: "CREATURE_TYPE_FLAG_HAS_NO_SHADOW_BLOB",
            67108864: "CREATURE_TYPE_FLAG_TREAT_AS_RAID_UNIT", 134217728: "CREATURE_TYPE_FLAG_FORCE_GOSSIP",
            268435456: "CREATURE_TYPE_FLAG_DO_NOT_SHEATHE", 536870912: "CREATURE_TYPE_FLAG_DO_NOT_TARGET_ON_INTERACTION",
            1073741824: "CREATURE_TYPE_FLAG_DO_NOT_RENDER_OBJECT_NAME", 2147483648: "CREATURE_TYPE_FLAG_QUEST_BOSS"
        }
        
        self.flags_extra = {
            1: "CREATURE_FLAG_EXTRA_INSTANCE_BIND", 2: "CREATURE_FLAG_EXTRA_CIVILIAN",
            4: "CREATURE_FLAG_EXTRA_NO_PARRY", 8: "CREATURE_FLAG_EXTRA_NO_PARRY_HASTEN",
            16: "CREATURE_FLAG_EXTRA_NO_BLOCK", 32: "CREATURE_FLAG_EXTRA_NO_CRUSHING_BLOWS",
            64: "CREATURE_FLAG_EXTRA_NO_XP", 128: "CREATURE_FLAG_EXTRA_TRIGGER",
            256: "CREATURE_FLAG_EXTRA_NO_TAUNT", 512: "CREATURE_FLAG_EXTRA_NO_MOVE_FLAGS_UPDATE",
            1024: "CREATURE_FLAG_EXTRA_GHOST_VISIBILITY", 2048: "CREATURE_FLAG_EXTRA_USE_OFFHAND_ATTACK",
            4096: "CREATURE_FLAG_EXTRA_NO_SELL_VENDOR", 8192: "CREATURE_FLAG_EXTRA_IGNORE_COMBAT",
            16384: "CREATURE_FLAG_EXTRA_WORLDEVENT", 32768: "CREATURE_FLAG_EXTRA_GUARD",
            65536: "CREATURE_FLAG_EXTRA_IGNORE_FEIGN_DEATH", 131072: "CREATURE_FLAG_EXTRA_NO_CRIT",
            262144: "CREATURE_FLAG_EXTRA_NO_SKILL_GAINS", 524288: "CREATURE_FLAG_EXTRA_OBEYS_TAUNT_DIMINISHING_RETURNS",
            1048576: "CREATURE_FLAG_EXTRA_ALL_DIMINISH", 2097152: "CREATURE_FLAG_EXTRA_NO_PLAYER_DAMAGE_REQ",
            268435456: "CREATURE_FLAG_EXTRA_DUNGEON_BOSS", 536870912: "CREATURE_FLAG_EXTRA_IGNORE_PATHFINDING",
            1073741824: "CREATURE_FLAG_EXTRA_IMMUNITY_KNOCKBACK"
        }

        # Quest Template Flags
        self.quest_flags = {
            1: "QUEST_FLAGS_STAY_ALIVE",
            2: "QUEST_FLAGS_PARTY_ACCEPT",
            4: "QUEST_FLAGS_EXPLORATION",
            8: "QUEST_FLAGS_SHARABLE",
            16: "QUEST_FLAGS_HAS_CONDITION",
            32: "QUEST_FLAGS_HIDE_REWARD_POI",
            64: "QUEST_FLAGS_RAID",
            128: "QUEST_FLAGS_TBC",
            256: "QUEST_FLAGS_NO_MONEY_FROM_XP",
            512: "QUEST_FLAGS_HIDDEN_REWARDS",
            1024: "QUEST_FLAGS_TRACKING",
            2048: "QUEST_FLAGS_DEPRECATE_REPUTATION",
            4096: "QUEST_FLAGS_DAILY",
            8192: "QUEST_FLAGS_FLAGS_PVP",
            16384: "QUEST_FLAGS_UNAVAILABLE",
            32768: "QUEST_FLAGS_WEEKLY",
            65536: "QUEST_FLAGS_AUTOCOMPLETE",
            131072: "QUEST_FLAGS_DISPLAY_ITEM_IN_TRACKER",
            262144: "QUEST_FLAGS_OBJ_TEXT",
            524288: "QUEST_FLAGS_AUTO_ACCEPT"
        }

        # Item Template Flags
        self.item_flags = {
            1: "ITEM_FLAG_NO_PICKUP",
            2: "ITEM_FLAG_CONJURED",
            4: "ITEM_FLAG_HAS_LOOT",
            8: "ITEM_FLAG_HEROIC_TOOLTIP",
            16: "ITEM_FLAG_DEPRECATED",
            32: "ITEM_FLAG_NO_USER_DESTROY",
            64: "ITEM_FLAG_PLAYERCAST",
            128: "ITEM_FLAG_NO_EQUIP_COOLDOWN",
            256: "ITEM_FLAG_MULTI_LOOT_QUEST",
            512: "ITEM_FLAG_IS_WRAPPER",
            1024: "ITEM_FLAG_USES_RESOURCES",
            2048: "ITEM_FLAG_MULTI_DROP",
            4096: "ITEM_FLAG_ITEM_PURCHASE_RECORD",
            8192: "ITEM_FLAG_PETITION",
            16384: "ITEM_FLAG_HAS_TEXT",
            32768: "ITEM_FLAG_NO_DISENCHANT",
            65536: "ITEM_FLAG_REAL_DURATION",
            131072: "ITEM_FLAG_NO_CREATOR",
            262144: "ITEM_FLAG_IS_PROSPECTABLE",
            524288: "ITEM_FLAG_UNIQUE_EQUIPPABLE",
            1048576: "ITEM_FLAG_IGNORE_FOR_AURAS",
            2097152: "ITEM_FLAG_IGNORE_DEFAULT_ARENA_RESTRICTIONS",
            4194304: "ITEM_FLAG_NO_DURABILITY_LOSS",
            8388608: "ITEM_FLAG_USE_WHEN_SHAPESHIFTED",
            16777216: "ITEM_FLAG_HAS_QUEST_GLOW",
            33554432: "ITEM_FLAG_HIDE_UNUSABLE_RECIPE",
            67108864: "ITEM_FLAG_NOT_USEABLE_IN_ARENA",
            134217728: "ITEM_FLAG_IS_BOUND_TO_ACCOUNT",
            268435456: "ITEM_FLAG_NO_REAGENT_COST",
            536870912: "ITEM_FLAG_IS_MILLABLE",
            1073741824: "ITEM_FLAG_REPORT_TO_GUILD_CHAT",
            2147483648: "ITEM_FLAG_NO_PROGRESSIVE_LOOT"
        }

        self.item_flags2 = {
            1: "ITEM_FLAG2_FACTION_HORDE",
            2: "ITEM_FLAG2_FACTION_ALLIANCE",
            4: "ITEM_FLAG2_DONT_IGNORE_BUY_PRICE",
            8: "ITEM_FLAG2_CLASSIFY_AS_CASTER",
            16: "ITEM_FLAG2_CLASSIFY_AS_PHYSICAL",
            32: "ITEM_FLAG2_EVERYONE_CAN_ROLL_NEED",
            64: "ITEM_FLAG2_NO_TRADE_BIND_ON_ACQUIRE",
            128: "ITEM_FLAG2_CAN_TRADE_BIND_ON_ACQUIRE",
            256: "ITEM_FLAG2_CAN_ONLY_ROLL_GREED",
            512: "ITEM_FLAG2_CASTER_WEAPON",
            1024: "ITEM_FLAG2_DELETE_ON_LOGIN",
            2048: "ITEM_FLAG2_INTERNAL_ITEM",
            4096: "ITEM_FLAG2_NO_VENDOR_VALUE",
            8192: "ITEM_FLAG2_SHOW_BEFORE_DISCOVERED",
            16384: "ITEM_FLAG2_OVERRIDE_GOLD_COST",
            32768: "ITEM_FLAG2_IGNORE_DEFAULT_RATED_BG_RESTRICTIONS",
            65536: "ITEM_FLAG2_NOT_USABLE_IN_RATED_BG",
            131072: "ITEM_FLAG2_BNET_ACCOUNT_TRADE_OK",
            262144: "ITEM_FLAG2_CONFIRM_BEFORE_USE",
            524288: "ITEM_FLAG2_REEVALUATE_BONDING_ON_TRANSFORM",
            1048576: "ITEM_FLAG2_NO_TRANSFORM_ON_CHARGE_DEPLETION",
            2097152: "ITEM_FLAG2_NO_ALTER_ITEM_VISUAL",
            4194304: "ITEM_FLAG2_NO_SOURCE_FOR_ITEM_VISUAL",
            8388608: "ITEM_FLAG2_IGNORE_QUALITY_FOR_ITEM_VISUAL_SOURCE",
            16777216: "ITEM_FLAG2_NO_DURABILITY",
            33554432: "ITEM_FLAG2_ROLE_TANK",
            67108864: "ITEM_FLAG2_ROLE_HEALER",
            134217728: "ITEM_FLAG2_ROLE_DAMAGE",
            268435456: "ITEM_FLAG2_CAN_DROP_IN_CHALLENGE_MODE",
            536870912: "ITEM_FLAG2_NEVER_STACK_IN_LOOT_UI",
            1073741824: "ITEM_FLAG2_DISENCHANT_TO_LOOT_TABLE",
            2147483648: "ITEM_FLAG2_USED_IN_A_TRADESKILL"
        }

        self.item_flags3 = {
            1: "ITEM_FLAG3_UNK1", 2: "ITEM_FLAG3_UNK2", 4: "ITEM_FLAG3_UNK3",
            8: "ITEM_FLAG3_UNK4", 16: "ITEM_FLAG3_UNK5", 32: "ITEM_FLAG3_UNK6",
            64: "ITEM_FLAG3_UNK7", 128: "ITEM_FLAG3_UNK8", 256: "ITEM_FLAG3_UNK9"
        }

        self.item_flags_custom = {
            1: "ITEM_FLAG_CU_DURATION_REAL", 2: "ITEM_FLAG_CU_IGNORE_QUEST_STATUS",
            4: "ITEM_FLAG_CU_FOLLOW_LOOT_RULES", 8: "ITEM_FLAG_CU_PROSPECTABLE",
            16: "ITEM_FLAG_CU_MILLABLE", 32: "ITEM_FLAG_CU_ENGINEERABLE"
        }

        # Für Validierung
        self.max_values = {
            '1': 0xFFFFFFFF,
            '2': 0xFFFFFFFF,
            '3': 0xFFFFFFFF,
            '4': 0xFFFFFFFF,
            '5': 0xFFFFFFFF,
            '6': 0xFFFFFFFF
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def parse_input(self, value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value.startswith(('0x', '0X')):
                return int(value, 16)
            return int(value)
        return int(value)

    def validate_value(self, value, category):
        max_val = self.max_values.get(category, 0xFFFFFFFF)
        if value > max_val:
            return False, f"Value too high! Maximum is {max_val} (0x{max_val:X})"
        if value < 0:
            return False, "Value cannot be negative"
        return True, ""

    def decode_flags(self, bitmask, flag_dict):
        found = []
        bitmask = int(bitmask)
        for flag_value in sorted(flag_dict.keys()):
            if bitmask & flag_value:
                found.append(flag_value)
        return found

    def show_flags_table(self, flags, flag_dict, title, input_value):
        print(f"\n{title}")
        print(f"Input: {input_value}")
        print("=" * 80)
        
        if flags:
            print(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
            print("-" * 80)
            
            for value in flags:
                name = flag_dict.get(value, f"UNKNOWN ({value})")
                print(f"{value:>12,}\t0x{value:<10X} {name}")
            
            print("-" * 80)
            print(f"{'List:':>12}\t{', '.join(map(str, flags))}")
            print()
            print(f"{'Count:':>12}\t{len(flags)} flag(s)")
        else:
            print("No flags set (0)")

    def show_all_flags_table(self):
        flag_sets = [
            ("NPC FLAGS", self.npc_flags),
            ("UNIT_FLAGS", self.unit_flags),
            ("UNIT_FLAGS2", self.unit_flags2),
            ("DYNAMICFLAGS", self.dynamic_flags),
            ("TYPE_FLAGS", self.type_flags),
            ("FLAGS_EXTRA", self.flags_extra),
            ("QUEST_FLAGS", self.quest_flags),
            ("ITEM_FLAGS", self.item_flags),
            ("ITEM_FLAGS2", self.item_flags2),
            ("ITEM_FLAGS3", self.item_flags3),
            ("ITEM_FLAGS_CUSTOM", self.item_flags_custom)
        ]
        
        all_output = []
        for title, flag_dict in flag_sets:
            all_output.append(f"\n{title}:")
            all_output.append("=" * 80)
            all_output.append(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
            all_output.append("-" * 80)
            
            for value in sorted(flag_dict.keys()):
                all_output.append(f"{value:>12,}\t0x{value:<10X} {flag_dict[value]}")
        
        self.clear_screen()
        print("\n".join(all_output))
        self.wait_for_key()

    def show_creature_menu(self):
        while True:
            self.clear_screen()
            print("Creature Template Flags")
            print("-" * 30)
            print("1 - NPC Flags")
            print("2 - Unit Flags")
            print("3 - Unit Flags 2")
            print("4 - Dynamic Flags")
            print("5 - Type Flags")
            print("6 - Extra Flags")
            print("s - Show all creature flags (reference)")
            print("b - Back to main menu")
            print("q - Quit program")
            
            try:
                choice = input("\nSelect (1-6, s, b, q): ").strip().lower()
                
                if choice == 'q':
                    return 'quit'
                if choice == 'b':
                    return
                if choice == 's':
                    flag_sets = [
                        ("NPC FLAGS", self.npc_flags),
                        ("UNIT_FLAGS", self.unit_flags),
                        ("UNIT_FLAGS2", self.unit_flags2),
                        ("DYNAMICFLAGS", self.dynamic_flags),
                        ("TYPE_FLAGS", self.type_flags),
                        ("FLAGS_EXTRA", self.flags_extra)
                    ]
                    
                    all_output = []
                    for title, flag_dict in flag_sets:
                        all_output.append(f"\n{title}:")
                        all_output.append("=" * 80)
                        all_output.append(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
                        all_output.append("-" * 80)
                        
                        for value in sorted(flag_dict.keys()):
                            all_output.append(f"{value:>12,}\t0x{value:<10X} {flag_dict[value]}")
                    
                    self.clear_screen()
                    print("\n".join(all_output))
                    self.wait_for_key()
                    continue
                
                if choice not in ['1', '2', '3', '4', '5', '6']:
                    print("Invalid choice. Use 1-6, s, b, or q")
                    self.wait_for_key()
                    continue
                
                commands = {
                    '1': ('NPC FLAGS', self.npc_flags),
                    '2': ('UNIT_FLAGS', self.unit_flags),
                    '3': ('UNIT_FLAGS2', self.unit_flags2),
                    '4': ('DYNAMICFLAGS', self.dynamic_flags),
                    '5': ('TYPE_FLAGS', self.type_flags),
                    '6': ('FLAGS_EXTRA', self.flags_extra)
                }
                
                self.clear_screen()
                title, flag_dict = commands[choice]
                print(f"Selected: {title}")
                print("-" * 30)
                
                value_str = input("Enter bitmask (decimal or hex like 0x83): ").strip()
                if not value_str:
                    continue
                    
                try:
                    value = self.parse_input(value_str)
                    
                    is_valid, error_msg = self.validate_value(value, choice)
                    if not is_valid:
                        print(f"\nError: {error_msg}")
                        self.wait_for_key()
                        continue
                    
                    flags = self.decode_flags(value, flag_dict)
                    
                    self.clear_screen()
                    self.show_flags_table(flags, flag_dict, title, value_str)
                    self.wait_for_key()
                    
                except ValueError:
                    print("\nError: Invalid number format. Use decimal (123) or hex (0x7B)")
                    self.wait_for_key()
                except OverflowError:
                    print("\nError: Number too large")
                    self.wait_for_key()
                    
            except KeyboardInterrupt:
                return 'quit'

    def show_quest_menu(self):
        while True:
            self.clear_screen()
            print("Quest Template Flags")
            print("-" * 30)
            print("1 - Quest Flags")
            print("s - Show all quest flags (reference)")
            print("b - Back to main menu")
            print("q - Quit program")
            
            try:
                choice = input("\nSelect (1, s, b, q): ").strip().lower()
                
                if choice == 'q':
                    return 'quit'
                if choice == 'b':
                    return
                if choice == 's':
                    self.clear_screen()
                    print("\nQUEST FLAGS:")
                    print("=" * 80)
                    print(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
                    print("-" * 80)
                    
                    for value in sorted(self.quest_flags.keys()):
                        print(f"{value:>12,}\t0x{value:<10X} {self.quest_flags[value]}")
                    
                    self.wait_for_key()
                    continue
                
                if choice != '1':
                    print("Invalid choice. Use 1, s, b, or q")
                    self.wait_for_key()
                    continue
                
                self.clear_screen()
                print("Selected: QUEST FLAGS")
                print("-" * 30)
                
                value_str = input("Enter bitmask (decimal or hex like 0x83): ").strip()
                if not value_str:
                    continue
                    
                try:
                    value = self.parse_input(value_str)
                    flags = self.decode_flags(value, self.quest_flags)
                    
                    self.clear_screen()
                    self.show_flags_table(flags, self.quest_flags, "QUEST FLAGS", value_str)
                    self.wait_for_key()
                    
                except ValueError:
                    print("\nError: Invalid number format. Use decimal (123) or hex (0x7B)")
                    self.wait_for_key()
                except OverflowError:
                    print("\nError: Number too large")
                    self.wait_for_key()
                    
            except KeyboardInterrupt:
                return 'quit'

    def show_item_menu(self):
        while True:
            self.clear_screen()
            print("Item Template Flags")
            print("-" * 30)
            print("1 - Item Flags")
            print("2 - Item Flags 2")
            print("3 - Item Flags 3")
            print("4 - Item Flags Custom")
            print("s - Show all item flags (reference)")
            print("b - Back to main menu")
            print("q - Quit program")
            
            try:
                choice = input("\nSelect (1-4, s, b, q): ").strip().lower()
                
                if choice == 'q':
                    return 'quit'
                if choice == 'b':
                    return
                if choice == 's':
                    flag_sets = [
                        ("ITEM FLAGS", self.item_flags),
                        ("ITEM FLAGS 2", self.item_flags2),
                        ("ITEM FLAGS 3", self.item_flags3),
                        ("ITEM FLAGS CUSTOM", self.item_flags_custom)
                    ]
                    
                    all_output = []
                    for title, flag_dict in flag_sets:
                        all_output.append(f"\n{title}:")
                        all_output.append("=" * 80)
                        all_output.append(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
                        all_output.append("-" * 80)
                        
                        for value in sorted(flag_dict.keys()):
                            all_output.append(f"{value:>12,}\t0x{value:<10X} {flag_dict[value]}")
                    
                    self.clear_screen()
                    print("\n".join(all_output))
                    self.wait_for_key()
                    continue
                
                if choice not in ['1', '2', '3', '4']:
                    print("Invalid choice. Use 1-4, s, b, or q")
                    self.wait_for_key()
                    continue
                
                commands = {
                    '1': ('ITEM FLAGS', self.item_flags),
                    '2': ('ITEM FLAGS 2', self.item_flags2),
                    '3': ('ITEM FLAGS 3', self.item_flags3),
                    '4': ('ITEM FLAGS CUSTOM', self.item_flags_custom)
                }
                
                self.clear_screen()
                title, flag_dict = commands[choice]
                print(f"Selected: {title}")
                print("-" * 30)
                
                value_str = input("Enter bitmask (decimal or hex like 0x83): ").strip()
                if not value_str:
                    continue
                    
                try:
                    value = self.parse_input(value_str)
                    flags = self.decode_flags(value, flag_dict)
                    
                    self.clear_screen()
                    self.show_flags_table(flags, flag_dict, title, value_str)
                    self.wait_for_key()
                    
                except ValueError:
                    print("\nError: Invalid number format. Use decimal (123) or hex (0x7B)")
                    self.wait_for_key()
                except OverflowError:
                    print("\nError: Number too large")
                    self.wait_for_key()
                    
            except KeyboardInterrupt:
                return 'quit'

    def wait_for_key(self):
        input("\nPress any key to continue...")

def main():
    decoder = WoWFlagDecoder()
    
    while True:
        decoder.clear_screen()
        print("WoW Flag Decoder - Main Menu")
        print("=" * 30)
        print("1 - Creature Template")
        print("2 - Quest Template")
        print("3 - Item Template")
        print("s - Show all flags (reference)")
        print("q - Quit")
        print("-" * 30)
        
        try:
            choice = input("\nSelect (1-3, s, q): ").strip().lower()
            
            if choice == 'q':
                decoder.clear_screen()
                print("Goodbye!")
                break
            
            if choice == 's':
                decoder.show_all_flags_table()
                continue
            
            if choice == '1':
                result = decoder.show_creature_menu()
                if result == 'quit':
                    break
            elif choice == '2':
                result = decoder.show_quest_menu()
                if result == 'quit':
                    break
            elif choice == '3':
                result = decoder.show_item_menu()
                if result == 'quit':
                    break
            else:
                print("Invalid choice. Use 1-3, s, or q")
                decoder.wait_for_key()
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()