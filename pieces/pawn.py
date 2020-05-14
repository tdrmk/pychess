from __future__ import annotations

from utils import Player, Square, Move
from .piece import Piece


class Pawn(Piece):
	def en_passant(self):
		x, y = self.square
		if self.board.last_move:
			last_move = self.board.last_move
			enemy_piece, from_square, to_square = last_move.piece, last_move.old_square, last_move.new_square
			if isinstance(enemy_piece, Pawn) and \
					((enemy_piece.player == Player.WHITE and from_square.y == 6 and to_square.y == 4) or
					 (enemy_piece.player == Player.BLACK and from_square.y == 1 and to_square.y == 3)) \
					and y == to_square.y and abs(to_square.x - x) == 1:
				# checking the condition for en-passant
				en_passant_square = Square(to_square.x, y - 1 if self.player == Player.WHITE else y + 1)
				return Move.en_passant(self.board, self, en_passant_square, enemy_piece)

	def possible_moves(self):
		x, y = self.square
		forward_square = Square(x, y - 1) if self.player == Player.WHITE else Square(x, y + 1)
		forward_two_square = Square(x, y - 2) if self.player == Player.WHITE else Square(x, y + 2)
		right_square = Square(x + 1, y - 1) if self.player == Player.WHITE else Square(x + 1, y + 1)
		left_square = Square(x - 1, y - 1) if self.player == Player.WHITE else Square(x - 1, y + 1)

		moves = []
		if not self.moved:  # if not yet moved
			if not self.board[forward_square] and not self.board[forward_two_square]:
				# if nothing in first two squares, can move two squares
				moves.append(Move.typical(self.board, piece=self, new_square=forward_two_square))

		# promotion occurs if pawn reaches last rank
		promotion = (y - 1) == 0 if self.player == Player.WHITE else (y + 1) == 7
		if promotion:
			# note: promoted piece is determined by the player.
			if forward_square and not self.board[forward_square]:  # if nothing forward, can move one square forward
				moves.append(Move.pawn_promotion(self.board, self, forward_square, new_piece=None))
			if right_square and self.board[right_square] and self.board[right_square].player != self.player:
				moves.append(Move.pawn_promotion(self.board, self, right_square, new_piece=None))
			if left_square and self.board[left_square] and self.board[left_square].player != self.player:
				moves.append(Move.pawn_promotion(self.board, self, left_square, new_piece=None))

		else:  # if no promotion possible (typical)
			if forward_square and not self.board[forward_square]:  # if nothing forward, can move one square forward
				moves.append(Move.typical(self.board, self, forward_square))
			if right_square and self.board[right_square] and self.board[right_square].player != self.player:
				moves.append(Move.typical(self.board, self, right_square))
			if left_square and self.board[left_square] and self.board[left_square].player != self.player:
				moves.append(Move.typical(self.board, self, left_square))

		en_passant = self.en_passant()
		if en_passant:
			moves.append(en_passant)

		return moves

	def attack_squares(self):
		x, y = self.square
		right_square = Square(x + 1, y - 1) if self.player == Player.WHITE else Square(x + 1, y + 1)
		left_square = Square(x - 1, y - 1) if self.player == Player.WHITE else Square(x - 1, y + 1)
		return list(filter(
			# Either no piece or enemy piece to capture
			lambda square: square and (not self.board[square] or self.board[square].player != self.player),
			[left_square, right_square]
		))
