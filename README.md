# TrinityCore Flag Calculator

Small interactive command-line tool that decodes TrinityCore database bitmask values into readable flag names. Enter a decimal or hex value and see which flags are set.

## Supported flag sets

- **Creature template:** `npcflag`, `unit_flags`, `unit_flags2`, `dynamicflags`, `type_flags`, `flags_extra`
- **Quest template:** `Flags`
- **Item template:** `Flags`, `Flags2`, `Flags3`, custom flags

A reference table of all known flags is available from the menus (`s`).

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
