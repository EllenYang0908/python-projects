import pygame
from Board import Board
from Block import Block
import pickle
import os
import time

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

# initialize the game with pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")
# Loop until the user clicks the close button.
clock = pygame.time.Clock()
fps = 25


class Game:
    def __init__(self, height, width):
        self.game = Board(height, width)
        self.height = height
        self.width = width
        # self.game = Block(20, 10)
        self.done = False
        self.counter = 0
        self.pressing_down = False
    
        self.game_state = {'score': 0, 'blocks': [...]}  # initialize game state

        self.highest_score = self.load_highest_score()
        self.score = 0

    # start the game
    def run(self) -> None:
        bk_music = pygame.mixer.Sound("back.mp3")
        bk_music.set_volume(0.5)
        bk_music.play(-1)
        over_music = pygame.mixer.Sound("over.mp3")

        while not self.done:
            if self.game.shape is None:
                self.game.new_shape()
            self.counter += 1
            if self.counter > 99999:
                self.counter = 0

            if self.counter % (fps // self.game.level // 2) == 0 or self.pressing_down:
                if self.game.state == "start":
                    self.game.go_down()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.rotate()
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = True
                    if event.key == pygame.K_LEFT:
                        self.game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        self.game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        self.game.go_space()
                    if event.key == pygame.K_ESCAPE:
                        self.game.__init__(20, 10)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.pressing_down = False
            screen.fill(WHITE)

            for i in range(self.game.height):
                for j in range(self.game.width):
                    pygame.draw.rect(screen, GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i,
                                                    self.game.zoom, self.game.zoom], 1)
                    if self.game.field[i][j] > 0:
                        pygame.draw.rect(screen, colors[self.game.field[i][j]],
                                         [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1,
                                          self.game.zoom - 2, self.game.zoom - 1])

            if self.game.shape is not None:
                shape = self.game.shape.getShape()

                for i in range(4):
                    for j in range(4):
                        # p = i * 4 + j
                        # if p in self.game.shape.image():
                        if shape[i][j]:
                            pygame.draw.rect(screen, colors[self.game.shape.color],
                                             [self.game.x + self.game.zoom * (j + self.game.shape.x) + 1,
                                              self.game.y + self.game.zoom * (i + self.game.shape.y) + 1,
                                              self.game.zoom - 2, self.game.zoom - 2])

            font = pygame.font.SysFont('Calibri', 25, True, False)
            font1 = pygame.font.SysFont('Calibri', 65, True, False)
            text = font.render("Score: " + str(self.game.score), True, BLACK)
            text_game_over = font1.render("Game Over", True, (255, 125, 0))
            text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

            screen.blit(text, [0, 0])
            if self.game.state == "gameover":
                screen.blit(text_game_over, [20, 200])
                screen.blit(text_game_over1, [25, 265])
                if self.game.game_over == 0:
                    over_music.play()
                    self.game.game_over = 1

            pygame.display.flip()
            clock.tick(fps)


    # Function to save the game state
    def save_game_state(self):
        with open('game_state.pickle', 'wb') as f:
            pickle.dump(self.game_state, f)

    # Function to load the game state
    def load_game_state(self):
        with open('game_state.pickle', 'rb') as f:
            self.game_state = pickle.load(f)

    # Function to display a pause message to the player
    def display_pause_message(self):
        print("Game paused. Press 'r' to resume.")

    # Function to pause the game loop
    def pause_game_loop(self):
        while True:
            # Wait for player to resume the game
            user_input = input("Enter 'r' to resume: ")
            if user_input == 'r':
                # Player has resumed the game, exit the pause loop
                break
    # Function to remove the pause message
    def remove_pause_message(self):
        print("\r" + " " * 100 + "\r", end="")
        # The print statement above clears the pause message from the console output

    # Function to resume the game loop
    def resume_game_loop(self):
        pass

    # Function to exit the game
    def exit_game(self):
        print("Exiting game.")
        exit()

    # Function to update the game state
    def update_game_state(self):
        pass
    # Game loop
    def game_loop(self):
        while True:
            # Get user input
            user_input = input("Enter a command (pause/resume/exit): ")
            if user_input == 'pause':
                # Save the game state and pause the game loop
                self.save_game_state()
                self.display_pause_message()
                self.pause_game_loop()
            elif user_input == 'resume':
                # Load the game state and resume the game loop
                self.load_game_state()
                self.remove_pause_message()
                self.resume_game_loop()
            elif user_input == 'exit':
                # Save the game state and exit the game
                self.save_game_state()
                self.exit_game()
            # Update game state
            self.update_game_state()


    #Socre record system
    def load_highest_score(self):
        if os.path.exists("highest_score.txt"):
            with open("highest_score.txt", "r") as f:
                return int(f.read())
        else:
            return 0

    def save_highest_score(self):
        with open("highest_score.txt", "w") as f:
            f.write(str(self.highest_score))

    def end_game(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.save_highest_score()
        pygame.quit()

    # print board on the command line
    def display(self) -> None:
        board = self.game.getView()
        for i in range(len(board)):
            print(' '.join(map(str, board[i])).replace('0', '-').replace('1', 'X'))
        print()
        
    def load_game_state(self, game_state):
        self.board = game_state["board"]
        self.current_piece = game_state["current_piece"]
        self.next_piece = game_state["next_piece"]
        self.piece_x = game_state["piece_x"]
        self.piece_y = game_state["piece_y"]
        self.score = game_state["score"]
        self.lines_cleared = game_state["lines_cleared"]
        self.level = game_state["level"]
        self.game_over = game_state["game_over"]



class TimedTetrisGame(Game):
    def __init__(self, time_limit=60):
        super().__init__()
        self.time_limit = time_limit
        self.start_time = time.time()

    def update(self):
        # Call the parent class's update method to handle falling pieces and line clearing
        super().update()

        # Check if the time limit has been reached
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.time_limit:
            self.game_over = True

    def draw_hud(self):
        # Call the parent class's draw_hud method to draw the score and level
        super().draw_hud()

        # Draw the timer on the screen
        elapsed_time = time.time() - self.start_time
        remaining_time = max(self.time_limit - elapsed_time, 0)
        time_text = f"Time: {int(remaining_time)}s"
        font = pygame.font.Font(None, 30)
        text_surface = font.render(time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (self.width - 10, self.height - 10)
        self.window.blit(text_surface, text_rect)

class SurvivalTetrisGame(Game):
    def __init__(self, move_limit=100):
        super().__init__()
        self.move_limit = move_limit
        self.move_counter = move_limit

    def update(self):
        # Call the parent class's update method to handle falling pieces and line clearing
        super().update()

        # Decrement the move counter each time a piece is placed on the board
        if self.current_piece_placed:
            self.move_counter -= 1

        # Check if the move limit has been reached
        if self.move_counter <= 0:
            self.game_over = True

    def draw_hud(self):
        # Call the parent class's draw_hud method to draw the score and level
        super().draw_hud()

        # Draw the move counter on the screen
        move_text = f"Moves: {self.move_counter}"
        font = pygame.font.Font(None, 30)
        text_surface = font.render(move_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (self.width - 10, self.height - 10)
        self.window.blit(text_surface, text_rect)


