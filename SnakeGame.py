import curses
import re
from random import randint

# Save and load high scores from a file
def load_high_score(file_name="high_score.txt"):
    try:
        with open(file_name, "r") as file:
            content = file.read().strip()
            # Use regex to validate that the score is a number
            match = re.match(r"^\d+$", content)
            return int(content) if match else 0
    except FileNotFoundError:
        return 0

def save_high_score(score, file_name="high_score.txt"):
    with open(file_name, "w") as file:
        file.write(str(score))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = load_high_score()

    def update_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def run(self):
        curses.initscr()
        win = curses.newwin(20, 60, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)

        key = curses.KEY_RIGHT
        ESC = 27

        win.addstr(0, 2, f"High Score: {self.high_score}")
        while key != ESC:
            win.addstr(0, 2, f"Score: {self.score} High Score: {self.high_score}")
            win.timeout(150 - len(self.snake.body) // 5 + len(self.snake.body) // 10 % 120)

            prev_key = key
            event = win.getch()
            key = event if event != -1 else prev_key

            if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
                key = prev_key

            self.snake.move(key)

            # Check collisions
            if self.snake.check_collision():
                break

            # Check food
            if self.snake.body[0] == self.food.position:
                self.update_score()
                self.food.generate_new(self.snake.body)
            else:
                self.snake.remove_tail()

            # Render food and snake
            win.addch(self.food.position[0], self.food.position[1], '#')
            for segment in self.snake.body:
                win.addch(segment[0], segment[1], '*')

        curses.endwin()
        print(f"Final Score: {self.score}")
        save_high_score(self.high_score)

class Snake:
    def __init__(self):
        self.body = [(4, 10), (4, 9), (4, 8)]
        self.direction = curses.KEY_RIGHT

    def move(self, key):
        y, x = self.body[0]
        if key == curses.KEY_DOWN:
            y += 1
        if key == curses.KEY_UP:
            y -= 1
        if key == curses.KEY_LEFT:
            x -= 1
        if key == curses.KEY_RIGHT:
            x += 1

        self.body.insert(0, (y, x))
        self.direction = key

    def remove_tail(self):
        self.body.pop()

    def check_collision(self):
        head = self.body[0]
        # Check if the snake hits the wall
        if head[0] == 0 or head[0] == 19 or head[1] == 0 or head[1] == 59:
            return True
        # Check if the snake hits itself
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self):
        self.position = (10, 20)

    def generate_new(self, snake_body):
        while True:
            self.position = (randint(1, 18), randint(1, 58))
            if self.position not in snake_body:
                break

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
