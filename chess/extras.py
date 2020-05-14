from __future__ import annotations

from board import Board
from chess import Chess
from pieces import King, Queen, Rook, Bishop, Knight, Pawn
from utils import Player, Square, History

WHITE, BLACK = Player.WHITE, Player.BLACK

INITIAL_POSITIONS = [
	# White pieces
	(Pawn, Player.WHITE, Square(0, 6)),
	(Pawn, Player.WHITE, Square(1, 6)),
	(Pawn, Player.WHITE, Square(2, 6)),
	(Pawn, Player.WHITE, Square(3, 6)),
	(Pawn, Player.WHITE, Square(4, 6)),
	(Pawn, Player.WHITE, Square(5, 6)),
	(Pawn, Player.WHITE, Square(6, 6)),
	(Pawn, Player.WHITE, Square(7, 6)),
	(Rook, Player.WHITE, Square(0, 7)),
	(Knight, Player.WHITE, Square(1, 7)),
	(Bishop, Player.WHITE, Square(2, 7)),
	(Queen, Player.WHITE, Square(3, 7)),
	(King, Player.WHITE, Square(4, 7)),
	(Bishop, Player.WHITE, Square(5, 7)),
	(Knight, Player.WHITE, Square(6, 7)),
	(Rook, Player.WHITE, Square(7, 7)),
	# Black pieces
	(Pawn, Player.BLACK, Square(0, 1)),
	(Pawn, Player.BLACK, Square(1, 1)),
	(Pawn, Player.BLACK, Square(2, 1)),
	(Pawn, Player.BLACK, Square(3, 1)),
	(Pawn, Player.BLACK, Square(4, 1)),
	(Pawn, Player.BLACK, Square(5, 1)),
	(Pawn, Player.BLACK, Square(6, 1)),
	(Pawn, Player.BLACK, Square(7, 1)),
	(Rook, Player.BLACK, Square(0, 0)),
	(Knight, Player.BLACK, Square(1, 0)),
	(Bishop, Player.BLACK, Square(2, 0)),
	(Queen, Player.BLACK, Square(3, 0)),
	(King, Player.BLACK, Square(4, 0)),
	(Bishop, Player.BLACK, Square(5, 0)),
	(Knight, Player.BLACK, Square(6, 0)),
	(Rook, Player.BLACK, Square(7, 0)),
]


def from_initial():
	# Returns a chess object with pieces at their initial positions
	history_stack = History()
	board = Board(history_stack)
	for piece_cls, player, square in INITIAL_POSITIONS:
		board.add(piece_cls(player, board), square)
	return Chess(board, Player.WHITE, history_stack)
