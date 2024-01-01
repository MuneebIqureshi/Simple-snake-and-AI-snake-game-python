
from tkinter import *
import random 
import math

# Updated variable names and appearance
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

EASY_SPEED = 300
MEDIUM_SPEED = 200
HARD_SPEED = 100

SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE_COLOR = "blue"
FOOD_COLOR = "orange"
BACKGROUND_COLOR = "white"  # Change the background color here
BUTTON_COLOR = "red"

score = 0
current_direction = 'down'
selected_difficulty = None

game_canvas = None  
game_window = None  
points_label = None  
snake_length_label = None 

# Class to design the snake 
class Snake: 
    def __init__(self): 
        self.body_size = BODY_SIZE 
        self.coordinates = [] 
        self.squares = []
        
        for _ in range(0, BODY_SIZE): 
            self.coordinates.append([0, 0])

        for x, y in self.coordinates: 
            circle = game_canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake") 
            self.squares.append(circle)

# Generating food at random 
class Food: 
    def __init__(self): 
        x = random.randint(0, (SCREEN_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE 
        y = random.randint(0, (SCREEN_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE 
        self.coordinates = [x, y]          
        game_canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food") 
        
def initialize_window(window):
    window.title("Snake Game") 
    window.update() 

    # Make window fullscreen
    window.attributes('-fullscreen', True)

def difficulty_selection():
    global selected_difficulty
    difficulty_window = Tk()
    difficulty_window.title("Select Difficulty")

    Label(difficulty_window, text="Select Difficulty", font=('Helvetica', 20)).pack(pady=20)

    def set_difficulty(difficulty):
        global selected_difficulty
        selected_difficulty = difficulty
        difficulty_window.destroy()

    Button(difficulty_window, text="Easy", command=lambda: set_difficulty("easy"), font=('Helvetica', 15)).pack(pady=10)
    Button(difficulty_window, text="Medium", command=lambda: set_difficulty("medium"), font=('Helvetica', 15)).pack(pady=10)
    Button(difficulty_window, text="Hard", command=lambda: set_difficulty("hard"), font=('Helvetica', 15)).pack(pady=10)

    difficulty_window.mainloop()

def set_speed():
    global SPEED
    if selected_difficulty == "easy":
        SPEED = EASY_SPEED
    elif selected_difficulty == "medium":
        SPEED = MEDIUM_SPEED
    elif selected_difficulty == "hard":
        SPEED = HARD_SPEED

# Function to check the next move of snake 
def next_turn(snake, food): 
    x, y = snake.coordinates[0]
    
    if current_direction == "up": 
        y -= SPACE_SIZE 
    elif current_direction == "down": 
        y += SPACE_SIZE 
    elif current_direction == "left": 
        x -= SPACE_SIZE 
    elif current_direction == "right": 
        x += SPACE_SIZE 

    snake.coordinates.insert(0, (x, y)) 

    circle = game_canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) 
    snake.squares.insert(0, circle) 

    if x == food.coordinates[0] and y == food.coordinates[1]: 
        global score 
        score += 1

        points_label.config(text="Points:{}".format(score)) 
        snake_length_label.config(text="Length of Snake:{}".format(score+2)) 

        game_canvas.delete("food") 
        food = Food() 

    else: 
        del snake.coordinates[-1] 
        game_canvas.delete(snake.squares[-1]) 
        del snake.squares[-1] 

    if check_collisions(snake): 
        game_over() 

    else: 
        game_window.after(SPEED, next_turn, snake, food) 

# Function to control direction of snake 
def change_direction(new_direction): 
    global current_direction 

    if new_direction == 'left' and current_direction != 'right': 
        current_direction = new_direction 
    elif new_direction == 'right' and current_direction != 'left': 
        current_direction = new_direction 
    elif new_direction == 'up'and  current_direction != 'down': 
        current_direction = new_direction 
    elif new_direction == 'down' and current_direction != 'up': 
        current_direction = new_direction 

# function to check snake's collision and position 
def check_collisions(snake): 
    x, y = snake.coordinates[0] 
    if x < 0 or x >= SCREEN_WIDTH: 
        return True
    elif y < 0 or y >= SCREEN_HEIGHT: 
        return True
    for body_part in snake.coordinates[1:]: 
        if x == body_part[0] and y == body_part[1]: 
            return True
    return False

# game over function
def game_over():
    game_canvas.delete(ALL)
    game_canvas.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                            font=('Helvetica', 40), text="GAME OVER", fill="red", tag="gameover")

    # Adding a button to restart game
    restart_button = Button(game_window, text="Restart", command=restart_game, font=('Helvetica', 20), bg=BUTTON_COLOR)
    restart_button.pack(pady=20)

def restart_game():
    global score, current_direction, snake, food
    score = 0
    current_direction = 'down'

    game_canvas.delete("all")
    snake = Snake()
    food = Food()

    # Display initial labels
    points_label.config(text="Points:{}".format(score))
    points_label.pack()
    snake_length_label.config(text="Length of Snake:{}".format(score+2))

    next_turn(snake, food)

def main():
    global game_window, game_canvas, points_label, snake_length_label
    game_window = Tk()

    difficulty_selection()  # Select difficulty before starting the game
    set_speed()  # Set the speed based on the selected difficulty

    # Display of Points Scored in Game 
    points_label = Label(game_window, text="Points:{}".format(score), font=('Helvetica', 20)) 
    points_label.pack() 

    # Display length of snake 
    snake_length_label = Label(game_window, text="Length of Snake:{}".format(score+2), font=('Helvetica', 20)) 
    snake_length_label.pack() 

    game_canvas = Canvas(game_window, bg=BACKGROUND_COLOR, height=SCREEN_HEIGHT, width=SCREEN_WIDTH) 
    game_canvas.pack()

    initialize_window(game_window)

    game_window.bind("<KeyPress>", change_direction)
    game_window.bind('<Left>', lambda event: change_direction('left')) 
    game_window.bind('<Right>',lambda event: change_direction('right')) 
    game_window.bind('<Up>', lambda event: change_direction('up')) 
    game_window.bind('<Down>',lambda event: change_direction('down')) 

    snake = Snake() 
    food = Food() 

    next_turn(snake, food) 

    game_window.mainloop() 	

if __name__ == "__main__":
    main()
