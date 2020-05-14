from __future__ import annotations

from utils import Square, Move
from .piece import Piece
from .rook import Rook


class King(Piece):
	def under_check(self):
		attacked_squares = self.board.attacked_squares(self.player.enemy)
		return self.square in attacked_squares

	def king_side_castle(self):
		x, y = self.square
		if not self.moved:  # King must not have moved
			if not self.board[Square(5, y)] and not self.board[Square(6, y)] and self.board[Square(7, y)]:
				# no pieces between rook and king and rook must not have moved
				piece: Piece = self.board[Square(7, y)]
				if piece.player == self.player and isinstance(piece, Rook) and not piece.moved:
					if not self.under_check():  # NOTE: No castling under check
						return Move.castle(self.board, king=self, new_king_square=Square(6, y), rook=piece,
										   new_rook_square=Square(5, y))

	def queen_side_castle(self):
		x, y = self.square
		if not self.moved:  # King must not have moved
			if not self.board[Square(3, y)] and not self.board[Square(2, y)] and not self.board[Square(1, y)] and \
					self.board[Square(0, y)]:
				# no pieces between rook and king and rook must not have moved
				piece: Piece = self.board[Square(0, y)]
				if piece.player == self.player and isinstance(piece, Rook) and not piece.moved:
					if not self.under_check():  # NOTE: No castling under check
						return Move.castle(self.board, king=self, new_king_square=Square(2, y), rook=piece,
										   new_rook_square=Square(3, y))

	def possible_moves(self):
		x, y = self.square
		# typical one hop moves
		moves = list(map(
			lambda square: Move.typical(self.board, piece=self, new_square=square),
			filter(
				# Either no piece or enemy piece to capture
				lambda square: square and (not self.board[square] or self.board[square].player != self.player),
				(Square(x + 1, y), Square(x, y + 1), Square(x + 1, y + 1), Square(x - 1, y + 1),
				 Square(x - 1, y), Square(x, y - 1), Square(x + 1, y - 1), Square(x - 1, y - 1))
			)))

		# castling moves
		king_side_castle = self.king_side_castle()
		if king_side_castle:
			moves.append(king_side_castle)

		queen_side_castle = self.queen_side_castle()
		if queen_side_castle:
			moves.append(queen_side_castle)

		return moves

	def attack_squares(self):
		x, y = self.square
		# typical one hop moves
		return list(filter(
			# Either no piece or enemy piece to capture
			lambda square: square and (not self.board[square] or self.board[square].player != self.player),
			(Square(x + 1, y), Square(x, y + 1), Square(x + 1, y + 1), Square(x - 1, y + 1),
			 Square(x - 1, y), Square(x, y - 1), Square(x + 1, y - 1), Square(x - 1, y - 1))
		))
