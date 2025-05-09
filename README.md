# SnakeGame

**Key Features and Fixes**

1. Random Food Generation: Generates 1-3 'pi' or 'y' food items randomly.

2. 'y' with 'pi': Ensures at least one 'pi' is generated along with 'y'.

3. Refresh on 'y' Only or When All Eaten: Refreshes with a new batch of food if only 'y' is left or if all food items have been eaten.

4. Score for 'pi': Increases the score by 1 when the snake eats 'pi'.

5. Score Reset for 'y': Resets the score to -1 when the snake eats 'y'.

6. Centered Score Display: Displays the score centered at the top in bold (default color).

7. Speed Increase: Increases the snake's speed based on the score.

8. Food Regeneration Logic: Fixed to ensure new food appears when all food is eaten or only 'y' is left.

9. Score Increase Fix: The food_eaten flag is used to prevent the snake's tail from being removed when it eats 'pi', allowing the score to increase correctly.

10. "GAME OVER!" Message: Displays a large "GAME OVER!" message in the center of the screen when the game ends.
