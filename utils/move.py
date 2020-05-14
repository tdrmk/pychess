from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from board import Board
	from pieces import Piece, Pawn, Rook, King
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
