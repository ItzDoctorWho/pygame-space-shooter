import pygame
import random
from settings import *

vec = pygame.math.Vector2  # For potential vector math later

class Player(pygame.sprite.Sprite):
    def __init__(self, game, color=BLUE):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = self.game.assets.get("player", pygame.Surface([int(PLAYER_WIDTH * 1.5), int(PLAYER_HEIGHT * 1.5)]))
        if "player" not in self.game.assets:
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_delay_base = PLAYER_SHOOT_DELAY_BASE
        self.last_shot = pygame.time.get_ticks()
        self.power_level = 0
        self.powerup_timers = []
        self.lives = PLAYER_LIVES
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.current_player_vel = PLAYER_VEL  # Base velocity

    def update(self):
        # Debug: Check if update is called
        print("Player update called")

        if self.hidden:
            if pygame.time.get_ticks() - self.hide_timer > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
            return

        # Reset speeds each frame
        self.speed_x = 0
        self.speed_y = 0

        # Get keyboard state (support both WASD and arrow keys)
        keystate = pygame.key.get_pressed()
        
        # Debug: Check if keys are pressed and speeds are set
        if keystate[pygame.K_LEFT]:
            print("Key LEFT pressed")
            self.speed_x = -3
        if keystate[pygame.K_RIGHT]:
            print("Key RIGHT pressed")
            self.speed_x = 3
        if keystate[pygame.K_UP]:
            print("Key UP pressed")
            self.speed_y = -3
        if keystate[pygame.K_DOWN]:
            print("Key DOWN pressed")
            self.speed_y = 3

        # Normalize diagonal movement
        if self.speed_x != 0 and self.speed_y != 0:
            diagonal_factor = 0.7071  # 1/sqrt(2)
            self.speed_x *= diagonal_factor
            self.speed_y *= diagonal_factor

        # Debug: Check final speed values
        if self.speed_x != 0 or self.speed_y != 0:
            print(f"Final speed: ({self.speed_x:.2f}, {self.speed_y:.2f})")

        # Increase player speed based on power level
        current_player_vel = PLAYER_VEL + (self.power_level * 0.5)

        # Apply movement based on calculated speed and direction
        self.rect.x += self.speed_x * current_player_vel * self.game.dt
        self.rect.y += self.speed_y * current_player_vel * self.game.dt

        # Keep player on screen (adjusted for larger size)
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(HEIGHT // 2, min(HEIGHT - self.rect.height, self.rect.y))

        # Automatic shooting
        now = pygame.time.get_ticks()
        current_shoot_delay = self.shoot_delay_base / (1 + self.power_level * 0.2)
        if now - self.last_shot > current_shoot_delay:
            self.shoot()

        # Update power level
        expired_count = 0
        remaining_timers = []
        for timer_end in self.powerup_timers:
            if now < timer_end:
                remaining_timers.append(timer_end)
            else:
                expired_count += 1
        if expired_count > 0:
            self.power_level = max(0, self.power_level - expired_count)
            self.powerup_timers = remaining_timers
            self.current_player_vel = PLAYER_VEL + (self.power_level * 1.5)

    def shoot(self):
        if self.hidden:
            return
        now = pygame.time.get_ticks()
        self.last_shot = now
        offset = int(5 * 1.5)
        if self.power_level == 0:
            Bullet(self.game, self.rect.centerx, self.rect.top)
        elif self.power_level == 1:
            Bullet(self.game, self.rect.left + offset, self.rect.centery)
            Bullet(self.game, self.rect.right - offset, self.rect.centery)
        elif self.power_level >= 2:
            Bullet(self.game, self.rect.left + offset, self.rect.centery)
            Bullet(self.game, self.rect.centerx, self.rect.top)
            Bullet(self.game, self.rect.right - offset, self.rect.centery)

    def collect_powerup(self):
        if self.hidden:
            return
        if self.power_level < PLAYER_MAX_POWER_LEVEL:
            self.power_level += 1
        self.powerup_timers.append(pygame.time.get_ticks() + PLAYER_POWERUP_DURATION)
        self.powerup_timers.sort()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_type="basic"):
        super().__init__(game.all_sprites, game.enemies)
        self.game = game
        self.enemy_type = enemy_type
        self.diff_mult = self.game.difficulty_multipliers
        image_key = f"enemy_{enemy_type}"
        self.image = self.game.assets.get(image_key, pygame.Surface([int(ENEMY_WIDTH * 1.5), int(ENEMY_HEIGHT * 1.5)]))
        if image_key not in self.game.assets:
            if enemy_type == "basic":
                self.image.fill(GREEN)
            elif enemy_type == "zigzag":
                self.image.fill(TEAL)
            elif enemy_type == "shooter":
                self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = ENEMY_VEL_BASE * self.diff_mult["enemy_speed_mult"] * self.game.time_based_difficulty_multiplier
        self.speed_x = 0
        self.last_shot = pygame.time.get_ticks()
        self.base_shoot_delay = ENEMY_SHOOT_DELAY_BASE + random.randrange(-300, 300)
        self.shoot_delay = self.base_shoot_delay * self.diff_mult["enemy_shoot_delay_mult"]
        if self.enemy_type == "zigzag":
            self.base_speed_x = random.choice([-2, 2]) * (ENEMY_VEL_BASE / 1.5)
            self.speed_x = self.base_speed_x * self.diff_mult["enemy_speed_mult"]
        elif self.enemy_type == "shooter":
            self.vel_y *= 0.7

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.speed_x
        if self.enemy_type == "zigzag":
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speed_x *= -1
        elif self.enemy_type == "shooter":
            if self.rect.top > random.randrange(50, 150):
                self.vel_y = 0
            if self.vel_y == 0 and self.rect.bottom > 0:
                self.shoot()
        if self.rect.top > HEIGHT + 10 or self.rect.left < -int(ENEMY_WIDTH * 1.5) - 5 or self.rect.right > WIDTH + int(ENEMY_WIDTH * 1.5) + 5:
            self.game.score += ENEMY_SKIP_SCORE
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            EnemyBullet(self.game, self.rect.centerx, self.rect.bottom)

class Boss(pygame.sprite.Sprite):
    def __init__(self, game, level, boss_type):
        super().__init__(game.all_sprites, game.boss_group)
        self.game = game
        self.level = level
        self.boss_type = boss_type
        self.diff_mult = self.game.difficulty_multipliers
        image_key = f"boss_{boss_type.replace('_boss', '')}"
        self.image = self.game.assets.get(image_key, pygame.Surface([int(BOSS_WIDTH * 1.5), int(BOSS_HEIGHT * 1.5)]))
        if image_key not in self.game.assets:
            if boss_type == "level1_boss":
                self.image.fill(ORANGE)
            elif boss_type == "level2_boss":
                self.image.fill(PURPLE)
            elif boss_type == "level3_boss":
                self.image.fill(RED)
            elif boss_type == "level4_boss":
                self.image.fill(WHITE)
            elif boss_type == "level5_boss":
                self.image.fill(BLUE)
            elif boss_type == "final_boss":
                self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = -int(BOSS_HEIGHT * 1.5)
        self.base_speed_y = BOSS_VEL_BASE
        self.base_speed_x = BOSS_VEL_BASE * random.choice([-1.5, 1.5])
        self.speed_y = self.base_speed_y * self.diff_mult["boss_speed_mult"]
        self.speed_x = self.base_speed_x * self.diff_mult["boss_speed_mult"]
        self.health = (BOSS_HEALTH_BASE * level) * self.diff_mult["boss_health_mult"]
        self.max_health = self.health
        self.entry_complete = False
        self.base_shoot_delay = BOSS_SHOOT_DELAY_BASE
        self.shoot_delay = self.base_shoot_delay * self.diff_mult["boss_shoot_delay_mult"]
        self.last_shot = pygame.time.get_ticks()
        if self.boss_type == "level2_boss":
            self.base_shoot_delay = 750
        elif self.boss_type == "level3_boss":
            self.base_shoot_delay = 900
            self.base_speed_x *= 1.2
        elif self.boss_type == "level4_boss":
            self.base_shoot_delay = 600
        elif self.boss_type == "level5_boss":
            self.base_shoot_delay = 700
            self.health *= 1.5
        elif self.boss_type == "final_boss":
            self.health *= 2
            self.base_shoot_delay = 500
        self.health = self.health * self.diff_mult["boss_health_mult"]
        self.max_health = self.health
        self.speed_x = self.base_speed_x * self.diff_mult["boss_speed_mult"]
        self.shoot_delay = self.base_shoot_delay * self.diff_mult["boss_shoot_delay_mult"]

    def update(self):
        if not self.entry_complete:
            self.rect.y += self.speed_y
            if self.rect.top >= 20:
                self.rect.top = 20
                self.entry_complete = True
                self.speed_y = 0
        else:
            self.rect.x += self.speed_x
            if self.rect.right > WIDTH - 10:
                self.rect.right = WIDTH - 10
                self.speed_x *= -1
            if self.rect.left < 10:
                self.rect.left = 10
                self.speed_x *= -1
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            offset = int(10 * 1.5)
            if self.boss_type == "level1_boss":
                EnemyBullet(self.game, self.rect.centerx, self.rect.bottom)
            elif self.boss_type == "level2_boss":
                EnemyBullet(self.game, self.rect.left + offset, self.rect.bottom)
                EnemyBullet(self.game, self.rect.right - offset, self.rect.bottom)
            elif self.boss_type == "final_boss":
                EnemyBullet(self.game, self.rect.left + offset, self.rect.centery)
                EnemyBullet(self.game, self.rect.centerx, self.rect.bottom)
                EnemyBullet(self.game, self.rect.right - offset, self.rect.centery)
            else:
                EnemyBullet(self.game, self.rect.centerx, self.rect.bottom)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        self.image = self.game.assets.get("bullet_player", pygame.Surface([int(BULLET_WIDTH * 1.5), int(BULLET_HEIGHT * 1.5)]))
        if "bullet_player" not in self.game.assets:
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -BULLET_VEL

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.enemy_bullets)
        self.game = game
        self.diff_mult = self.game.difficulty_multipliers
        self.image = self.game.assets.get("bullet_enemy", pygame.Surface([int(BULLET_WIDTH * 1.5), int(BULLET_HEIGHT * 1.5 * 1.5)]))
        if "bullet_enemy" not in self.game.assets:
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = (BULLET_VEL * ENEMY_BULLET_VEL_MULT) * self.diff_mult["enemy_bullet_speed_mult"]

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, center):
        super().__init__(game.all_sprites, game.powerups)
        self.game = game
        self.image = self.game.assets.get("powerup", pygame.Surface([POWERUP_WIDTH, POWERUP_HEIGHT]))
        if "powerup" not in self.game.assets:
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = POWERUP_VEL

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()