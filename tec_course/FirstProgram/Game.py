"""
Interactive mini-game with PyGame:
A circle bounces inside the window.
The circle's color changes when clicking with the mouse.
The player can change its direction with the arrow keys or WASD.
Every time the circle hits a border, the player loses points.
A sound plays when bouncing.
The game ends when the score reaches zero or the user closes the window.
"""

import pygame
import random

# Initialize all PyGame modules.
pygame.init()

# Set the game window size.
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 1️⃣ Add a title to the game window
pygame.display.set_caption("Bouncing Circle Game")

# Define a list of possible colors for the circle (RGB format).
colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128)   # Purple
]

# Select a random color for the circle at the start.
circle_color = random.choice(colors)

# Create a font to display the score on screen.
font = pygame.font.SysFont("Arial", 30)

# Define the circle's radius in pixels.
radius = 30

# Place the circle in the center of the screen at the start.
x = WIDTH // 2
y = HEIGHT // 2

# Define the circle's initial speed along the x and y axes.
vel_x, vel_y = 5, 5

# Set the player's initial score.
score = 100

# 2️⃣ Load a bounce sound effect (.wav file)
bounce_sound = pygame.mixer.Sound("efecto.wav")

# Create a clock to control the frame rate (frames per second).
clock = pygame.time.Clock()

# Variable that indicates whether the game is still running.
running = True

# Main game loop. Repeats until the user closes the window or the score reaches 0.
while running:
    # Limit the game to 60 frames per second.
    clock.tick(60)
    # Draw the background (dark gray).
    screen.fill((30, 30, 30))

    # Process user events (keyboard, mouse, close window).
    for event in pygame.event.get():
        # If the user closes the window, end the game.
        if event.type == pygame.QUIT:
            running = False

        # If the user clicks the mouse, change the circle's color.
        if event.type == pygame.MOUSEBUTTONDOWN:
            circle_color = random.choice(colors)

        # If the user presses the arrow keys or WASD, they can change the circle's direction.
        if event.type == pygame.KEYDOWN:
            # UP (↑ or W)
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and vel_y > 0:
                vel_y *= -1
            # RIGHT (→ or D)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and vel_x < 0:
                vel_x *= -1
            # DOWN (↓ or S)
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and vel_y < 0:
                vel_y *= -1
            # LEFT (← or A)
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and vel_x > 0:
                vel_x *= -1

    # Move the circle by adding velocity to its position.
    x += vel_x
    y += vel_y

    # If the circle touches the left or right edges, bounce and lose points.
    if x - radius <= 0 or x + radius >= WIDTH:
        vel_x *= -1
        score -= 5
        bounce_sound.play()
        if score <= 0:
            running = False

    # If the circle touches the top or bottom edges, bounce and lose points.
    if y - radius <= 0 or y + radius >= HEIGHT:
        vel_y *= -1
        score -= 5
        bounce_sound.play()
        if score <= 0:
            running = False

    # Draw the circle on the screen.
    pygame.draw.circle(screen, circle_color, (x, y), radius)

    # Display the score in the top-left corner.
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the screen with everything drawn.
    pygame.display.update()

# 4️⃣ If the game ended because score reached zero, show "Game Over!"
if score <= 0:
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.update()
    # 5️⃣ Delay closing the window by 2 seconds.
    pygame.time.wait(2000)

# Exit the main loop when the score reaches 0 or the user closes the window.
pygame.quit()

