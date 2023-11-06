import unittest
from Block import Block
from Board import Board
from Game import Game

class TestBlock(unittest.TestCase):
    def test_Block_rotateLeft(self):
        b = Block()
        original_shape = b.getShape()
        b.rotateLeft()
        self.assertNotEqual(original_shape, b.getShape())

    def test_Board_isBlockValid(self):
        board = Board()
        self.assertTrue(board.isBlockValid(0,0))
        self.assertFalse(board.isBlockValid(0,16))

    def test_Board_tryMoveDown(self):
        board = Board()
        original_x = board.shape.x
        original_y = board.shape.y
        board.tryMoveDown()
        self.assertEqual(original_x+1, board.shape.x)
        self.assertEqual(original_y, board.shape.y)

    def test_Board_dump(self):
        board = Board()
        original_board = board.board
        original_x = board.shape.x
        original_y = board.shape.y
        board.dump()
        self.assertNotEqual(original_board, board.board)
        self.assertNotEqual(original_x, board.shape.x)
        self.assertNotEqual(original_y, board.shape.y)

    def test_Game_display(self):
        game = Game()
        self.assertEqual(game.display(), None)

        
    def test_moveDown(self):
        block = Block()
        self.assertEqual(block.x, 0)
        self.assertEqual(block.y, 0)
        block.moveDown()
        self.assertEqual(block.y, 1)
        self.assertEqual(block.x, 0)
        
if __name__ == '__main__':
    unittest.main()


class BoardTestCase(unittest.TestCase):
    
    def test_isBlockValid(self):
        board = Board()
        self.assertTrue(board.isBlockValid(0, 0))
        board.shape.moveRight()
        board.shape.moveRight()
        self.assertFalse(board.isBlockValid(0, 18))
        board.shape.rotateLeft()
        self.assertFalse(board.isBlockValid(0, 0))