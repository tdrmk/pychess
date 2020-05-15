from __future__ import annotations

from utils import Square, Move
from .piece import Piece


class Bishop(Piece):
	def possible_moves(self):
		return list(map(lambda square: Move.typical(self.board, self, square), self.attack_squares()))

	def attack_squares(self):
		x, y = self.square
		squares = []
		for direction in [
			[Square(x - i, y - i) for i in range(1, min(x + 1, y + 1))],
			[Square(x + i, y + i) for i in range(1, min(8 - x, 8 - y))],
			[Square(x + i, y - i) for i in range(1, min(8 - x, y + 1))],
			[Square(x - i, y + i) for i in range(1, min(x + 1, 8 - y))],
		]:
			for square in direction:
				if not self.board[square]:  # if nothing in pathway
					squares.append(square)
					continue
				if self.board[square].player != self.player:  # if enemy in pathway
					squares.append(square)
				break
		return squares

	@property
	def notation(self) -> str:
		return 'B'