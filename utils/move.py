from __future__ import annotations

import re
from collections import Counter
from contextlib import contextmanager
from typing import TYPE_CHECKING

from .player import Player
from .square import Square

if TYPE_CHECKING:
	from board import Board
	from pieces import Piece, Pawn, Rook, King
	from chess import Chess


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

	@contextmanager
	def update_notation(self, chess: Chess, indicate_enpassant: bool = False):
		# Context manager to update notation of the move.
		# Notation needs the state of the chess before applying the move (like to resolve ambiguity in pieces)
		# and after applying the move (game status like check, checkmate).

		###### BEFORE APPLYING MOVE	###########
		if self.castle_rook:  # in case of castling -- use special notation
			if self.new_square.x == 6:  # king side castling
				self.notation = 'O-O'
			else:  # self.new_square.x == 2	--  queen side castling
				self.notation = 'O-O-O'
		else:
			n_piece = self.piece.notation  # the piece, note in case of pawn, nothing
			n_square = self.new_square.notation  # the destination square
			n_captured = 'x' if self.captured_piece or self.en_passant_pawn else ''  # if capture (including enpassant)
			n_promoted = f'={self.new_piece.notation}' if self.pawn_promoted else ''  # if pawn promotion, the new piece
			n_enpassant = '(ep)' if indicate_enpassant and self.en_passant_pawn else ''  # in case of enpassant
			# if other pieces (of same type) can move to same square, `n_ambiguity` is used for resolving the piece
			n_ambiguity = ''  # if other pieces () also can move to same
			if not n_piece and n_captured:  # if pawn captures a piece, specify file
				n_piece = self.old_square.notation[0]
			elif n_piece:  # if not pawn
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

		yield
		###### AFTER APPLYING MOVE
		if chess.is_checkmate():
			self.notation += '#'
		elif chess.is_check():
			self.notation += '+'

	@classmethod
	def from_notation(cls, notation: str, chess: Chess):
		# obtain the move from the notation
		# WARNING: move must be valid -- it does not check for errors.
		import pieces
		player = chess.turn
		# Maps notation to piece.
		notation2piece = {
			'K': pieces.King,
			'Q': pieces.Queen,
			'R': pieces.Rook,
			'B': pieces.Bishop,
			'N': pieces.Knight,
			None: pieces.Pawn,
		}
		match = re.match('^O-O(?P<queen_side>-O)?[+#]?$', notation)
		if match:  # handling special case of castling.
			king = chess[pieces.King][player][0]
			if match.group('queen_side'):
				rook = chess[Square(0, king.square.y)]
				return cls.castle(chess.board, king=king, new_king_square=Square(2, king.square.y), rook=rook,
								  new_rook_square=Square(3, king.square.y))
			else:
				rook = chess[Square(7, king.square.y)]
				return cls.castle(chess.board, king=king, new_king_square=Square(6, king.square.y), rook=rook,
								  new_rook_square=Square(5, king.square.y))

		match = re.match(
			'^(?P<piece>[NBRQK])?(?P<ambiguity>[a-h]|[1-8])?(?P<captured>x)?(?P<square>[a-h][1-8])'
			'(=(?P<promoted>[NBRQ]))?(?P<enpassant>\(ep\))?([+#])?$',
			notation)
		if match:  # in case of any other move
			piece_cls = notation2piece[match.group('piece')]  # get the piece type being moved
			new_square = Square.from_notation(match.group('square'))  # get the new_square piece is intended to move
			ambiguity = match.group('ambiguity')  # get the file/rank to resolve ambiguity (if any)
			for piece in chess[piece_cls][player]:  # for each piece of the piece of specified type
				for move in piece.possible_moves():  # get all possible moves
					if move.new_square == new_square:  # if there is a match in destination square
						if not ambiguity or ambiguity in move.old_square.notation:  # if piece is the one indicated
							if match.group('promoted'):  # in case of promotion, create the new_piece
								move.new_piece = notation2piece[match.group('promoted')](player, chess.board)
							return move  # Found it
			raise NotImplementedError(f'No piece can make move {notation}.')
		raise NotImplementedError(f'Unknown Notation. Cannot parse notation {notation}.')
