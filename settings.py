# Settings for Cosmic Clash

import pygame

# --- Screen Dimensions ---
WIDTH = 1280
HEIGHT = 800

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255) # Default player color
GREEN = (0, 255, 0) # Enemy color
YELLOW = (255, 255, 0) # Power-up color / Enemy Bullet
ORANGE = (255, 165, 0) # Boss color (example)
TEAL = (0, 150, 150) # Zigzag enemy
BROWN = (200, 100, 0) # Shooter enemy
PURPLE = (200, 0, 200) # Boss 2
GREY = (150, 150, 150) # Final Boss

# --- Game Settings ---
FPS = 60
TITLE = "Cosmic Clash"
FONT_NAME = pygame.font.match_font("arial") # Or choose a specific pixel font later

# --- Player Settings ---
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
PLAYER_VEL = 64
PLAYER_SHOOT_DELAY_BASE = 250 # milliseconds
PLAYER_MAX_POWER_LEVEL = 6
PLAYER_POWERUP_DURATION = 10000 # milliseconds (10 seconds)
PLAYER_LIVES = 3

# --- Bullet Settings ---
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_VEL = 7
ENEMY_BULLET_VEL_MULT = 0.8 # Enemy bullets are 80% speed of player bullets

# --- Enemy Settings ---
ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35
ENEMY_VEL_BASE = 2 # Base downward speed
ENEMY_SHOOT_DELAY_BASE = 1500 # Base delay for shooters
ENEMY_SKIP_SCORE = 5 # Score awarded for skipping an enemy

# --- Boss Settings ---
BOSS_WIDTH = 100
BOSS_HEIGHT = 80
BOSS_HEALTH_BASE = 100 # Per level
BOSS_VEL_BASE = 1
BOSS_SHOOT_DELAY_BASE = 1000

# --- PowerUp Settings ---
POWERUP_WIDTH = 25
POWERUP_HEIGHT = 25
POWERUP_VEL = 3
POWERUP_DROP_CHANCE = 0.1 # Base chance

# --- Difficulty Settings ---
# Multipliers applied based on selected difficulty
DIFFICULTY_LEVELS = {
    "Easy": {
        "enemy_speed_mult": 0.8,
        "enemy_bullet_speed_mult": 0.7,
        "enemy_spawn_rate_mult": 1.3, # Slower spawn
        "enemy_shoot_delay_mult": 1.4, # Slower shooting
        "boss_health_mult": 0.7,
        "boss_speed_mult": 0.8,
        "boss_shoot_delay_mult": 1.3,
        "powerup_drop_mult": 1.5 # More powerups
    },
    "Medium": {
        "enemy_speed_mult": 1.0,
        "enemy_bullet_speed_mult": 1.0,
        "enemy_spawn_rate_mult": 1.0,
        "enemy_shoot_delay_mult": 1.0,
        "boss_health_mult": 1.0,
        "boss_speed_mult": 1.0,
        "boss_shoot_delay_mult": 1.0,
        "powerup_drop_mult": 1.0
    },
    "Hard": {
        "enemy_speed_mult": 1.3,
        "enemy_bullet_speed_mult": 1.2,
        "enemy_spawn_rate_mult": 0.7, # Faster spawn
        "enemy_shoot_delay_mult": 0.7, # Faster shooting
        "boss_health_mult": 1.5,
        "boss_speed_mult": 1.2,
        "boss_shoot_delay_mult": 0.7,
        "powerup_drop_mult": 0.6 # Fewer powerups
    }
}

