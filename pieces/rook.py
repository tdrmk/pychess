from __future__ import annotations

from utils import Square, Move
from .piece import Piece


class Rook(Piece):
	def possible_moves(self):
		return list(map(lambda square: Move.typical(self.board, self, square), self.attack_squares()))

	def attack_squares(self):
		x, y = self.square
		squares = []
		for direction in [
			[Square(i, y) for i in reversed(range(0, x))],
			[Square(i, y) for i in range(x + 1, 8)],
			[Square(x, j) for j in reversed(range(0, y))],
			[Square(x, j) for j in range(y + 1, 8)],
		]:
			for square in direction:
				if not self.board[square]:  # if nothing in pathway
					squares.append(square)
					continue
				if self.board[square].player != self.player:  # if enemy in pathway
					squares.append(square)
				break
		return squares
