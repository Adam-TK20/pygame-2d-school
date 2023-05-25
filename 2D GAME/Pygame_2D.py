import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D-Game")

# Load background image
background_image = pygame.image.load("background.jpg").convert()

# Load character images
character_image_left = pygame.image.load("character_left.png").convert_alpha()
character_image_right = pygame.image.load("character_right.png").convert_alpha()

# Load enemy images
enemy_image_1 = pygame.image.load("enemy_1.png").convert_alpha()
enemy_image_2 = pygame.image.load("enemy_2.png").convert_alpha()

# Load collectible image
collectible_image = pygame.image.load("collectible.png").convert_alpha()

# Load sound effects
move_sound = pygame.mixer.Sound("move_sound.wav")
collect_sound = pygame.mixer.Sound("collect_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")

# Set up game variables
player_pos = [WIDTH // 2, HEIGHT - 100]
player_image = character_image_right
player_speed = 5
score = 0
lives = 3
game_over = False

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.initial_pos = (x, y)  # Store initial position

    def update(self):
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = character_image_left
            pygame.mixer.Sound.play(move_sound)
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = character_image_right
            pygame.mixer.Sound.play(move_sound)
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            pygame.mixer.Sound.play(move_sound)
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            pygame.mixer.Sound.play(move_sound)

        # Update player position
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height

# Set up player
player = Player(character_image_right, WIDTH // 2, HEIGHT - 100, player_speed)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, images, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.image = random.choice(self.images)

# Create collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Variables for enemy spawning
max_enemies = 15
spawn_counter = 0
spawn_rate = 60  # Number of frames between enemy spawns

# Create collectible
collectible = Collectible(collectible_image, random.randint(0, WIDTH), random.randint(0, HEIGHT // 2))
collectibles.add(collectible)
all_sprites.add(collectible)

clock = pygame.time.Clock()

# Start game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        player.update()

        # Update enemy positions
        enemies.update()

        # Check collision between player and enemies
        player_rect = pygame.Rect(player.rect.x, player.rect.y, 50, 50)
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                lives -= 1
                pygame.mixer.Sound.play(collision_sound)
                if lives == 0:
                    game_over = True

        # Check collision between player and collectible
        if pygame.sprite.spritecollide(player, collectibles, True):
            score += 1
            pygame.mixer.Sound.play(collect_sound)
            collectible.rect.x = random.randint(0, WIDTH - collectible.rect.width)
            collectible.rect.y = random.randint(0, HEIGHT // 2)
            collectibles.add(collectible)
            all_sprites.add(collectible)
            if score % 20 == 0:
                lives += 1

        # Spawn enemies
        spawn_counter += 1
        if spawn_counter >= spawn_rate and len(enemies) < max_enemies:
            enemy_speed = random.uniform(0.5, 1.5) + spawn_counter / 1000  # Calculate enemy speed based on time passed
            if random.random() < 0.2:  # 20% chance for a faster enemy
                enemy_speed *= 5.0
            enemy = Enemy([enemy_image_1, enemy_image_2], random.randint(0, WIDTH - enemy_image_1.get_width()), -enemy_image_1.get_height(), enemy_speed)
            enemies.add(enemy)
            all_sprites.add(enemy)
            spawn_counter = 0

        # Draw all sprites on the screen
        all_sprites.draw(screen)

        # Draw player
        screen.blit(player.image, player.rect)

        # Draw score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
    else:
        # Game over screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))

        # Restart the game if "R" key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            lives = 3
            game_over = False
            # Reset player position
            player.rect.x, player.rect.y = player.initial_pos

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
