from Block import Block
import pygame


class Board:

    def __init__(self, height, width):
        self.board = [[0] * 20 for _ in range(15)]

        self.level = 2
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.shape = None

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.game_over = 0
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_shape(self):
        if self.state == "start":
            self.shape = Block(2, 0)

    # check if current block is valid, see if the block intersects
    def intersects(self) -> bool:

        intersection = False
        for i in range(4):
            for j in range(4):
                shape = self.shape.getShape()
                if shape[i][j] == 0:
                    continue
                # if i * 4 + j in self.shape.image():
                if i + self.shape.y > self.height - 1 or \
                        j + self.shape.x > self.width - 1 or \
                        j + self.shape.x < 0 or \
                        self.field[i + self.shape.y][j + self.shape.x] > 0 or \
                        self.field[i + self.shape.y][j + self.shape.x] > 0:
                    intersection = True
        if intersection:
            if self.shape.is_bottom==0:
                bottom_music = pygame.mixer.Sound("bottom.mp3")
                bottom_music.play()
            self.shape.is_bottom = 1
        return intersection

    # move the block downward by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveDown(self) -> None:
        while not self.intersects():
            self.shape.y += 1
        self.shape.y -= 1
        self.dump()

    def go_down(self):
        self.shape.y += 1
        if self.intersects():
            self.shape.y -= 1
            self.dump()

    def go_side(self, dx):
        old_x = self.shape.x
        self.shape.x += dx
        if self.intersects():
            self.shape.x = old_x

    def rotate(self):
        old_rotation = self.shape.rotation
        self.shape.rotate()
        if self.intersects():
            self.shape.rotation = old_rotation

    # write current shape to the board permanently
    def dump(self) -> None:
        shape = self.shape.getShape()
        for i in range(4):
            for j in range(4):
                if shape[i][j]:
                    self.field[i + self.shape.y][j + self.shape.x] = self.shape.color
        self.break_lines()
        self.new_shape()
        if self.intersects():
            self.state = "gameover"

    # destroy a line if it is full from the bottom to the top
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    # return the current board with block on it 
    def getView(self) -> "list[list[int]]":
        tmp = [self.board[i][:] for i in range(15)]
        for i in range(4):
            for j in range(4):
                if (self.shape.x + i < 15 and
                        self.shape.y + j < 20 and
                        self.shape.y + j >= 0 and
                        self.shape.getShape()[i][j] == 1):
                    tmp[self.shape.x + i][self.shape.y + j] = 1
        return tmp
