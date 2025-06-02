# Cosmic Clash - Main Game File

import pygame
import sys
import random
import time
import math
from settings import *
from sprites import Player, Enemy, Bullet, PowerUp, Boss, EnemyBullet
from levels import LEVELS
from explosion import Explosion

class Background:
    def __init__(self, game):
        self.game = game
        self.layers = []
        self.scroll_speeds = [0.5, 1.0, 1.5]  # Different scroll speeds for parallax effect
        self.positions = [0, 0, 0]  # Current position of each layer
        
        # Load background layers
        for i in range(3):
            layer_path = f"assets/bg/Starry background  - Layer {i+1:02d} - {'Void' if i == 0 else 'Stars'}.png"
            try:
                layer = pygame.image.load(layer_path).convert_alpha()
                # Scale the layer to cover the entire screen while maintaining aspect ratio
                scale = max(WIDTH / layer.get_width(), HEIGHT / layer.get_height())
                new_width = int(layer.get_width() * scale)
                new_height = int(layer.get_height() * scale)
                layer = pygame.transform.scale(layer, (new_width, new_height))
                self.layers.append(layer)
            except pygame.error as e:
                print(f"Error loading background layer {i+1}: {e}")
                # Create a fallback colored surface
                fallback = pygame.Surface((WIDTH, HEIGHT))
                fallback.fill((10, 10, 30))  # Dark blue color
                self.layers.append(fallback)

    def update(self):
        # Update positions for parallax scrolling
        for i in range(len(self.layers)):
            self.positions[i] += self.scroll_speeds[i]
            if self.positions[i] >= self.layers[i].get_height():
                self.positions[i] = 0

    def draw(self, surface):
        # Draw each layer
        for i, layer in enumerate(self.layers):
            # Calculate the position to center the layer
            x_offset = (WIDTH - layer.get_width()) // 2
            
            # Draw the main layer
            surface.blit(layer, (x_offset, self.positions[i]))
            # Draw the layer again above to create seamless scrolling
            surface.blit(layer, (x_offset, self.positions[i] - layer.get_height()))
            # Draw the layer again below to ensure full coverage
            surface.blit(layer, (x_offset, self.positions[i] + layer.get_height()))

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize sound
        # Set standard windowed mode with fixed size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()
        self.background = Background(self)  # Initialize background
        self.game_state = "START_SCREEN"
        self.current_level = 1
        self.score = 0
        self.difficulty = "Medium" # Default difficulty
        self.difficulty_multipliers = DIFFICULTY_LEVELS[self.difficulty]
        self.playing = False
        self.selected_level = 1
        self.max_level = max(LEVELS.keys())
        self.difficulty_options = list(DIFFICULTY_LEVELS.keys())
        self.selected_difficulty_index = self.difficulty_options.index(self.difficulty)
        
        # Load background music
        try:
            pygame.mixer.music.load("assets/audio.wav")
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        except:
            print("Could not load background music")

        # Timers for automatic difficulty adjustments and player power increase
        self.last_power_increase_time = pygame.time.get_ticks()
        self.power_increase_interval = 30000 # 30 seconds in milliseconds
        self.last_obstacle_difficulty_increase_time = pygame.time.get_ticks()
        self.obstacle_difficulty_increase_interval = 20000 # 20 seconds in milliseconds
        self.time_based_difficulty_multiplier = 1.0 # Starts at 1.0, increases over time

    def load_data(self):
        import os
        self.assets = {}
        asset_dir = "assets"
        
        # Ensure the assets directory exists
        if not os.path.exists(asset_dir):
            print(f"Error: Assets directory '{asset_dir}' does not exist.")
            return
        
        # Define asset mappings
        asset_files = {
            "player": "player.png",
            "enemy_basic": "enemy_basic.png",
            "enemy_zigzag": "enemy_zigzag.png",
            "enemy_shooter": "enemy_shooter.png",
            "boss_level1": "boss_level1.png",
            "boss_level2": "boss_level2.png",
            "boss_level3": "boss_level3.png",
            "boss_level4": "boss_level4.png",
            "boss_level5": "boss_level5.png",
            "boss_final": "boss_final.png",
            "bullet_player": "bullet_player.png",
            "bullet_enemy": "bullet_enemy.png",
            "powerup": "powerup.png",
            "explosion_frames": [
                "explosion_1.png",
                "explosion_2.png",
                "explosion_3.png",
                "explosion_4.png",
                "explosion_5.png",
                "explosion_6.png",
                "explosion_7.png",
                "explosion_8.png"
            ]
        }
        
        # Scaling factor for larger sprites
        SCALE_FACTOR = 1.5
        
        # Load images with error handling
        for key, filename in asset_files.items():
            if key == "explosion_frames":
                self.assets[key] = []
                for frame_file in filename:
                    try:
                        path = os.path.join(asset_dir, frame_file)
                        if not os.path.exists(path):
                            print(f"Error: File '{path}' does not exist.")
                            raise FileNotFoundError
                        img = pygame.image.load(path).convert_alpha()
                        # Scale explosion frames to match original sizes (30x30 to 100x100)
                        size = 30 + (len(self.assets[key]) * 10)
                        img = pygame.transform.scale(img, (int(size), int(size)))
                        self.assets[key].append(img)
                    except (pygame.error, FileNotFoundError) as e:
                        print(f"Warning: Could not load {path}. Using placeholder.")
                        size = 30 + (len(self.assets[key]) * 10)
                        surface = pygame.Surface([size, size], pygame.SRCALPHA)
                        color_index = len(self.assets[key]) % len([(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 255, 255)])
                        pygame.draw.circle(surface, [(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 255, 255)][color_index],
                                        (size // 2, size // 2), size // 2 - 5)
                        self.assets[key].append(surface)
            else:
                try:
                    path = os.path.join(asset_dir, filename)
                    if not os.path.exists(path):
                        print(f"Error: File '{path}' does not exist.")
                        raise FileNotFoundError
                    img = pygame.image.load(path).convert_alpha()
                    # Scale images to match settings.py sizes with scaling factor
                    if key == "player":
                        img = pygame.transform.scale(img, (int(PLAYER_WIDTH * SCALE_FACTOR), int(PLAYER_HEIGHT * SCALE_FACTOR)))
                    elif key.startswith("enemy"):
                        img = pygame.transform.scale(img, (int(ENEMY_WIDTH * SCALE_FACTOR), int(ENEMY_HEIGHT * SCALE_FACTOR)))
                    elif key.startswith("boss"):
                        img = pygame.transform.scale(img, (int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)))
                    elif key == "bullet_player":
                        img = pygame.transform.scale(img, (int(BULLET_WIDTH * SCALE_FACTOR), int(BULLET_HEIGHT * SCALE_FACTOR)))
                    elif key == "bullet_enemy":
                        img = pygame.transform.scale(img, (int(BULLET_WIDTH * SCALE_FACTOR), int(BULLET_HEIGHT * 1.5 * SCALE_FACTOR)))
                    elif key == "powerup":
                        img = pygame.transform.scale(img, (POWERUP_WIDTH, POWERUP_HEIGHT))  # Unchanged size
                    self.assets[key] = img
                except (pygame.error, FileNotFoundError) as e:
                    print(f"Warning: Could not load {path}. Using placeholder surface.")
                    # Fallback to colored surfaces with scaled sizes
                    if key == "player":
                        surface = pygame.Surface([int(PLAYER_WIDTH * SCALE_FACTOR), int(PLAYER_HEIGHT * SCALE_FACTOR)])
                        surface.fill(BLUE)
                    elif key == "enemy_basic":
                        surface = pygame.Surface([int(ENEMY_WIDTH * SCALE_FACTOR), int(ENEMY_HEIGHT * SCALE_FACTOR)])
                        surface.fill(GREEN)
                    elif key == "enemy_zigzag":
                        surface = pygame.Surface([int(ENEMY_WIDTH * SCALE_FACTOR), int(ENEMY_HEIGHT * SCALE_FACTOR)])
                        surface.fill(TEAL)
                    elif key == "enemy_shooter":
                        surface = pygame.Surface([int(ENEMY_WIDTH * SCALE_FACTOR), int(ENEMY_HEIGHT * SCALE_FACTOR)])
                        surface.fill(BROWN)
                    elif key == "boss_level1":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(ORANGE)
                    elif key == "boss_level2":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(PURPLE)
                    elif key == "boss_level3":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(RED)
                    elif key == "boss_level4":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(WHITE)
                    elif key == "boss_level5":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(BLUE)
                    elif key == "boss_final":
                        surface = pygame.Surface([int(BOSS_WIDTH * SCALE_FACTOR), int(BOSS_HEIGHT * SCALE_FACTOR)])
                        surface.fill(GREY)
                    elif key == "bullet_player":
                        surface = pygame.Surface([int(BULLET_WIDTH * SCALE_FACTOR), int(BULLET_HEIGHT * SCALE_FACTOR)])
                        surface.fill(RED)
                    elif key == "bullet_enemy":
                        surface = pygame.Surface([int(BULLET_WIDTH * SCALE_FACTOR), int(BULLET_HEIGHT * 1.5 * SCALE_FACTOR)])
                        surface.fill(YELLOW)
                    elif key == "powerup":
                        surface = pygame.Surface([POWERUP_WIDTH, POWERUP_HEIGHT])
                        surface.fill(YELLOW)
                    self.assets[key] = surface        
                           
    def set_difficulty(self, difficulty_level):
        if difficulty_level in DIFFICULTY_LEVELS:
            self.difficulty = difficulty_level
            self.difficulty_multipliers = DIFFICULTY_LEVELS[self.difficulty]
            print(f"Difficulty set to: {self.difficulty}")
            self.selected_difficulty_index = self.difficulty_options.index(self.difficulty) # Update index
        else:
            print(f"Warning: Invalid difficulty ", difficulty_level, ". Keeping ", self.difficulty)

    def new(self):
        # Start or restart a game
        self.score = 0
        self.current_level = self.selected_level
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.boss_group = pygame.sprite.GroupSingle()
        self.player = Player(self) # Player adds itself
        self.level_data = LEVELS[self.current_level]
        self.current_wave = 0
        self.enemies_killed_this_level = 0
        self.game_state = "PLAYING"
        
        # Start playing background music
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.background.update()  # Update background animation

        if self.game_state == "PLAYING":
            self.manage_waves()

        self.check_collisions()

        if self.player.lives <= 0 and not self.player.hidden:
             self.game_state = "GAME_OVER"
             self.playing = False

        # Check for automatic player power increase
        now = pygame.time.get_ticks()
        if self.game_state == "PLAYING" or self.game_state == "BOSS_FIGHT":
            if now - self.last_power_increase_time > self.power_increase_interval:
                self.player.collect_powerup() # Reuse powerup logic for stat increase
                self.last_power_increase_time = now
                print("Player power increased automatically!")

            # Check for automatic obstacle difficulty increase
            if now - self.last_obstacle_difficulty_increase_time > self.obstacle_difficulty_increase_interval:
                self.time_based_difficulty_multiplier += 0.1 # Increase multiplier by 0.1
                self.last_obstacle_difficulty_increase_time = now
                print(f"Obstacle difficulty increased! Multiplier: {self.time_based_difficulty_multiplier:.2f}")

    def manage_waves(self):
        # If we're in a boss fight, don't manage waves
        if self.game_state == "BOSS_FIGHT":
            return

        # If we have no enemies and haven't completed all waves
        if len(self.enemies) == 0:
            if self.current_wave < len(self.level_data["waves"]):
                # Spawn next wave
                wave = self.level_data["waves"][self.current_wave]
                print(f"Spawning wave {self.current_wave + 1} with {wave['count']} {wave['type']} enemies")
                for _ in range(wave["count"]):
                    self.spawn_enemy(wave["type"], wave["pattern"])
                self.current_wave += 1
            # If all waves are complete and we've killed enough enemies, start boss fight
            elif self.enemies_killed_this_level >= self.level_data["enemy_count_for_boss"]:
                print(f"Starting boss fight for level {self.current_level}")
                self.start_boss_fight()
            else:
                # If we haven't killed enough enemies but all waves are done, spawn more enemies
                print(f"Spawning additional enemies to reach boss threshold. Killed: {self.enemies_killed_this_level}, Required: {self.level_data['enemy_count_for_boss']}")
                # Spawn a small wave of basic enemies
                for _ in range(3):
                    self.spawn_enemy("basic", "top_random")

    def check_collisions(self):
        # Player Bullets hitting enemies
        hits_bullet_enemy = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for enemy_hit in hits_bullet_enemy:
            self.score += 10
            self.enemies_killed_this_level += 1
            # Apply difficulty multiplier to powerup drop chance
            if random.random() < (POWERUP_DROP_CHANCE * self.difficulty_multipliers["powerup_drop_mult"]):
                PowerUp(self, enemy_hit.rect.center)

        # Player Bullets hitting boss
        if self.game_state == "BOSS_FIGHT":
            boss = self.boss_group.sprite
            if boss is not None:  # Check if boss exists
                hits_bullet_boss = pygame.sprite.spritecollide(boss, self.bullets, True)
                for hit in hits_bullet_boss:
                    boss_defeated = boss.take_damage(1)
                    self.score += 5
                    if boss_defeated:
                        self.score += 500 * self.current_level
                        self.handle_boss_defeat()
                        return  # Exit early to prevent any further processing

        # Player hitting enemies or boss
        if not self.player.hidden:
            hits_player_enemy = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if self.game_state == "BOSS_FIGHT" and self.boss_group.sprite is not None:
                hits_player_boss = pygame.sprite.spritecollide(self.player, self.boss_group, False)
                if hits_player_boss:
                    self.player_death()
            if hits_player_enemy:
                self.player_death()

            # Player hitting enemy bullets
            hits_player_enemybullet = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            if hits_player_enemybullet:
                self.player_death()

        # Player collecting power-ups
        if not self.player.hidden:
            hits_player_powerup = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for hit in hits_player_powerup:
                self.player.collect_powerup()

    def handle_boss_defeat(self):
        """Handle the boss defeat sequence and level transition"""
        print(f"Boss defeated in level {self.current_level}")
        # Create explosion at boss position if boss still exists
        if self.boss_group.sprite is not None:
            explosion = Explosion(self, self.boss_group.sprite.rect.center)
            self.all_sprites.add(explosion)
        
        # Clear all projectiles and enemies
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.powerups.empty()
        
        # Add a delay to show the explosion
        pygame.time.delay(1000)
        
        # Clear the boss group
        self.boss_group.empty()
        
        # Transition to next level
        self.level_complete()

    def level_complete(self):
        """Handle level completion and transition to next level"""
        print(f"Level {self.current_level} Complete!")
        self.current_level += 1
        
        # Clear all sprites except player
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()
        
        # Ensure all sprite groups are empty
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.powerups.empty()
        self.boss_group.empty()

        if self.current_level > len(LEVELS):
            print("Congratulations! You beat the game!")
            self.game_state = "GAME_OVER"
            self.playing = False
        else:
            print(f"Starting level {self.current_level}")
            # Reset level state
            self.level_data = LEVELS[self.current_level]
            self.current_wave = 0
            self.enemies_killed_this_level = 0
            self.game_state = "PLAYING"
            
            # Reset player state
            self.player.rect.centerx = WIDTH / 2
            self.player.rect.bottom = HEIGHT - 10
            self.player.hidden = False
            
            # Add a small delay before starting next level
            pygame.time.delay(500)

    def start_boss_fight(self):
        """Start a boss fight with proper state management"""
        if self.game_state != "BOSS_FIGHT":  # Prevent multiple boss spawns
            # Clear any remaining enemies and projectiles
            self.enemies.empty()
            self.bullets.empty()
            self.enemy_bullets.empty()
            self.powerups.empty()
            self.boss_group.empty()
            
            # Start the boss fight
            boss_type = self.level_data.get("boss_type", "level1_boss")
            print(f"Starting Boss Fight: {boss_type} for Level {self.current_level}")
            self.game_state = "BOSS_FIGHT"
            Boss(self, self.current_level, boss_type)
            
            # Add a small delay before boss appears
            pygame.time.delay(500)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_state == "START_SCREEN":
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.playing = False
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.selected_level = max(1, self.selected_level - 1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.selected_level = min(self.max_level, self.selected_level + 1)
                    elif event.key == pygame.K_RETURN:
                        self.playing = False
                    elif event.key == pygame.K_UP:
                        self.selected_difficulty_index = (self.selected_difficulty_index - 1) % len(self.difficulty_options)
                        self.set_difficulty(self.difficulty_options[self.selected_difficulty_index])
                    elif event.key == pygame.K_DOWN:
                        self.selected_difficulty_index = (self.selected_difficulty_index + 1) % len(self.difficulty_options)
                        self.set_difficulty(self.difficulty_options[self.selected_difficulty_index])
                elif self.game_state == "GAME_OVER":
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.playing = False
                    else:
                        self.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    if HEIGHT / 2 + 100 <= mouse_pos[1] <= HEIGHT / 2 + 140:
                        if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100:
                            self.playing = False
    def draw(self):
        # Draw animated background
        self.background.draw(self.screen)
        
        # Draw all game sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI background rectangles
        pygame.draw.rect(self.screen, (0,0,0,180), (WIDTH/2-90, 5, 180, 36), border_radius=8)
        pygame.draw.rect(self.screen, (0,0,0,180), (10, 5, 120, 60), border_radius=8)
        pygame.draw.rect(self.screen, (0,0,0,180), (WIDTH-140, 5, 130, 60), border_radius=8)
        
        # Score (center top, big)
        self.draw_text(f"Score: {self.score}", 28, YELLOW, WIDTH / 2, 10)
        # Level (top right)
        self.draw_text(f"Level: {self.current_level}", 22, WHITE, WIDTH - 75, 10)
        # Lives (top left)
        self.draw_text(f"Lives: {self.player.lives}", 22, GREEN, 70, 10)
        # Power (top left, below lives)
        self.draw_text(f"Power: {self.player.power_level}", 18, BLUE, 70, 35)
        # Difficulty (top right, below level)
        self.draw_text(f"Difficulty: {self.difficulty}", 18, RED if self.difficulty=="Hard" else (YELLOW if self.difficulty=="Medium" else GREEN), WIDTH - 75, 35)
        
        # Boss health bar
        if self.game_state == "BOSS_FIGHT" and self.boss_group.sprite:
            boss = self.boss_group.sprite
            BAR_LENGTH = 200
            BAR_HEIGHT = 18
            fill_pct = max(0, boss.health / boss.max_health)
            fill = fill_pct * BAR_LENGTH
            outline_rect = pygame.Rect(WIDTH / 2 - BAR_LENGTH / 2, 60, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pygame.Rect(WIDTH / 2 - BAR_LENGTH / 2, 60, fill, BAR_HEIGHT)
            pygame.draw.rect(self.screen, RED, fill_rect)
            pygame.draw.rect(self.screen, WHITE, outline_rect, 2)
        
        pygame.display.flip()

    def show_start_screen(self):
        self.game_state = "START_SCREEN"
        selecting_level = True

        # Card dimensions and position
        card_width = 600
        card_height = 500
        card_x = (WIDTH - card_width) // 2
        card_y = (HEIGHT - card_height) // 2 + 50 # Shift slightly down from center
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        card_color = (20, 20, 40) # Darker blue/purple for the card
        border_color = (80, 80, 100)
        border_radius = 20

        # Difficulty button positions (adjusting for the card)
        button_y = card_y + card_height * 0.6
        button_spacing = 10
        button_width = 100
        button_height = 40
        easy_button_x = card_x + card_width / 2 - button_width * 1.5 - button_spacing
        medium_button_x = card_x + card_width / 2 - button_width / 2
        hard_button_x = card_x + card_width / 2 + button_width * 0.5 + button_spacing

        # Level selection position
        level_select_y = button_y + button_height + 40

        while selecting_level and self.running:
            # Draw animated background
            self.background.draw(self.screen)
            
            # Draw the card background with rounded corners and border
            pygame.draw.rect(self.screen, border_color, card_rect, border_radius=border_radius)
            pygame.draw.rect(self.screen, card_color, card_rect.inflate(-4, -4), border_radius=border_radius - 2)

            # Draw title outside the card
            # Pulsating Title Animation
            now = pygame.time.get_ticks()
            pulse_scale = 1.0 + math.sin(now * 0.002) * 0.05 # Pulsates between 1.0 and 1.05
            title_size = int(64 * pulse_scale)
            # Ensure title size doesn't go below a minimum to avoid visual glitches if pulse_scale becomes small
            title_size = max(title_size, 56) # Minimum font size
            # Recalculate text surface for animated size
            font = pygame.font.Font(self.font_name, title_size)
            text_surface = font.render("COSMIC CLASH", True, (100, 150, 255))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 10))
            self.screen.blit(text_surface, text_rect)

            # Draw text inside the card
            self.draw_text("Welcome to Cosmic Clash", 36, (150, 180, 255), WIDTH / 2, card_y + 40) # Lighter blue/purple
            self.draw_text("A space shooter with power-ups, levels, and boss fights!", 22, WHITE, WIDTH / 2, card_y + 90)

            # Controls section
            controls_box_y = card_y + 140
            controls_box_height = 60
            pygame.draw.rect(self.screen, (30, 30, 50), (card_x + 20, controls_box_y, card_width - 40, controls_box_height), border_radius=10)
            self.draw_text("Controls", 20, WHITE, WIDTH / 2, controls_box_y + 10)
            self.draw_text("WASD or Arrow keys to move, SPACE to shoot", 24, WHITE, WIDTH / 2, controls_box_y + 35)

            # Difficulty selection text
            self.draw_text("Select Difficulty", 24, WHITE, WIDTH / 2, button_y - 30)

            # Draw difficulty buttons
            easy_button_rect = pygame.Rect(easy_button_x, button_y, button_width, button_height)
            medium_button_rect = pygame.Rect(medium_button_x, button_y, button_width, button_height)
            hard_button_rect = pygame.Rect(hard_button_x, button_y, button_width, button_height)

            # Highlight the selected difficulty
            easy_color = GREEN if self.difficulty == "Easy" else (34, 139, 34) # Darker green when not selected
            medium_color = YELLOW if self.difficulty == "Medium" else (218, 165, 32) # Darker yellow/orange
            hard_color = RED if self.difficulty == "Hard" else (139, 0, 0) # Darker red

            # Hover and Selection Animation for Difficulty Buttons
            mouse_pos = pygame.mouse.get_pos()
            hover_scale_factor = 1.1 # Scale up by 10% on hover/select

            easy_draw_rect = easy_button_rect.copy()
            medium_draw_rect = medium_button_rect.copy()
            hard_draw_rect = hard_button_rect.copy()

            # Check for hover or selection
            if easy_button_rect.collidepoint(mouse_pos) or self.difficulty == "Easy":
                easy_draw_rect.width *= hover_scale_factor
                easy_draw_rect.height *= hover_scale_factor
                easy_draw_rect.center = easy_button_rect.center
                easy_color = GREEN # Keep bright color on hover/select
            if medium_button_rect.collidepoint(mouse_pos) or self.difficulty == "Medium":
                medium_draw_rect.width *= hover_scale_factor
                medium_draw_rect.height *= hover_scale_factor
                medium_draw_rect.center = medium_button_rect.center
                medium_color = YELLOW # Keep bright color on hover/select
            if hard_button_rect.collidepoint(mouse_pos) or self.difficulty == "Hard":
                hard_draw_rect.width *= hover_scale_factor
                hard_draw_rect.height *= hover_scale_factor
                hard_draw_rect.center = hard_button_rect.center
                hard_color = RED # Keep bright color on hover/select

            pygame.draw.rect(self.screen, easy_color, easy_draw_rect, border_radius=8)
            pygame.draw.rect(self.screen, medium_color, medium_draw_rect, border_radius=8)
            pygame.draw.rect(self.screen, hard_color, hard_draw_rect, border_radius=8)

            # Adjust text position slightly for scaled buttons
            self.draw_text("Easy", 20, BLACK, easy_draw_rect.centerx, easy_draw_rect.centery - 10)
            self.draw_text("Medium", 20, BLACK, medium_draw_rect.centerx, medium_draw_rect.centery - 10)
            self.draw_text("Hard", 20, BLACK, hard_draw_rect.centerx, hard_draw_rect.centery - 10)

            # Level selection text and display
            level_text = f"Select Level: {self.selected_level}"
            level_text_size = 28
            level_text_color = WHITE

            level_rect_approx = pygame.Rect(WIDTH / 2 - 150, level_select_y - 10, 300, 60) # Approximate clickable area

            # Pulsate the level text slightly
            pulse_scale_level = 1.0 + math.sin(now * 0.003) * 0.03 # Slower pulsation
            animated_level_size = int(level_text_size * pulse_scale_level)
            animated_level_size = max(animated_level_size, 24) # Minimum font size

            # Change color on hover
            if level_rect_approx.collidepoint(mouse_pos):
                 level_text_color = YELLOW # Highlight color on hover

            font_level = pygame.font.Font(self.font_name, animated_level_size)
            text_surface_level = font_level.render(level_text, True, level_text_color)
            text_rect_level = text_surface_level.get_rect(center=(WIDTH / 2, level_select_y))
            self.screen.blit(text_surface_level, text_rect_level)

            self.draw_text("Use LEFT/RIGHT or A/D to change level", 18, WHITE, WIDTH / 2, level_select_y + 30)
            self.draw_text("Click on the level number to start", 20, WHITE, WIDTH / 2, level_select_y + 70)

            self.draw_text("Press ESC to Quit", 18, WHITE, WIDTH / 2, HEIGHT - 30)

            pygame.display.flip()
            
            # Update background animation
            self.background.update()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    selecting_level = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        selecting_level = False
                    # Arrow key navigation for difficulty
                    elif event.key == pygame.K_UP:
                        self.selected_difficulty_index = (self.selected_difficulty_index - 1) % len(self.difficulty_options)
                        self.set_difficulty(self.difficulty_options[self.selected_difficulty_index])
                    elif event.key == pygame.K_DOWN:
                        self.selected_difficulty_index = (self.selected_difficulty_index + 1) % len(self.difficulty_options)
                        self.set_difficulty(self.difficulty_options[self.selected_difficulty_index])
                    # Level selection handled by LEFT/RIGHT or A/D
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.selected_level = max(1, self.selected_level - 1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.selected_level = min(self.max_level, self.selected_level + 1)
                    # Select difficulty/start game with ENTER
                    elif event.key == pygame.K_RETURN:
                        selecting_level = False
                        self.playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = event.pos
                        # Check if click is on a difficulty button
                        if easy_draw_rect.collidepoint(mouse_pos):
                            self.set_difficulty("Easy")
                            selecting_level = False
                            self.playing = False
                        elif medium_draw_rect.collidepoint(mouse_pos):
                            self.set_difficulty("Medium")
                            selecting_level = False
                            self.playing = False
                        elif hard_draw_rect.collidepoint(mouse_pos):
                            self.set_difficulty("Hard")
                            selecting_level = False
                            self.playing = False
                        # Check if click is on level selection area
                        elif level_select_y - 10 <= mouse_pos[1] <= level_select_y + 50:
                             if WIDTH / 2 - 150 <= mouse_pos[0] <= WIDTH / 2 + 150:
                                 selecting_level = False
                                 self.playing = False
            
            self.clock.tick(FPS / 2)  # Slow down the loop to avoid high CPU usage

    def show_game_over_screen(self):
        if not self.running:
            return
        self.game_state = "GAME_OVER"
        # Stop background music
        pygame.mixer.music.stop()
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"Final Score: {self.score}", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again (ESC to Quit)", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key_or_quit()

    def wait_for_key_or_quit(self):
        # This loop now primarily handles waiting in start/game over screens
        # Key handling for these states is done in self.events()
        waiting = True
        while waiting and self.running:
            self.clock.tick(FPS / 2)
            # Process events to check for key presses or quit
            self.events()
            # If playing is set to False by event handler, exit wait loop
            if not self.playing:
                 waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def spawn_enemy(self, enemy_type, pattern):
        if pattern == "top_random":
            x = random.randrange(ENEMY_WIDTH, WIDTH - ENEMY_WIDTH)
            y = random.randrange(-150, -100)
        elif pattern == "top_sides":
             x = random.choice([random.randrange(ENEMY_WIDTH, WIDTH // 4), random.randrange(WIDTH * 3 // 4, WIDTH - ENEMY_WIDTH)])
             y = random.randrange(-150, -100)
        elif pattern == "top_center_spread":
             x = WIDTH / 2 + random.randrange(-50, 50)
             y = random.randrange(-100, -80)
        else:
            x = random.randrange(ENEMY_WIDTH, WIDTH - ENEMY_WIDTH)
            y = random.randrange(-150, -100)
        Enemy(self, x, y, enemy_type)

    def player_death(self):
        if self.player.lives > 0:
            self.player.lives -= 1
            # Create an explosion at the player's position
            explosion = Explosion(self, self.player.rect.center) # Pass game instance and position
            self.all_sprites.add(explosion)
            # Hide the player and reset position, will respawn after a delay (handled in Player class update)
            self.player.hide()
            self.player.power_level = 0
            self.player.powerup_timers = []
            print(f"Player died! Lives remaining: {self.player.lives}")
            for bullet in self.enemy_bullets:
                bullet.kill()
        else:
            # If no lives left, transition to game over state after a brief delay for explosion
            explosion = Explosion(self, self.player.rect.center)
            self.all_sprites.add(explosion)
            # Small delay to show explosion before game over screen
            pygame.time.delay(500) # Adjust delay as needed
            self.player.hide()
            self.game_state = "GAME_OVER"
            self.playing = False

# --- Main Execution ---
g = Game()
while g.running:
    g.show_start_screen()
    if not g.running: break
    # Reset player state for new game after game over
    if g.game_state == "GAME_OVER":
        g.player.lives = PLAYER_LIVES
        g.player.power_level = 0
        g.player.powerup_timers = []
        g.player.hidden = False
    g.new() # Starts a new game loop
    if not g.running: break
    g.show_game_over_screen()

pygame.quit()
sys.exit()

