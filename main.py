import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cone Ball Shooter")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Player (rectangle)
player_width = 50
player_height = 20
player_x = 370
player_y = 550
player_x_change = 0
player_speed = 0.3  # Movement speed set to 0.3 pixels per frame

# Bullets
bullet_width = 5
bullet_height = 20
bullet_y_change = 10
bullet_state = "ready"  # "ready" means bullet is not visible; "fire" means it is moving
bullet_list = []  # A list to track multiple bullets

# Enemy balls (set speed to a very slow value)
balls = [
    {"x": 400, "y": 50, "radius": 20, "speed": 0.2, "destroyed": False},
    {"x": 350, "y": 20, "radius": 20, "speed": 0.2, "destroyed": False},
    {"x": 450, "y": 20, "radius": 20, "speed": 0.2, "destroyed": False},
    {"x": 300, "y": 0, "radius": 20, "speed": 0.2, "destroyed": False},
    {"x": 500, "y": 0, "radius": 20, "speed": 0.2, "destroyed": False},
]

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, white)
    screen.blit(score, (x, y))

def show_message(message, color, x, y):
    message_font = pygame.font.Font('freesansbold.ttf', 50)
    message_surface = message_font.render(message, True, color)
    screen.blit(message_surface, (x, y))

# Function to detect collision
def is_collision(ball_x, ball_y, bullet_x, bullet_y, radius):
    distance = math.sqrt(math.pow(ball_x - bullet_x, 2) + math.pow(ball_y - bullet_y, 2))
    return distance < radius

# Function to detect player collision with balls
def player_collision(ball_x, ball_y, player_x, player_y, radius):
    distance = math.sqrt(math.pow(ball_x - player_x, 2) + math.pow(ball_y - player_y, 2))
    return distance < radius + player_width / 2  # Collision with player rectangle

# Main game loop
running = True
game_over = False
level_complete = False
while running:
    screen.fill(black)  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keypress events to toggle sliding
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            elif event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            elif event.key == pygame.K_SPACE:
                # Start firing bullets when space is pressed
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullet_list.append([bullet_x, bullet_y])  # Add the bullet to the list

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0  # Stop moving when key is released

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - player_width:
        player_x = screen_width - player_width

    # Bullet movement (all bullets in the list)
    for bullet in bullet_list[:]:
        pygame.draw.rect(screen, green, (bullet[0], bullet[1], bullet_width, bullet_height))
        bullet[1] -= bullet_y_change  # Move bullet upwards

        # Check if bullet goes off the screen
        if bullet[1] <= 0:
            bullet_list.remove(bullet)  # Remove bullet if it goes off-screen

    # Ball movement and collision detection (very slow speed)
    all_destroyed = True
    for ball in balls:
        if not ball["destroyed"]:
            all_destroyed = False
            # Move the ball down with a very slow speed (0.2)
            ball["y"] += 0.2  # Very slow speed for balls

            # Check if the ball collides with the player
            if player_collision(ball["x"], ball["y"], player_x, player_y, ball["radius"]):
                game_over = True
                break  # Exit the loop as game is over

            # Check if ball goes beyond the player's rectangle (game over condition)
            if ball["y"] > player_y + player_height:
                game_over = True
                break  # Exit the loop and end the game

            # Check if it hits the bottom of the screen (reset position)
            if ball["y"] > screen_height:
                ball["y"] = 0

            # Draw the ball
            pygame.draw.circle(screen, red, (ball["x"], ball["y"]), ball["radius"])

            # Check for bullet collision
            for bullet in bullet_list[:]:
                if is_collision(ball["x"], ball["y"], bullet[0], bullet[1], ball["radius"]):
                    bullet_list.remove(bullet)  # Remove bullet when it hits a ball
                    score_value += 5
                    ball["destroyed"] = True

    # Check if all balls are destroyed
    if all_destroyed:
        level_complete = True

    # Draw player
    pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))

    # Display score
    show_score(text_x, text_y)

    # Display "You Won!" message if level complete
    if level_complete:
        show_message("You Won!", green, 300, 250)
        pygame.display.update()
        pygame.time.wait(3000)
        running = False  # Exit the game loop

    # Display "Game Over" if collision occurs
    if game_over:
        show_message("Game Over!", red, 250, 250)
        pygame.display.update()
        pygame.time.wait(3000)
        running = False  # Exit the game loop

    pygame.display.update()