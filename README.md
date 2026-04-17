[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/fmId_lNR)
# COMP-1510-202610-TERM-PROJECT
Every program needs a README.md

This is written in Markdown.

Read about Markdown here: [markdowncheatsheet](https://www.markdownguide.org/cheat-sheet/)

## YOUR NAME:
Fawaz Shariff

## YOUR STUDENT NUMBER:
A01443086

## YOUR GITHUB NAME:
Chungywungy

## PROJECT STRUCTURE
```text
PythonProject-1510-Term-Project-Fawaz/
│
├── game/
│   ├── __init__.py
│   ├── character.py
│   ├── combat.py
│   ├── file_tampering.py
│   ├── game.py
│   ├── map.py
│   └── progression.py
│
├── json_files/
│   ├── character.json
│   ├── classes.json
│   ├── events.json
│   └── items.json
│
├── sounds/
│   ├── clavar_la_espada_shiro_sagisu.mp3
│   ├── escalon_shiro_sagisu.mp3
│   ├── la_distancia_para_un_duelo_shiro_sagisu.mp3
│   ├── nube_negra_shiro_sagisu.mp3
│   └── test.mp3
│
├── tests/
│   ├── __init__.py
│   ├── test_apply_class_traits.py
│   ├── test_apply_item_effect.py
│   ├── test_award_xp.py
│   ├── test_build.py
│   ├── test_calculate_damage.py
│   ├── test_character_class.py
│   ├── test_character_name.py
│   ├── test_create_character.py
│   ├── test_describe_location.py
│   ├── test_display_inventory.py
│   ├── test_enemy_behaviour.py
│   ├── test_equip_item.py
│   ├── test_flee.py
│   ├── test_get_available_actions.py
│   ├── test_get_effective_stats.py
│   ├── test_get_user_choice.py
│   ├── test_level_up.py
│   ├── test_move_character.py
│   ├── test_open_json.py
│   ├── test_perform_action.py
│   ├── test_player_name.py
│   ├── test_tick_cooldowns.py
│   ├── test_tick_temp_buffs.py
│   ├── test_traverse_stairs.py
│   ├── test_unequip_item.py
│   ├── test_use_item.py
│   └── test_validate_move.py
│
├── .gitignore
├── character_information.pdf
├── flowchart.pdf
└── README.md
```
---

## INSTRUCTIONS

1. Open terminal.
2. Navigate to the location of this project.
3. Run game.py from the terminal with ```python -m game.game```

---

## HELPFUL INFORMATION

- The game is designed to be challenging and may require multiple runs.
- Avoid unnecessary exploration early game unless you are prepared for fights.
- The boss encounter is placed on the final floor.
- Map generation includes stairs, fights, and special event tiles.
- Combat timing and difficulty are balanced around turn-based decision making.
- Using items in combat does not use up a turn.
- one of the classes is significantly stronger than the other.

Legend:
  - S = stairs
  - C = chests
  - "-" = random event

---

## REQUIRED FEATURES CHECKLIST

| Requirement | Location |
|------------|----------|
| Dictionary/list comprehensions | `game/map.py` and `combat.py` |
| Selection (if statements) | `combat.py`, `character.py`, `map.py` |
| Repetition (loops) | `combat.py`, `game.py`, `map.py` |
| Membership operators | `combat.py`, `character.py` |
| `range()` usage | `map.build()` and loops in combat |
| `random` module usage | `map.py`, `combat.py`, `enemy_behaviour` |
| File handling | `file_tampering.py` |
| Formatted output | throughout `combat.py` and `game.py` |
| Itertools | `combat.combat` and `combat.boss_combat`|

---

## GAME OVERVIEW

This project is a turn-based RPG where the player:
- Navigates a multi-layer dungeon map
- Encounters enemies and bosses
- Uses equipment, consumables, and class abilities
- Gains XP and levels up
- Manages stats like health and mana
- Can traverse stairs between floors

Combat is turn-based and includes:
- Actions with cooldowns
- Mana costs
- Item usage
- Temporary buffs
- Enemy AI behaviour
- Boss-specific rules (no fleeing)

---

## SPOILERS

Boss encounter is located on the final layer of the map at a randomly assigned stair/empty tile position.

---

## NOTES

- The game uses JSON files to define classes, items, and events.
- Map generation is partially random, meaning each playthrough differs.
- Combat system is modular and split across multiple files for maintainability.
