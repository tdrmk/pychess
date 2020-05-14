from __future__ import annotations

from utils import Square, Move
from .piece import Piece


class Knight(Piece):
	def possible_moves(self):
		return list(map(lambda square: Move.typical(self.board, self, square), self.attack_squares()))

	def attack_squares(self):
		x, y = self.square
		return list(filter(
			lambda square: square and (not self.board[square] or self.board[square].player != self.player),
			[Square(x - 1, y - 2), Square(x + 1, y - 2), Square(x - 2, y - 1), Square(x + 2, y - 1),
			 Square(x - 1, y + 2), Square(x + 1, y + 2), Square(x - 2, y + 1), Square(x + 2, y + 1)]
		))
