# -*- coding: utf-8 -*-
"""SnakeGame2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jIGQ5x4cIVgsi6F28Q7DpNgZx-Ft0NcY
"""

import curses
import random
import time

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor

# Get screen dimensions
sh, sw = stdscr.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(True)  # Enable keypad input
w.timeout(100)  # Initial timeout (base speed)

# Initial snake position
snake_x = sw // 4
snake_y = sh // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Function to generate food
def generate_food(w, sh, sw, snake):
    food_positions = []
    num_food = random.randint(1, 3)  # Generate 1-3 food items

    # Ensure at least one 'pi' is generated
    food_positions.append(generate_single_food(w, sh, sw, snake, curses.ACS_PI, food_positions))

    # Generate remaining food (can be 'pi' or 'y')
    for _ in range(num_food - 1):
        food_type = random.choice([curses.ACS_PI, ord('y')])
        food_positions.append(generate_single_food(w, sh, sw, snake, food_type, food_positions))

    return food_positions

# Function to generate a single food item
def generate_single_food(w, sh, sw, snake, food_type, food_positions):
    food = None
    while food is None:
        nf = [
            random.randint(1, sh - 1),
            random.randint(1, sw - 1)
        ]
        # Check if food position is valid
        food = nf if nf not in snake and nf not in [f[:2] for f in food_positions] else None
    w.addch(food[0], food[1], food_type)
    return [food[0], food[1], food_type]  # Store food type with position

# Initial food positions
food_positions = generate_food(w, sh, sw, snake)

# Initial direction
key = curses.KEY_RIGHT

# Game loop
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Check for game over conditions
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        # Display "GAME OVER!"
        game_over_str = "GAME OVER!"
        game_over_x = (sw - len(game_over_str)) // 2
        game_over_y = sh // 2
        w.addstr(game_over_y, game_over_x, game_over_str, curses.A_BOLD | curses.A_REVERSE)
        w.refresh()
        time.sleep(2)  # Pause for 2 seconds
        break  # Exit the game loop

    # Determine the new head position
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN or chr(key) == 's':
        new_head[0] += 1
    if key == curses.KEY_UP or chr(key) == 'w':
        new_head[0] -= 1
    if key == curses.KEY_LEFT or chr(key) == 'a':
        new_head[1] -= 1
    if key == curses.KEY_RIGHT or chr(key) == 'd':
        new_head[1] += 1

    # Insert the new head
    snake.insert(0, new_head)

    # Check if snake eats food
    head_x, head_y = snake[0]
    food_eaten = False  # Flag to track if food was eaten in this iteration

    for i, food_item in enumerate(food_positions):
        food_x, food_y, food_type = food_item
        if head_x == food_x and head_y == food_y:
            if food_type == ord('y'):
                # Reduce snake size to 3 (resetting score to 0)
                while len(snake) > 3:
                    tail = snake.pop()
                    w.addch(int(tail[0]), int(tail[1]), ' ')
            else:  # If food_type is curses.ACS_PI
                food_eaten = True  # Set the flag to True

            food_positions.pop(i)  # Remove the eaten food
            break  # Exit the food check loop

    # Remove the tail if food was not eaten (and if it's not a 'pi' that was just eaten)
    if not food_eaten and snake[0] not in [[f[0], f[1]] for f in food_positions]:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Regenerate food if all food items are eaten, or only 'y' is left
    if not food_positions or (food_positions and all(f[2] == ord('y') for f in food_positions)):
        # Clear existing 'y' food (if any)
        for food_item in food_positions:
            w.addch(food_item[0], food_item[1], ' ')
        # Generate new food
        food_positions = generate_food(w, sh, sw, snake)

    # Draw the snake head
    if 0 <= snake[0][0] < sh and 0 <= snake[0][1] < sw:
        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

    # Display the score (centered and larger)
    score = len(snake) - 3
    score_str = f"Score: {score}"
    score_x = (sw - len(score_str)) // 2
    w.addstr(0, score_x, score_str, curses.A_BOLD)  # Only bold, no color

    # Adjust speed based on score
    speed = 100 - (score // 5)
    speed = max(speed, 10)
    w.timeout(speed)

    # Update the screen
    w.refresh()

# Game Over screen
curses.endwin()
print("Game Over!")
print(f"Your score: {len(snake) - 3}")