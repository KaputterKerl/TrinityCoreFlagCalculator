# TrinityCore Flag Calculator

Small interactive command-line tool that decodes TrinityCore database bitmask values into readable flag names. Enter a decimal or hex value and see which flags are set.

## Supported flag sets

Tables are generated from the TrinityCore `master` headers (October 2026).

- **Creature template:** `npcflag`, `npcflag2`, `unit_flags`, `unit_flags2`, `unit_flags3`, `flags_extra`, and the creature static flags 1 to 8
- **Quest template:** `Flags`, `FlagsEx`, `FlagsEx2`
- **Item template:** `Flags`, `Flags2`, `Flags3`, `Flags4`, custom flags

The old Type Flags table is gone because it was replaced by the creature static flags in `master`. The old Dynamic Flags table is gone because `master` no longer has a `UNIT_DYNFLAG_*` enum in the headers this tool is generated from.

A reference table of all known flags is available from the main menu and from each category menu (`s`).

## Usage

Requires Python 3, no extra dependencies.

```
python3 FlagCalc_TrinityCoreMaster.py
```

Pick a category, pick a flag set, then enter a bitmask as decimal (`131`) or hex (`0x83`).

## Example

Decoding `0x83` as NPC flags:

```
NPC FLAGS
Input: 0x83
================================================================================
       Value	Hex          Flag Name
--------------------------------------------------------------------------------
           1	0x1          Gossip
           2	0x2          Quest Giver
         128	0x80         Vendor
--------------------------------------------------------------------------------
       List:	1, 2, 128

      Count:	3 flag(s)
```

## License

GPL-3.0, see [LICENSE](LICENSE).
