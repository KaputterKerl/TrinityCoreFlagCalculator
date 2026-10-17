# TrinityCore Flag Calculator

Small interactive command-line tool that decodes TrinityCore database bitmask values into readable flag names. Enter a decimal or hex value and see which flags are set.

## Versions

One script per server version. Each one has the flag tables of its own source tree:

| Script | Source |
|---|---|
| `FlagCalc_TrinityCoreMaster.py` | [TrinityCore](https://github.com/TrinityCore/TrinityCore) `master` |
| `FlagCalc_TrinityCore335.py` | TrinityCore branch `3.3.5` |
| `FlagCalc_CataclysmClassic.py` | TrinityCore branch `cata_classic` |
| `FlagCalc_CataclysmPreservation434.py` | [Cataclysm Preservation Project](https://github.com/The-Cataclysm-Preservation-Project/TrinityCore) (4.3.4) |

The tables are generated from the flag enums in the headers of these branches. The scripts only need Python 3.

## Supported flag sets

What a script offers depends on its version, for example only the older trees have Dynamic Flags and Type Flags, and only `master` and `cata_classic` have `unit_flags3`.

- **Creature template:** `npcflag`, `unit_flags`, `unit_flags2`, `dynamicflags`, `type_flags`, `flags_extra`, the creature static flags, and where they exist `npcflag2`, `unit_flags3` and `type_flags2`
- **Quest template:** `Flags`, and where they exist `FlagsEx` and `FlagsEx2`
- **Item template:** `Flags`, `Flags2`, `Flags3`, `Flags4`, custom flags

A reference table of all known flags is available from the main menu and from each category menu (`s`).

## Usage

Requires Python 3, no extra dependencies.

```
python3 FlagCalc_TrinityCoreMaster.py   # or any of the other scripts
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
           2	0x2          Questgiver
         128	0x80         Vendor
--------------------------------------------------------------------------------
       List:	1, 2, 128

      Count:	3 flag(s)
```

## License

GPL-3.0, see [LICENSE](LICENSE).
