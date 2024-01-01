
from tkinter import *
import random
from queue import Queue

# Updated appearance variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
EASY_SPEED = 300
MEDIUM_SPEED = 200
HARD_SPEED = 100
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE_COLOR = "blue"
AI_SNAKE_COLOR = "green"
FOOD_COLOR = "orange"
BACKGROUND_COLOR = "white"
BUTTON_COLOR = "red"
FONT_STYLE = 'Helvetica'
FONT_SIZE = 16

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # Create snake and food
        self.snake = self.create_snake()
        self.food = self.create_food()

        # Initialize game variables
        self.score = 0
        self.current_direction = 'down'
        self.speed = EASY_SPEED  # Initial speed
        self.difficulty_selected = False

        # Display initial labels
        self.points_label = Label(master, text="Points:{}".format(self.score), font=(FONT_STYLE, FONT_SIZE), bg=BACKGROUND_COLOR)
        self.points_label.pack()

        self.snake_length_label = Label(master, text="Length of Snake:{}".format(len(self.snake)), font=(FONT_STYLE, FONT_SIZE), bg=BACKGROUND_COLOR)
        self.snake_length_label.pack()

        # Difficulty selection buttons
        self.easy_button = Button(master, text="Easy", command=lambda: self.set_difficulty(EASY_SPEED), font=(FONT_STYLE, FONT_SIZE), bg=BUTTON_COLOR)
        self.easy_button.pack(pady=10)

        self.medium_button = Button(master, text="Medium", command=lambda: self.set_difficulty(MEDIUM_SPEED), font=(FONT_STYLE, FONT_SIZE), bg=BUTTON_COLOR)
        self.medium_button.pack(pady=10)

        self.hard_button = Button(master, text="Hard", command=lambda: self.set_difficulty(HARD_SPEED), font=(FONT_STYLE, FONT_SIZE), bg=BUTTON_COLOR)
        self.hard_button.pack(pady=10)

        # Set up key bindings
        self.master.bind("<Key>", self.change_direction)

    def create_snake(self):
        # Create initial snake with two blocks
        x, y = 100, 100
        snake = [self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)]

        return snake

    def create_food(self):
        # Create initial food at a random position
        x = random.randint(0, (SCREEN_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (SCREEN_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        food = self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR)

        return food

    def set_difficulty(self, speed):
        # Set the game speed based on the selected difficulty
        self.speed = speed
        self.difficulty_selected = True

        # Remove difficulty selection buttons
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.hard_button.pack_forget()

        # Start the game loop if difficulty is selected
        if self.difficulty_selected:
            self.next_turn()

    def change_direction(self, event):
        # Change direction based on user input
        if event.keysym in {'Left', 'Right', 'Up', 'Down'}:
            self.current_direction = event.keysym.lower()

    def move_snake(self):
        # Move the snake based on the current direction
        x, y = self.canvas.coords(self.snake[0])

        if self.current_direction == "up":
            y -= SPACE_SIZE
        elif self.current_direction == "down":
            y += SPACE_SIZE
        elif self.current_direction == "left":
            x -= SPACE_SIZE
        elif self.current_direction == "right":
            x += SPACE_SIZE

        self.snake.insert(0, self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR))

        # Check if the snake eats the food
        if self.canvas.coords(self.snake[0]) == self.canvas.coords(self.food):
            self.score += 1
            self.points_label.config(text="Points:{}".format(self.score))

            self.canvas.delete(self.food)
            self.food = self.create_food()
        else:
            # If the snake doesn't eat the food, remove the last block
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

        # Check for collisions
        if self.check_collisions():
            self.game_over()
        else:
            self.snake_length_label.config(text="Length of Snake:{}".format(len(self.snake)))

    def move_ai_snake(self):
        # AI logic to move the snake towards the food using BFS
        head_coords = self.canvas.coords(self.snake[0])
        food_coords = self.canvas.coords(self.food)

        destination = self.find_path(head_coords[0], head_coords[1], food_coords[0], food_coords[1])

        if destination:
            x, y = destination
            self.snake.insert(0, self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=AI_SNAKE_COLOR))

            # Check if the AI snake eats the food
            if self.canvas.coords(self.snake[0]) == food_coords:
                self.canvas.delete(self.food)
                self.food = self.create_food()
            else:
                # If the AI snake doesn't eat the food, remove the last block
                self.canvas.delete(self.snake[-1])
                self.snake.pop()

    def find_path(self, start_x, start_y, goal_x, goal_y):
        # BFS algorithm to find the shortest path from start to goal
        visited = set()
        q = Queue()
        q.put((start_x, start_y, []))

        while not q.empty():
            x, y, path = q.get()

            if (x, y) == (goal_x, goal_y):
                return path

            if (x, y) in visited:
                continue

            visited.add((x, y))

            # Check adjacent cells
            for dx, dy in [(0, -SPACE_SIZE), (0, SPACE_SIZE), (-SPACE_SIZE, 0), (SPACE_SIZE, 0)]:
                new_x, new_y = x + dx, y + dy

                if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT and (new_x, new_y) not in visited:
                    q.put((new_x, new_y, path + [(new_x, new_y)]))

        return None

    def check_collisions(self):
        # Check for collisions with walls and itself
        head_coords = self.canvas.coords(self.snake[0])

        if (head_coords[0] < 0 or head_coords[0] >= SCREEN_WIDTH or
            head_coords[1] < 0 or head_coords[1] >= SCREEN_HEIGHT or
            head_coords in [self.canvas.coords(segment) for segment in self.snake[1:]]):
            return True

        return False

    def game_over(self):
        # Game over logic
        self.canvas.delete(ALL)
        self.canvas.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                                font=(FONT_STYLE, 40), text="GAME OVER", fill="red", tag="gameover")

        # Adding a button to restart game
        restart_button = Button(self.master, text="Restart", command=self.restart_game, font=(FONT_STYLE, FONT_SIZE), bg=BUTTON_COLOR)
        restart_button.pack(pady=20)

    def restart_game(self):
        # Restart the game
        self.score = 0
        self.current_direction = 'down'

        self.canvas.delete("all")
        self.snake = self.create_snake()
        self.food = self.create_food()

        # Display initial labels
        self.points_label.config(text="Points:{}".format(self.score))
        self.snake_length_label.config(text="Length of Snake:{}".format(len(self.snake)))

        # Display difficulty selection buttons
        self.easy_button.pack(pady=10)
        self.medium_button.pack(pady=10)
        self.hard_button.pack(pady=10)

    def next_turn(self):
        # Game loop
        self.move_snake()
        self.move_ai_snake()

        if not self.check_collisions():
            self.master.after(self.speed, self.next_turn)

# Main loop
root = Tk()
game = SnakeGame(root)
root.mainloop()
