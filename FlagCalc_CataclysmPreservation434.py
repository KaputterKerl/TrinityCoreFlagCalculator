import os
import sys

class WoWFlagDecoder:
    def __init__(self):
        # Flag tables, generated from the flag enums of
        # The-Cataclysm-Preservation-Project/TrinityCore branch master
        self.tbl_npcflags = {
            1: "Gossip", 2: "Questgiver",
            4: "Unk1", 8: "Unk2",
            16: "Trainer", 32: "Trainer Class",
            64: "Trainer Profession", 128: "Vendor",
            256: "Vendor Ammo", 512: "Vendor Food",
            1024: "Vendor Poison", 2048: "Vendor Reagent",
            4096: "Repair", 8192: "Flightmaster",
            16384: "Spirithealer", 32768: "Spiritguide",
            65536: "Innkeeper", 131072: "Banker",
            262144: "Petitioner", 524288: "Tabarddesigner",
            1048576: "Battlemaster", 2097152: "Auctioneer",
            4194304: "Stablemaster", 8388608: "Guild Banker",
            16777216: "Spellclick", 33554432: "Player Vehicle",
            67108864: "Mailbox", 134217728: "Reforger",
            268435456: "Transmogrifier", 536870912: "Vaultkeeper"
        }

        self.tbl_unitflags = {
            1: "UNIT_FLAG_SERVER_CONTROLLED", 2: "UNIT_FLAG_NON_ATTACKABLE",
            4: "UNIT_FLAG_REMOVE_CLIENT_CONTROL", 8: "UNIT_FLAG_PLAYER_CONTROLLED",
            16: "UNIT_FLAG_RENAME", 32: "UNIT_FLAG_PREPARATION",
            64: "UNIT_FLAG_UNK_6", 128: "UNIT_FLAG_NOT_ATTACKABLE_1",
            256: "UNIT_FLAG_IMMUNE_TO_PC", 512: "UNIT_FLAG_IMMUNE_TO_NPC",
            1024: "UNIT_FLAG_LOOTING", 2048: "UNIT_FLAG_PET_IN_COMBAT",
            4096: "UNIT_FLAG_PVP_ENABLING", 8192: "UNIT_FLAG_SILENCED",
            16384: "UNIT_FLAG_CANT_SWIM", 32768: "UNIT_FLAG_CAN_SWIM",
            65536: "UNIT_FLAG_NON_ATTACKABLE_2", 131072: "UNIT_FLAG_PACIFIED",
            262144: "UNIT_FLAG_STUNNED", 524288: "UNIT_FLAG_IN_COMBAT",
            1048576: "UNIT_FLAG_ON_TAXI", 2097152: "UNIT_FLAG_DISARMED",
            4194304: "UNIT_FLAG_CONFUSED", 8388608: "UNIT_FLAG_FLEEING",
            16777216: "UNIT_FLAG_POSSESSED", 33554432: "UNIT_FLAG_NOT_SELECTABLE",
            67108864: "UNIT_FLAG_SKINNABLE", 134217728: "UNIT_FLAG_MOUNT",
            268435456: "UNIT_FLAG_UNK_28", 536870912: "UNIT_FLAG_PREVENT_EMOTES_FROM_CHAT_TEXT",
            1073741824: "UNIT_FLAG_SHEATHE", 2147483648: "UNIT_FLAG_IMMUNE"
        }

        self.tbl_unitflags2 = {
            1: "UNIT_FLAG2_FEIGN_DEATH", 2: "UNIT_FLAG2_HIDE_BODY",
            4: "UNIT_FLAG2_IGNORE_REPUTATION", 8: "UNIT_FLAG2_COMPREHEND_LANG",
            16: "UNIT_FLAG2_MIRROR_IMAGE", 32: "UNIT_FLAG2_DONT_FADE_IN",
            64: "UNIT_FLAG2_FORCE_MOVEMENT", 128: "UNIT_FLAG2_DISARM_OFFHAND",
            256: "UNIT_FLAG2_DISABLE_PRED_STATS", 512: "UNIT_FLAG2_ALLOW_CHANGING_TALENTS",
            1024: "UNIT_FLAG2_DISARM_RANGED", 2048: "UNIT_FLAG2_REGENERATE_POWER",
            4096: "UNIT_FLAG2_RESTRICT_PARTY_INTERACTION", 8192: "UNIT_FLAG2_PREVENT_SPELL_CLICK",
            16384: "UNIT_FLAG2_INTERACT_WHILE_HOSTILE", 32768: "UNIT_FLAG2_CANNOT_TURN",
            65536: "UNIT_FLAG2_UNK2", 131072: "UNIT_FLAG2_PLAY_DEATH_ANIM",
            262144: "UNIT_FLAG2_ALLOW_CHEAT_SPELLS", 524288: "UNIT_FLAG2_SUPPRESS_HIGHLIGHT_WHEN_TARGETED_OR_MOUSED_OVER",
            1048576: "UNIT_FLAG2_TREAT_AS_RAID_UNIT_FOR_HELPFUL_SPELLS", 2097152: "UNIT_FLAG2_LARGE_AOI",
            4194304: "UNIT_FLAG2_GIGANTIC_AOI", 8388608: "UNIT_FLAG2_NO_ACTIONS",
            16777216: "UNIT_FLAG2_AI_WILL_ONLY_SWIM_IF_TARGET_SWIMS", 33554432: "UNIT_FLAG2_DONT_GENERATE_COMBAT_LOG_WHEN_ENGAGED_WITH_NPCS",
            67108864: "UNIT_FLAG2_UNTARGETABLE_BY_CLIENT", 134217728: "UNIT_FLAG2_ATTACKER_IGNORES_MINIMUM_RANGES",
            268435456: "UNIT_FLAG2_UNINTERACTIBLE_IF_HOSTILE", 536870912: "UNIT_FLAG2_UNUSED_11",
            1073741824: "UNIT_FLAG2_INFINITE_AOI", 2147483648: "UNIT_FLAG2_UNUSED_13"
        }

        self.tbl_unitdynflags = {
            1: "UNIT_DYNFLAG_LOOTABLE", 2: "UNIT_DYNFLAG_TRACK_UNIT",
            4: "UNIT_DYNFLAG_TAPPED", 8: "UNIT_DYNFLAG_TAPPED_BY_PLAYER",
            16: "UNIT_DYNFLAG_SPECIALINFO", 32: "UNIT_DYNFLAG_DEAD",
            64: "UNIT_DYNFLAG_REFER_A_FRIEND", 128: "UNIT_DYNFLAG_TAPPED_BY_ALL_THREAT_LIST"
        }

        self.tbl_creaturetypeflags = {
            1: "CREATURE_TYPE_FLAG_TAMEABLE_PET", 2: "CREATURE_TYPE_FLAG_GHOST_VISIBLE",
            4: "CREATURE_TYPE_FLAG_BOSS_MOB", 8: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_WOUND_PARRY_ANIMATION",
            16: "CREATURE_TYPE_FLAG_HIDE_FACTION_TOOLTIP", 32: "CREATURE_TYPEFLAGS_UNK5",
            64: "CREATURE_TYPE_FLAG_SPELL_ATTACKABLE", 128: "CREATURE_TYPE_FLAG_CAN_INTERACT_WHILE_DEAD",
            256: "CREATURE_TYPE_FLAG_HERB_SKINNING_SKILL", 512: "CREATURE_TYPE_FLAG_MINING_SKINNING_SKILL",
            1024: "CREATURE_TYPE_FLAG_DO_NOT_LOG_DEATH", 2048: "CREATURE_TYPE_FLAG_MOUNTED_COMBAT_ALLOWED",
            4096: "CREATURE_TYPE_FLAG_CAN_ASSIST", 8192: "CREATURE_TYPE_FLAG_IS_PET_BAR_USED",
            16384: "CREATURE_TYPE_FLAG_MASK_UID", 32768: "CREATURE_TYPE_FLAG_ENGINEERING_SKINNING_SKILL",
            65536: "CREATURE_TYPE_FLAG_EXOTIC_PET", 131072: "CREATURE_TYPE_FLAG_USE_DEFAULT_COLLISION_BOX",
            262144: "CREATURE_TYPE_FLAG_IS_SIEGE_WEAPON", 524288: "CREATURE_TYPE_FLAG_CAN_COLLIDE_WITH_MISSILES",
            1048576: "CREATURE_TYPE_FLAG_HIDE_NAME_PLATE", 2097152: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_MOUNTED_ANIMATIONS",
            4194304: "CREATURE_TYPE_FLAG_IS_LINK_ALL", 8388608: "CREATURE_TYPE_FLAG_INTERACT_ONLY_WITH_CREATOR",
            16777216: "CREATURE_TYPE_FLAG_DO_NOT_PLAY_UNIT_EVENT_SOUNDS", 33554432: "CREATURE_TYPE_FLAG_HAS_NO_SHADOW_BLOB",
            67108864: "CREATURE_TYPE_FLAG_TREAT_AS_RAID_UNIT", 134217728: "CREATURE_TYPE_FLAG_FORCE_GOSSIP",
            268435456: "CREATURE_TYPE_FLAG_DO_NOT_SHEATHE", 536870912: "CREATURE_TYPE_FLAG_DO_NOT_TARGET_ON_INTERACTION",
            1073741824: "CREATURE_TYPE_FLAG_DO_NOT_RENDER_OBJECT_NAME", 2147483648: "CREATURE_TYPE_FLAG_UNIT_IS_QUEST_BOSS"
        }

        self.tbl_creaturetypeflags2 = {
            1: "CREATURE_TYPEFLAGS_2_UNK1", 2: "CREATURE_TYPEFLAGS_2_UNK2",
            4: "CREATURE_TYPEFLAGS_2_UNK3", 8: "CREATURE_TYPEFLAGS_2_UNK4",
            16: "CREATURE_TYPEFLAGS_2_UNK5", 32: "CREATURE_TYPEFLAGS_2_UNK6",
            64: "CREATURE_TYPEFLAGS_2_UNK7", 128: "CREATURE_TYPEFLAGS_2_UNK8"
        }

        self.tbl_creatureflagsextra = {
            1: "CREATURE_FLAG_EXTRA_INSTANCE_BIND", 2: "CREATURE_FLAG_EXTRA_CIVILIAN",
            4: "CREATURE_FLAG_EXTRA_NO_PARRY", 8: "CREATURE_FLAG_EXTRA_NO_PARRY_HASTEN",
            16: "CREATURE_FLAG_EXTRA_NO_BLOCK", 32: "CREATURE_FLAG_EXTRA_NO_CRUSH",
            64: "CREATURE_FLAG_EXTRA_NO_XP_AT_KILL", 128: "CREATURE_FLAG_EXTRA_TRIGGER",
            256: "CREATURE_FLAG_EXTRA_NO_TAUNT", 512: "CREATURE_FLAG_EXTRA_UNUSED_9",
            1024: "CREATURE_FLAG_EXTRA_GHOST_VISIBILITY", 2048: "CREATURE_FLAG_EXTRA_USE_OFFHAND_ATTACK",
            4096: "CREATURE_FLAG_EXTRA_NO_SELL_VENDOR", 8192: "CREATURE_FLAG_EXTRA_UNUSED_13",
            16384: "CREATURE_FLAG_EXTRA_WORLDEVENT", 32768: "CREATURE_FLAG_EXTRA_GUARD",
            65536: "CREATURE_FLAG_EXTRA_IGNORE_FEIGN_DEATH", 131072: "CREATURE_FLAG_EXTRA_NO_CRIT",
            262144: "CREATURE_FLAG_EXTRA_NO_SKILLGAIN", 524288: "CREATURE_FLAG_EXTRA_TAUNT_DIMINISH",
            1048576: "CREATURE_FLAG_EXTRA_ALL_DIMINISH", 2097152: "CREATURE_FLAG_EXTRA_NO_PLAYER_DAMAGE_REQ",
            4194304: "CREATURE_FLAG_EXTRA_UNUSED_22", 8388608: "CREATURE_FLAG_EXTRA_UNUSED_23",
            16777216: "CREATURE_FLAG_EXTRA_UNUSED_24", 33554432: "CREATURE_FLAG_EXTRA_UNUSED_25",
            67108864: "CREATURE_FLAG_EXTRA_UNUSED_26", 134217728: "CREATURE_FLAG_EXTRA_UNUSED_27",
            268435456: "CREATURE_FLAG_EXTRA_DUNGEON_BOSS", 536870912: "CREATURE_FLAG_EXTRA_IGNORE_PATHFINDING",
            1073741824: "CREATURE_FLAG_EXTRA_IMMUNITY_KNOCKBACK", 2147483648: "CREATURE_FLAG_EXTRA_UNUSED_31"
        }

        self.tbl_creaturestaticflags = {
            1: "CREATURE_STATIC_FLAG_MOUNTABLE", 2: "CREATURE_STATIC_FLAG_NO_XP",
            4: "CREATURE_STATIC_FLAG_NO_LOOT", 8: "CREATURE_STATIC_FLAG_UNKILLABLE",
            16: "CREATURE_STATIC_FLAG_TAMEABLE", 32: "CREATURE_STATIC_FLAG_IMMUNE_TO_PC",
            64: "CREATURE_STATIC_FLAG_IMMUNE_TO_NPC", 128: "CREATURE_STATIC_FLAG_CAN_WIELD_LOOT",
            256: "CREATURE_STATIC_FLAG_SESSILE", 512: "CREATURE_STATIC_FLAG_UNINTERACTIBLE",
            1024: "CREATURE_STATIC_FLAG_NO_AUTOMATIC_REGEN", 2048: "CREATURE_STATIC_FLAG_DESPAWN_INSTANTLY",
            4096: "CREATURE_STATIC_FLAG_CORPSE_RAID", 8192: "CREATURE_STATIC_FLAG_CREATOR_LOOT",
            16384: "CREATURE_STATIC_FLAG_NO_DEFENSE", 32768: "CREATURE_STATIC_FLAG_NO_SPELL_DEFENSE",
            65536: "CREATURE_STATIC_FLAG_BOSS_MOB", 131072: "CREATURE_STATIC_FLAG_COMBAT_PING",
            262144: "CREATURE_STATIC_FLAG_AQUATIC", 524288: "CREATURE_STATIC_FLAG_AMPHIBIOUS",
            1048576: "CREATURE_STATIC_FLAG_NO_MELEE", 2097152: "CREATURE_STATIC_FLAG_VISIBLE_TO_GHOSTS",
            4194304: "CREATURE_STATIC_FLAG_PVP_ENABLING", 8388608: "CREATURE_STATIC_FLAG_DO_NOT_PLAY_WOUND_ANIM",
            16777216: "CREATURE_STATIC_FLAG_NO_FACTION_TOOLTIP", 33554432: "CREATURE_STATIC_FLAG_IGNORE_COMBAT",
            67108864: "CREATURE_STATIC_FLAG_ONLY_ATTACK_PVP_ENABLING", 134217728: "CREATURE_STATIC_FLAG_CALLS_GUARDS",
            268435456: "CREATURE_STATIC_FLAG_CAN_SWIM", 536870912: "CREATURE_STATIC_FLAG_FLOATING",
            1073741824: "CREATURE_STATIC_FLAG_MORE_AUDIBLE", 2147483648: "CREATURE_STATIC_FLAG_LARGE_AOI"
        }

        self.tbl_creaturestaticflags2 = {
            1: "CREATURE_STATIC_FLAG_2_NO_PET_SCALING", 2: "CREATURE_STATIC_FLAG_2_FORCE_PARTY_MEMBERS_INTO_COMBAT",
            4: "CREATURE_STATIC_FLAG_2_LOCK_TAPPERS_TO_RAID_ON_DEATH", 8: "CREATURE_STATIC_FLAG_2_SPELL_ATTACKABLE",
            16: "CREATURE_STATIC_FLAG_2_NO_CRUSHING_BLOWS", 32: "CREATURE_STATIC_FLAG_2_NO_OWNER_THREAT",
            64: "CREATURE_STATIC_FLAG_2_NO_WOUNDED_SLOWDOWN", 128: "CREATURE_STATIC_FLAG_2_USE_CREATOR_BONUSES",
            256: "CREATURE_STATIC_FLAG_2_IGNORE_FEIGN_DEATH", 512: "CREATURE_STATIC_FLAG_2_IGNORE_SANCTUARY",
            1024: "CREATURE_STATIC_FLAG_2_ACTION_TRIGGERS_WHILE_CHARMED", 2048: "CREATURE_STATIC_FLAG_2_INTERACT_WHILE_DEAD",
            4096: "CREATURE_STATIC_FLAG_2_NO_INTERRUPT_SCHOOL_COOLDOWN", 8192: "CREATURE_STATIC_FLAG_2_RETURN_SOUL_SHARD_TO_MASTER_OF_PET",
            16384: "CREATURE_STATIC_FLAG_2_SKIN_WITH_HERBALISM", 32768: "CREATURE_STATIC_FLAG_2_SKIN_WITH_MINING",
            65536: "CREATURE_STATIC_FLAG_2_ALERT_CONTENT_TEAM_ON_DEATH", 131072: "CREATURE_STATIC_FLAG_2_ALERT_CONTENT_TEAM_AT_90_PCT_HP",
            262144: "CREATURE_STATIC_FLAG_2_ALLOW_MOUNTED_COMBAT", 524288: "CREATURE_STATIC_FLAG_2_PVP_ENABLING_OOC",
            1048576: "CREATURE_STATIC_FLAG_2_NO_DEATH_MESSAGE", 2097152: "CREATURE_STATIC_FLAG_2_IGNORE_PATHING_FAILURE",
            4194304: "CREATURE_STATIC_FLAG_2_FULL_SPELL_LIST", 8388608: "CREATURE_STATIC_FLAG_2_DOES_NOT_REDUCE_REPUTATION_FOR_RAIDS",
            16777216: "CREATURE_STATIC_FLAG_2_IGNORE_MISDIRECTION", 33554432: "CREATURE_STATIC_FLAG_2_HIDE_BODY",
            67108864: "CREATURE_STATIC_FLAG_2_SPAWN_DEFENSIVE", 134217728: "CREATURE_STATIC_FLAG_2_SERVER_ONLY",
            268435456: "CREATURE_STATIC_FLAG_2_CAN_SAFE_FALL", 536870912: "CREATURE_STATIC_FLAG_2_CAN_ASSIST",
            1073741824: "CREATURE_STATIC_FLAG_2_NO_SKILL_GAINS", 2147483648: "CREATURE_STATIC_FLAG_2_NO_PET_BAR"
        }

        self.tbl_creaturestaticflags3 = {
            1: "CREATURE_STATIC_FLAG_3_NO_DAMAGE_HISTORY", 2: "CREATURE_STATIC_FLAG_3_DONT_PVP_ENABLE_OWNER",
            4: "CREATURE_STATIC_FLAG_3_DO_NOT_FADE_IN", 8: "CREATURE_STATIC_FLAG_3_MASK_UID",
            16: "CREATURE_STATIC_FLAG_3_SKIN_WITH_ENGINEERING", 32: "CREATURE_STATIC_FLAG_3_NO_AGGRO_ON_LEASH",
            64: "CREATURE_STATIC_FLAG_3_NO_FRIENDLY_AREA_AURAS", 128: "CREATURE_STATIC_FLAG_3_EXTENDED_CORPSE_DURATION",
            256: "CREATURE_STATIC_FLAG_3_CANNOT_SWIM", 512: "CREATURE_STATIC_FLAG_3_TAMEABLE_EXOTIC",
            1024: "CREATURE_STATIC_FLAG_3_GIGANTIC_AOI", 2048: "CREATURE_STATIC_FLAG_3_INFINITE_AOI",
            4096: "CREATURE_STATIC_FLAG_3_CANNOT_PENETRATE_WATER", 8192: "CREATURE_STATIC_FLAG_3_NO_NAME_PLATE",
            16384: "CREATURE_STATIC_FLAG_3_CHECKS_LIQUIDS", 32768: "CREATURE_STATIC_FLAG_3_NO_THREAT_FEEDBACK",
            65536: "CREATURE_STATIC_FLAG_3_USE_MODEL_COLLISION_SIZE", 131072: "CREATURE_STATIC_FLAG_3_ATTACKER_IGNORES_FACING",
            262144: "CREATURE_STATIC_FLAG_3_ALLOW_INTERACTION_WHILE_IN_COMBAT", 524288: "CREATURE_STATIC_FLAG_3_SPELL_CLICK_FOR_PARTY_ONLY",
            1048576: "CREATURE_STATIC_FLAG_3_FACTION_LEADER", 2097152: "CREATURE_STATIC_FLAG_3_IMMUNE_TO_PLAYER_BUFFS",
            4194304: "CREATURE_STATIC_FLAG_3_COLLIDE_WITH_MISSILES", 8388608: "CREATURE_STATIC_FLAG_3_CAN_BE_MULTITAPPED",
            16777216: "CREATURE_STATIC_FLAG_3_DO_NOT_PLAY_MOUNTED_ANIMATIONS", 33554432: "CREATURE_STATIC_FLAG_3_CANNOT_TURN",
            67108864: "CREATURE_STATIC_FLAG_3_ENEMY_CHECK_IGNORES_LOS", 134217728: "CREATURE_STATIC_FLAG_3_FOREVER_CORPSE_DURATION",
            268435456: "CREATURE_STATIC_FLAG_3_PETS_ATTACK_WITH_3D_PATHING", 536870912: "CREATURE_STATIC_FLAG_3_LINK_ALL",
            1073741824: "CREATURE_STATIC_FLAG_3_AI_CAN_AUTO_TAKEOFF_IN_COMBAT", 2147483648: "CREATURE_STATIC_FLAG_3_AI_CAN_AUTO_LAND_IN_COMBAT"
        }

        self.tbl_creaturestaticflags4 = {
            1: "CREATURE_STATIC_FLAG_4_NO_BIRTH_ANIM", 2: "CREATURE_STATIC_FLAG_4_TREAT_AS_PLAYER_FOR_DIMINISHING_RETURNS",
            4: "CREATURE_STATIC_FLAG_4_TREAT_AS_PLAYER_FOR_PVP_DEBUFF_DURATION", 8: "CREATURE_STATIC_FLAG_4_INTERACT_ONLY_WITH_CREATOR",
            16: "CREATURE_STATIC_FLAG_4_DO_NOT_PLAY_UNIT_EVENT_SOUNDS", 32: "CREATURE_STATIC_FLAG_4_HAS_NO_SHADOW_BLOB",
            64: "CREATURE_STATIC_FLAG_4_DEALS_TRIPLE_DAMAGE_TO_PC_CONTROLLED_PETS", 128: "CREATURE_STATIC_FLAG_4_NO_NPC_DAMAGE_BELOW_85PTC",
            256: "CREATURE_STATIC_FLAG_4_OBEYS_TAUNT_DIMINISHING_RETURNS", 512: "CREATURE_STATIC_FLAG_4_NO_MELEE_APPROACH",
            1024: "CREATURE_STATIC_FLAG_4_UPDATE_CREATURE_RECORD_WHEN_INSTANCE_CHANGES_DIFFICULTY", 2048: "CREATURE_STATIC_FLAG_4_CANNOT_DAZE",
            4096: "CREATURE_STATIC_FLAG_4_FLAT_HONOR_AWARD", 8192: "CREATURE_STATIC_FLAG_4_IGNORE_LOS_WHEN_CASTING_ON_ME",
            16384: "CREATURE_STATIC_FLAG_4_GIVE_QUEST_KILL_CREDIT_WHILE_OFFLINE", 32768: "CREATURE_STATIC_FLAG_4_TREAT_AS_RAID_UNIT_FOR_HELPFUL_SPELLS",
            65536: "CREATURE_STATIC_FLAG_4_DONT_REPOSITION_IF_MELEE_TARGET_IS_TOO_CLOSE", 131072: "CREATURE_STATIC_FLAG_4_PET_OR_GUARDIAN_AI_DONT_GO_BEHIND_TARGET",
            262144: "CREATURE_STATIC_FLAG_4_5_MINUTE_LOOT_ROLL_TIMER", 524288: "CREATURE_STATIC_FLAG_4_FORCE_GOSSIP",
            1048576: "CREATURE_STATIC_FLAG_4_DONT_REPOSITION_WITH_FRIENDS_IN_COMBAT", 2097152: "CREATURE_STATIC_FLAG_4_DO_NOT_SHEATHE",
            4194304: "CREATURE_STATIC_FLAG_4_IGNORE_SPELL_MIN_RANGE_RESTRICTIONS", 8388608: "CREATURE_STATIC_FLAG_4_SUPPRESS_INSTANCE_WIDE_RELEASE_IN_COMBAT",
            16777216: "CREATURE_STATIC_FLAG_4_PREVENT_SWIM", 33554432: "CREATURE_STATIC_FLAG_4_HIDE_IN_COMBAT_LOG",
            67108864: "CREATURE_STATIC_FLAG_4_ALLOW_NPC_COMBAT_WHILE_UNINTERACTIBLE", 134217728: "CREATURE_STATIC_FLAG_4_PREFER_NPCS_WHEN_SEARCHING_FOR_ENEMIES",
            268435456: "CREATURE_STATIC_FLAG_4_ONLY_GENERATE_INITIAL_THREAT", 536870912: "CREATURE_STATIC_FLAG_4_DO_NOT_TARGET_ON_INTERACTION",
            1073741824: "CREATURE_STATIC_FLAG_4_DO_NOT_RENDER_OBJECT_NAME", 2147483648: "CREATURE_STATIC_FLAG_4_QUEST_BOSS"
        }

        self.tbl_creaturestaticflags5 = {
            1: "CREATURE_STATIC_FLAG_5_UNTARGETABLE_BY_CLIENT", 2: "CREATURE_STATIC_FLAG_5_FORCE_SELF_MOUNTING",
            4: "CREATURE_STATIC_FLAG_5_UNINTERACTIBLE_IF_HOSTILE", 8: "CREATURE_STATIC_FLAG_5_DISABLES_XP_AWARD",
            16: "CREATURE_STATIC_FLAG_5_DISABLE_AI_PREDICTION", 32: "CREATURE_STATIC_FLAG_5_NO_LEAVECOMBAT_STATE_RESTORE",
            64: "CREATURE_STATIC_FLAG_5_BYPASS_INTERACT_INTERRUPTS", 128: "CREATURE_STATIC_FLAG_5_240_DEGREE_BACK_ARC",
            256: "CREATURE_STATIC_FLAG_5_INTERACT_WHILE_HOSTILE", 512: "CREATURE_STATIC_FLAG_5_DONT_DISMISS_ON_FLYING_MOUNT",
            1024: "CREATURE_STATIC_FLAG_5_PREDICTIVE_POWER_REGEN", 2048: "CREATURE_STATIC_FLAG_5_HIDE_LEVEL_INFO_IN_TOOLTIP",
            4096: "CREATURE_STATIC_FLAG_5_HIDE_HEALTH_BAR_UNDER_TOOLTIP", 8192: "CREATURE_STATIC_FLAG_5_SUPPRESS_HIGHLIGHT_WHEN_TARGETED_OR_MOUSED_OVER",
            16384: "CREATURE_STATIC_FLAG_5_AI_PREFER_PATHABLE_TARGETS", 32768: "CREATURE_STATIC_FLAG_5_FREQUENT_AREA_TRIGGER_CHECKS",
            65536: "CREATURE_STATIC_FLAG_5_ASSIGN_KILL_CREDIT_TO_ENCOUNTER_LIST", 131072: "CREATURE_STATIC_FLAG_5_NEVER_EVADE",
            262144: "CREATURE_STATIC_FLAG_5_AI_CANT_PATH_ON_STEEP_SLOPES", 524288: "CREATURE_STATIC_FLAG_5_AI_IGNORE_LOS_TO_MELEE_TARGET",
            1048576: "CREATURE_STATIC_FLAG_5_NO_TEXT_IN_CHAT_BUBBLE", 2097152: "CREATURE_STATIC_FLAG_5_CLOSE_IN_ON_UNPATHABLE_TARGET",
            4194304: "CREATURE_STATIC_FLAG_5_DONT_GO_BEHIND_ME", 8388608: "CREATURE_STATIC_FLAG_5_NO_DEATH_THUD",
            16777216: "CREATURE_STATIC_FLAG_5_CLIENT_LOCAL_CREATURE", 33554432: "CREATURE_STATIC_FLAG_5_CAN_DROP_LOOT_WHILE_IN_A_CHALLENGE_MODE_INSTANCE",
            67108864: "CREATURE_STATIC_FLAG_5_HAS_SAFE_LOCATION", 134217728: "CREATURE_STATIC_FLAG_5_NO_HEALTH_REGEN",
            268435456: "CREATURE_STATIC_FLAG_5_NO_POWER_REGEN", 536870912: "CREATURE_STATIC_FLAG_5_NO_PET_UNIT_FRAME",
            1073741824: "CREATURE_STATIC_FLAG_5_NO_INTERACT_ON_LEFT_CLICK", 2147483648: "CREATURE_STATIC_FLAG_5_GIVE_CRITERIA_KILL_CREDIT_WHEN_CHARMED"
        }

        self.tbl_questflags = {
            1: "QUEST_FLAGS_COMPLETION_NO_DEATH", 2: "QUEST_FLAGS_COMPLETION_EVENT",
            4: "QUEST_FLAGS_COMPLETION_AREA_TRIGGER", 8: "QUEST_FLAGS_SHARABLE",
            16: "QUEST_FLAGS_HAS_CONDITION", 32: "QUEST_FLAGS_HIDE_REWARD_POI",
            64: "QUEST_FLAGS_RAID_GROUP_OK", 128: "QUEST_FLAGS_EXPANSION_ONLY",
            256: "QUEST_FLAGS_NO_MONEY_FOR_XP", 512: "QUEST_FLAGS_HIDE_REWARD",
            1024: "QUEST_FLAGS_TRACKING_EVENT", 2048: "QUEST_FLAGS_DEPRECATE_REPUTATION",
            4096: "QUEST_FLAGS_DAILY", 8192: "QUEST_FLAGS_FLAGS_PVP",
            16384: "QUEST_FLAGS_DEPRECATED", 32768: "QUEST_FLAGS_WEEKLY",
            65536: "QUEST_FLAGS_AUTO_COMPLETE", 131072: "QUEST_FLAGS_DISPLAY_ITEM_IN_TRACKER",
            262144: "QUEST_FLAGS_DISABLE_COMPLETION_TEXT", 524288: "QUEST_FLAGS_AUTO_ACCEPT",
            1048576: "QUEST_FLAGS_PLAYER_CAST_ACCEPT", 2097152: "QUEST_FLAGS_PLAYER_CAST_COMPLETE",
            4194304: "QUEST_FLAGS_UPDATE_PHASESHIFT", 8388608: "QUEST_FLAGS_SOR_WHITELIST",
            16777216: "QUEST_FLAGS_LAUNCH_GOSSIP_COMPLETE", 33554432: "QUEST_FLAGS_REMOVE_SURPLUS_ITEMS",
            67108864: "QUEST_FLAGS_WELL_KNOWN", 134217728: "QUEST_FLAGS_PORTRAIT_IN_QUEST_LOG",
            268435456: "QUEST_FLAGS_SHOW_ITEM_WHEN_COMPLETED", 536870912: "QUEST_FLAGS_LAUNCH_GOSSIP_ACCEPT",
            1073741824: "QUEST_FLAGS_ITEMS_GLOW_WHEN_COMPLETE", 2147483648: "QUEST_FLAGS_FAIL_ON_LOGOUT"
        }

        self.tbl_itemflags = {
            1: "ITEM_FLAG_NO_PICKUP", 2: "ITEM_FLAG_CONJURED",
            4: "ITEM_FLAG_HAS_LOOT", 8: "ITEM_FLAG_HEROIC_TOOLTIP",
            16: "ITEM_FLAG_DEPRECATED", 32: "ITEM_FLAG_NO_USER_DESTROY",
            64: "ITEM_FLAG_PLAYERCAST", 128: "ITEM_FLAG_NO_EQUIP_COOLDOWN",
            256: "ITEM_FLAG_MULTI_LOOT_QUEST", 512: "ITEM_FLAG_IS_WRAPPER",
            1024: "ITEM_FLAG_USES_RESOURCES", 2048: "ITEM_FLAG_MULTI_DROP",
            4096: "ITEM_FLAG_ITEM_PURCHASE_RECORD", 8192: "ITEM_FLAG_PETITION",
            16384: "ITEM_FLAG_HAS_TEXT", 32768: "ITEM_FLAG_NO_DISENCHANT",
            65536: "ITEM_FLAG_REAL_DURATION", 131072: "ITEM_FLAG_NO_CREATOR",
            262144: "ITEM_FLAG_IS_PROSPECTABLE", 524288: "ITEM_FLAG_UNIQUE_EQUIPPABLE",
            1048576: "ITEM_FLAG_IGNORE_FOR_AURAS", 2097152: "ITEM_FLAG_IGNORE_DEFAULT_ARENA_RESTRICTIONS",
            4194304: "ITEM_FLAG_NO_DURABILITY_LOSS", 8388608: "ITEM_FLAG_USE_WHEN_SHAPESHIFTED",
            16777216: "ITEM_FLAG_HAS_QUEST_GLOW", 33554432: "ITEM_FLAG_HIDE_UNUSABLE_RECIPE",
            67108864: "ITEM_FLAG_NOT_USEABLE_IN_ARENA", 134217728: "ITEM_FLAG_IS_BOUND_TO_ACCOUNT",
            268435456: "ITEM_FLAG_NO_REAGENT_COST", 536870912: "ITEM_FLAG_IS_MILLABLE",
            1073741824: "ITEM_FLAG_REPORT_TO_GUILD_CHAT", 2147483648: "ITEM_FLAG_NO_PROGRESSIVE_LOOT"
        }

        self.tbl_itemflags2 = {
            1: "ITEM_FLAG2_FACTION_HORDE", 2: "ITEM_FLAG2_FACTION_ALLIANCE",
            4: "ITEM_FLAG2_DONT_IGNORE_BUY_PRICE", 8: "ITEM_FLAG2_CLASSIFY_AS_CASTER",
            16: "ITEM_FLAG2_CLASSIFY_AS_PHYSICAL", 32: "ITEM_FLAG2_EVERYONE_CAN_ROLL_NEED",
            64: "ITEM_FLAG2_NO_TRADE_BIND_ON_ACQUIRE", 128: "ITEM_FLAG2_CAN_TRADE_BIND_ON_ACQUIRE",
            256: "ITEM_FLAG2_CAN_ONLY_ROLL_GREED", 512: "ITEM_FLAG2_CASTER_WEAPON",
            1024: "ITEM_FLAG2_DELETE_ON_LOGIN", 2048: "ITEM_FLAG2_INTERNAL_ITEM",
            4096: "ITEM_FLAG2_NO_VENDOR_VALUE", 8192: "ITEM_FLAG2_SHOW_BEFORE_DISCOVERED",
            16384: "ITEM_FLAG2_OVERRIDE_GOLD_COST", 32768: "ITEM_FLAG2_IGNORE_DEFAULT_RATED_BG_RESTRICTIONS",
            65536: "ITEM_FLAG2_NOT_USABLE_IN_RATED_BG", 131072: "ITEM_FLAG2_BNET_ACCOUNT_TRADE_OK",
            262144: "ITEM_FLAG2_CONFIRM_BEFORE_USE", 524288: "ITEM_FLAG2_REEVALUATE_BONDING_ON_TRANSFORM",
            1048576: "ITEM_FLAG2_NO_TRANSFORM_ON_CHARGE_DEPLETION", 2097152: "ITEM_FLAG2_NO_ALTER_ITEM_VISUAL",
            4194304: "ITEM_FLAG2_NO_SOURCE_FOR_ITEM_VISUAL", 8388608: "ITEM_FLAG2_IGNORE_QUALITY_FOR_ITEM_VISUAL_SOURCE",
            16777216: "ITEM_FLAG2_NO_DURABILITY", 33554432: "ITEM_FLAG2_ROLE_TANK",
            67108864: "ITEM_FLAG2_ROLE_HEALER", 134217728: "ITEM_FLAG2_ROLE_DAMAGE",
            268435456: "ITEM_FLAG2_CAN_DROP_IN_CHALLENGE_MODE", 536870912: "ITEM_FLAG2_NEVER_STACK_IN_LOOT_UI",
            1073741824: "ITEM_FLAG2_DISENCHANT_TO_LOOT_TABLE", 2147483648: "ITEM_FLAG2_USED_IN_A_TRADESKILL"
        }

        self.tbl_itemflagscustom = {
            1: "ITEM_FLAGS_CU_UNUSED", 2: "ITEM_FLAGS_CU_IGNORE_QUEST_STATUS",
            4: "ITEM_FLAGS_CU_FOLLOW_LOOT_RULES"
        }

        # Menu layout: (menu title, [(table title, attribute name), ...])
        self.categories = [
            ("Creature Template Flags", [
                ("NPC FLAGS", "tbl_npcflags"),
                ("UNIT_FLAGS", "tbl_unitflags"),
                ("UNIT_FLAGS2", "tbl_unitflags2"),
                ("DYNAMICFLAGS", "tbl_unitdynflags"),
                ("TYPE_FLAGS", "tbl_creaturetypeflags"),
                ("TYPE_FLAGS2", "tbl_creaturetypeflags2"),
                ("FLAGS_EXTRA", "tbl_creatureflagsextra"),
                ("STATIC_FLAGS1", "tbl_creaturestaticflags"),
                ("STATIC_FLAGS2", "tbl_creaturestaticflags2"),
                ("STATIC_FLAGS3", "tbl_creaturestaticflags3"),
                ("STATIC_FLAGS4", "tbl_creaturestaticflags4"),
                ("STATIC_FLAGS5", "tbl_creaturestaticflags5")
            ]),
            ("Quest Template Flags", [
                ("QUEST_FLAGS", "tbl_questflags")
            ]),
            ("Item Template Flags", [
                ("ITEM_FLAGS", "tbl_itemflags"),
                ("ITEM_FLAGS2", "tbl_itemflags2"),
                ("ITEM_FLAGS_CUSTOM", "tbl_itemflagscustom")
            ])
        ]

        self.max_value = 0xFFFFFFFF

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def parse_input(self, value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value.startswith('0x'):
                return int(value, 16)
            return int(value)
        return int(value)

    def validate_value(self, value):
        if value > self.max_value:
            return False, f"Value too high! Maximum is {self.max_value} (0x{self.max_value:X})"
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

    def reference_text(self, entries):
        output = []
        for title, attr in entries:
            flag_dict = getattr(self, attr)
            output.append(f"\n{title}:")
            output.append("=" * 80)
            output.append(f"{'Value':>12}\t{'Hex':<12} {'Flag Name':<50}")
            output.append("-" * 80)

            for value in sorted(flag_dict.keys()):
                output.append(f"{value:>12,}\t0x{value:<10X} {flag_dict[value]}")
        return "\n".join(output)

    def show_all_flags_table(self):
        entries = [entry for _, category_entries in self.categories for entry in category_entries]
        self.clear_screen()
        print(self.reference_text(entries))
        self.wait_for_key()

    def show_category_menu(self, menu_title, entries):
        numbers = [str(i) for i in range(1, len(entries) + 1)]
        while True:
            self.clear_screen()
            print(menu_title)
            print("-" * 30)
            for number, (title, _) in zip(numbers, entries):
                print(f"{number:>2} - {title}")
            print(" s - Show all flags of this category (reference)")
            print(" b - Back to main menu")
            print(" q - Quit program")

            try:
                choice = input(f"\nSelect (1-{len(entries)}, s, b, q): ").strip().lower()

                if choice == 'q':
                    return 'quit'
                if choice == 'b':
                    return
                if choice == 's':
                    self.clear_screen()
                    print(self.reference_text(entries))
                    self.wait_for_key()
                    continue

                if choice not in numbers:
                    print(f"Invalid choice. Use 1-{len(entries)}, s, b, or q")
                    self.wait_for_key()
                    continue

                title, attr = entries[int(choice) - 1]
                flag_dict = getattr(self, attr)

                self.clear_screen()
                print(f"Selected: {title}")
                print("-" * 30)

                value_str = input("Enter bitmask (decimal or hex like 0x83): ").strip()
                if not value_str:
                    continue

                try:
                    value = self.parse_input(value_str)

                    is_valid, error_msg = self.validate_value(value)
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

    def wait_for_key(self):
        input("\nPress any key to continue...")

def main():
    decoder = WoWFlagDecoder()

    while True:
        decoder.clear_screen()
        print("WoW Flag Decoder - Main Menu")
        print("Cataclysm Preservation Project (4.3.4)")
        print("=" * 30)
        for number, (menu_title, _) in enumerate(decoder.categories, 1):
            print(f"{number} - {menu_title}")
        print("s - Show all flags (reference)")
        print("q - Quit")
        print("-" * 30)

        try:
            choice = input(f"\nSelect (1-{len(decoder.categories)}, s, q): ").strip().lower()

            if choice == 'q':
                decoder.clear_screen()
                print("Goodbye!")
                break

            if choice == 's':
                decoder.show_all_flags_table()
                continue

            if choice in [str(i) for i in range(1, len(decoder.categories) + 1)]:
                menu_title, entries = decoder.categories[int(choice) - 1]
                if decoder.show_category_menu(menu_title, entries) == 'quit':
                    break
            else:
                print(f"Invalid choice. Use 1-{len(decoder.categories)}, s, or q")
                decoder.wait_for_key()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
