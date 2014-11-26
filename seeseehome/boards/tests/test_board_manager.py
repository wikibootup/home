from django.test import TestCase
from boards.models import Board
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from seeseehome import testdata

class BoardManagerTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_create_board(self):
        self.assertIsNotNone(
            Board.objects.create_board(
                boardname = testdata.boards_valid_name,
            )
        )

    def test_get_board(self):
        board = Board.objects.create_board(
                   boardname = testdata.boards_valid_name,
               )                    
        self.assertIsNotNone(
            Board.objects.get_board(
                id = board.id
            )
        )
    
##########
##### BOARDNAME TEST
    def test_board_name_argument_under_1_char(self):
        self.assertRaises(
            ValueError,
            Board.objects.create_board,
            boardname = testdata.boards_name_under_1_char,
        )

    def test_board_name_argument_over_30_char(self):
        self.assertRaises(
            ValidationError,
            Board.objects.create_board,
            boardname = testdata.boards_name_over_30_char,
        )

    def test_max_num_of_boards(self):
        for num in range(11):
            Board.objects.create_board(
                boardname = testdata.boards_valid_name + str(num),
            )   
        
        self.assertRaises(
            ValidationError,
            Board.objects.create_board,
            boardname = testdata.boards_valid_name,
        )
        
##########
##### RETRIEVE
    def test_get_board(self):
        board = Board.objects.create_board(
                   boardname = testdata.boards_valid_name,
               )
        board_from_get_method = Board.objects.get_board(board.id)
        self.assertEqual(board_from_get_method, board)
    
##########
##### UPDATE
    def test_update_board_name(self):
        board = Board.objects.create_board(
                   boardname = testdata.boards_old_name,
               )
        self.assertEqual(board.boardname, testdata.boards_old_name)
        Board.objects.update_board(board.id, boardname = testdata.boards_new_name)
        updated_board = Board.objects.get_board(board.id)
        self.assertEqual(updated_board.boardname, testdata.boards_new_name)
 
    
##########
##### DELETE
    def test_update_board_name(self):
        board = Board.objects.create_board(
                   boardname = testdata.boards_old_name,
               )
        board = Board.objects.get_board(board.id)
        Board.objects.delete_board(board.id)
        self.assertEqual(None, Board.objects.get_board(board.id))
    
