# Level definitions for Cosmic Clash

# Structure:
# LEVELS = {
#     level_number: {
#         "waves": [
#             # Wave definition:
#             {"type": "enemy_type_id", "count": num_enemies, "spawn_delay": ms, "pattern": "spawn_pattern_id"},
#             # ... more waves
#         ],
#         "enemy_count_for_boss": total_enemies_before_boss,
#         "boss_type": "boss_id"
#     },
# }

# Enemy Types: basic, zigzag, shooter (add more later: e.g., fast, tank, homing_shooter)
# Spawn Patterns: top_random, top_sides, top_center_spread, left_entry_sweep, right_entry_sweep (add more later)

LEVELS = {
    1: {
        "waves": [
            {"type": "basic", "count": 5, "spawn_delay": 1200, "pattern": "top_random"},
            {"type": "basic", "count": 8, "spawn_delay": 800, "pattern": "top_random"},
            {"type": "zigzag", "count": 3, "spawn_delay": 1500, "pattern": "top_sides"},
        ],
        "enemy_count_for_boss": 16,
        "boss_type": "level1_boss"
    },
    2: {
        "waves": [
            {"type": "basic", "count": 6, "spawn_delay": 1000, "pattern": "top_sides"},
            {"type": "zigzag", "count": 5, "spawn_delay": 1000, "pattern": "top_random"},
            {"type": "basic", "count": 7, "spawn_delay": 700, "pattern": "top_center_spread"},
            {"type": "shooter", "count": 2, "spawn_delay": 2000, "pattern": "top_sides"},
        ],
        "enemy_count_for_boss": 20,
        "boss_type": "level2_boss"
    },
    3: {
        "waves": [
            {"type": "shooter", "count": 4, "spawn_delay": 1500, "pattern": "top_random"},
            {"type": "zigzag", "count": 6, "spawn_delay": 900, "pattern": "top_random"},
            {"type": "basic", "count": 10, "spawn_delay": 500, "pattern": "top_center_spread"},
        ],
        "enemy_count_for_boss": 20,
        "boss_type": "level1_boss" # Reuse boss for now
    },
    4: {
        "waves": [
            {"type": "basic", "count": 8, "spawn_delay": 700, "pattern": "top_sides"},
            {"type": "zigzag", "count": 8, "spawn_delay": 700, "pattern": "top_sides"},
            {"type": "shooter", "count": 5, "spawn_delay": 1200, "pattern": "top_random"},
        ],
        "enemy_count_for_boss": 21,
        "boss_type": "level2_boss" # Reuse boss
    },
    5: {
        "waves": [
            {"type": "zigzag", "count": 10, "spawn_delay": 600, "pattern": "top_random"},
            {"type": "shooter", "count": 6, "spawn_delay": 1000, "pattern": "top_sides"},
            {"type": "basic", "count": 10, "spawn_delay": 400, "pattern": "top_center_spread"},
        ],
        "enemy_count_for_boss": 26,
        "boss_type": "level3_boss" # Introduce new boss type
    },
    # Placeholder definitions for levels 6-10 - Needs more variety
    6: {
        "waves": [
            {"type": "basic", "count": 15, "spawn_delay": 500, "pattern": "top_random"},
            {"type": "shooter", "count": 8, "spawn_delay": 900, "pattern": "top_sides"},
            {"type": "zigzag", "count": 10, "spawn_delay": 600, "pattern": "top_center_spread"},
            ],
        "enemy_count_for_boss": 33,
        "boss_type": "level3_boss"
    },
    7: {
        "waves": [
            {"type": "shooter", "count": 10, "spawn_delay": 800, "pattern": "top_random"},
            {"type": "zigzag", "count": 15, "spawn_delay": 500, "pattern": "top_sides"},
            ],
        "enemy_count_for_boss": 25,
        "boss_type": "level4_boss"
    },
    8: {
        "waves": [
            {"type": "basic", "count": 20, "spawn_delay": 400, "pattern": "top_center_spread"},
            {"type": "zigzag", "count": 10, "spawn_delay": 600, "pattern": "top_sides"},
            {"type": "shooter", "count": 10, "spawn_delay": 700, "pattern": "top_random"},
            ],
        "enemy_count_for_boss": 40,
        "boss_type": "level4_boss"
    },
    9: {
        "waves": [
            {"type": "zigzag", "count": 20, "spawn_delay": 400, "pattern": "top_random"},
            {"type": "shooter", "count": 15, "spawn_delay": 600, "pattern": "top_sides"},
            ],
        "enemy_count_for_boss": 35,
        "boss_type": "level5_boss"
    },
   10: { # Final level - mix of enemies, tough boss
        "waves": [
            {"type": "basic", "count": 10, "spawn_delay": 500, "pattern": "top_center_spread"},
            {"type": "zigzag", "count": 10, "spawn_delay": 500, "pattern": "top_sides"},
            {"type": "shooter", "count": 10, "spawn_delay": 800, "pattern": "top_random"},
            {"type": "basic", "count": 15, "spawn_delay": 300, "pattern": "top_random"},
            {"type": "zigzag", "count": 10, "spawn_delay": 400, "pattern": "top_sides"},
        ],
        "enemy_count_for_boss": 55,
        "boss_type": "final_boss"
    },
}

