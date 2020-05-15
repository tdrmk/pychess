from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from board import Board
	from pieces import Piece, Pawn, Rook, King
	from chess import Chess
	from . import Square, Player


class Move:
	def __init__(self,
				 player: Player,
				 # Typical move -- with capture piece, if any
				 # Note: all moves must have these populated
				 piece: Piece,
				 old_square: Square,
				 new_square: Square,
				 piece_moved: bool,
				 captured_piece: Piece = None,
				 # En-passant move -- involves removing addition pawn (not a typical capture piece)
				 en_passant_pawn: Pawn = None,
				 en_passant_pawn_square: Square = None,
				 en_passant_pawn_moved: bool = None,
				 # Castle move -- involves moving addition rook (however no capture from additional move)
				 castle_rook: Rook = None,
				 rook_old_square: Square = None,
				 rook_new_square: Square = None,
				 rook_moved: bool = None,  # must be false for castle
				 # Pawn promotion -- involves moving pawn and replace with specified new piece (may not be known)
				 pawn_promoted: bool = None,
				 new_piece: Piece = None
				 ):
		self.player = player

		self.piece = piece
		self.old_square = old_square
		self.new_square = new_square
		self.piece_moved = piece_moved
		self.captured_piece = captured_piece  # Expected that captured piece be on new_square

		self.en_passant_pawn = en_passant_pawn
		self.en_passant_pawn_square = en_passant_pawn_square
		self.en_passant_pawn_moved = en_passant_pawn_moved  # Not required!

		self.castle_rook = castle_rook
		self.rook_old_square = rook_old_square
		self.rook_new_square = rook_new_square
		self.rook_moved = rook_moved

		self.pawn_promoted = pawn_promoted
		self.new_piece = new_piece

		self.notation = ''  # Updated before and after applying move (needs chess object to compute)

	@classmethod
	def typical(cls, board: Board, piece: Piece, new_square: Square):  # Any move (not special)
		player = piece.player
		old_square = piece.square
		piece_moved = piece.moved
		captured_piece = board[new_square]  # piece on the new board position is captured
		return cls(player, piece, old_square, new_square, piece_moved, captured_piece=captured_piece)

	@classmethod
	def en_passant(cls, board: Board, pawn: Pawn, new_square: Square, enemy_pawn: Pawn):
		player = pawn.player
		piece = pawn
		old_square = pawn.square
		piece_moved = pawn.moved

		en_passant_pawn = enemy_pawn
		en_passant_pawn_square = enemy_pawn.square
		en_passant_pawn_moved = enemy_pawn.moved

		return cls(player, piece, old_square, new_square, piece_moved, en_passant_pawn=en_passant_pawn,
				   en_passant_pawn_square=en_passant_pawn_square, en_passant_pawn_moved=en_passant_pawn_moved)

	@classmethod
	def castle(cls, board: Board, king: King, new_king_square: Square, rook: Rook, new_rook_square: Square):
		player = king.player
		piece = king
		old_square = king.square
		new_square = new_king_square
		piece_moved = king.moved

		castle_rook = rook
		rook_old_square = rook.square
		rook_new_square = new_rook_square
		rook_moved = rook.moved
		return cls(player, piece, old_square, new_square, piece_moved, castle_rook=castle_rook,
				   rook_old_square=rook_old_square, rook_new_square=rook_new_square, rook_moved=rook_moved)

	@classmethod
	def pawn_promotion(cls, board: Board, pawn: Pawn, new_square: Square, new_piece: Piece = None):
		player = pawn.player
		piece = pawn
		old_square = pawn.square
		piece_moved = pawn.moved
		captured_piece = board[new_square]
		return cls(player, piece, old_square, new_square, piece_moved, captured_piece, pawn_promoted=True,
				   new_piece=new_piece)

	def update_notation_before_move(self, chess: Chess) -> None:
		# Call this method before applying the move, to update the notation string
		# i.e. compute notations for move which are performed
		if self.castle_rook:  # castling
			self.notation = 'O-O' if self.new_square.x == 6 else 'O-O-O'  # king side or queen side
			return

		n_square = self.new_square.notation
		n_captured = 'x' if self.captured_piece or self.en_passant_pawn else ''
		n_promoted = f'={self.new_piece.notation}' if self.pawn_promoted else ''
		n_enpassant = ' e.p.' if self.en_passant_pawn else ''
		n_piece = self.piece.notation
		n_ambiguity = ''  # remove ambiguity in case if any other piece of same type can move to same square

		if not n_piece and n_captured:  # in case of pawn and a piece captured, specify file
			n_piece = self.old_square.notation[0]
		else:  # if not pawn
			# if two different pieces of the same type could move to the same square,
			# to resolve the ambiguity of which piece had moved, we use the file (x in square) or rank (y in square)
			# to uniquely identify the piece
			other_pieces = [piece for piece in chess.board[type(self.piece)][self.player] if piece != self.piece and
							any(move for move in piece.possible_moves() if move.new_square == self.new_square)]
			if other_pieces:
				counter = Counter(''.join([piece.square.notation for piece in other_pieces]))
				if self.old_square.notation[0] not in counter:
					n_ambiguity = self.old_square.notation[0]
				else:
					assert self.old_square.notation[1] not in counter
					n_ambiguity = self.old_square.notation[1]

		self.notation = f"{n_piece}{n_ambiguity}{n_captured}{n_square}{n_promoted}{n_enpassant}"

	def update_notation_after_move(self, chess: Chess) -> None:
		# Call this method after applying the move, to update the notation string
		# with respect to status of the game
		if chess.is_checkmate():
			self.notation += '#'
		elif chess.is_check():
			self.notation += '+'
