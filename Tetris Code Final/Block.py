import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Block:
    def __init__(self, x: int = 0, y: int = 0):
        j_shape = [[[0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]],

                   [[1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]]]

        o_shape = [[[1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]]

        
        i_shape = [[[1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0]],
                   [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 1, 1, 1]]]
        
        z_shape = [[[1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],

                   [[0, 1, 1, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]]
        
        t_shape = [[[0, 1, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]]

        self.shapes = [j_shape, o_shape, i_shape, z_shape, t_shape]

        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.shapes) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
        self.is_bottom = 0

        # Initialize the current piece and the next piece
        self.current_piece = self.generate_random_piece()
        self.next_piece = self.generate_random_piece()

    # rotate the current block counterclockwise by 90 degree

    def rotate(self) -> None:
        # your code here
        self.rotation = (self.rotation + 1) % len(self.shapes[self.type])

    # move the current block downward by one
    def moveDown(self) -> None:
        # your code here
        self.x += 1
        return

    # move the current block rightward by one
    def moveRight(self) -> None:
        # your code here
        self.y += 1
        return

    # move the current block leftward by one 
    def moveLeft(self) -> None:
        # your code here
        self.y -= 1
        return

    # return current shape of the block
    def getShape(self) -> "list[list[int]]":
        # return self.shapes[self.type][self.current_direction]
        return self.shapes[self.type][self.rotation]
    
# Child class for special block that freezes other blocks
class FreezeBlock(Block):
    def __init__(self, x, y, freeze_time):
        super().__init__(x, y)
        self.color = "black"
        self.freeze_time = freeze_time

    def freeze_blocks(self, game_board):
        for block in game_board:
            if (block.x == self.x and block.y == self.y):
                # do not freeze the special block itself
                continue
            block.freeze(self.freeze_time)