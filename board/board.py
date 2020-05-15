from __future__ import annotations

from typing import TYPE_CHECKING, List, Set, Union, Dict, Tuple, Type

import pygame

from constants import BOARD_LEFT, BOARD_TOP, SQUARE, WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR, BOARD_MARGIN_COLOR, \
	BOARD_RECT_WITH_MARGIN, BOARD_RECT, BOARD_MARGIN
from pieces import Piece
from utils import Player, Square, Move, History

if TYPE_CHECKING:
	from pygame import Surface
	from pygame.font import Font


class Board:
	def __init__(self, moves_history: History[Move]):
		self._square_to_piece_map_: Dict[Square, Piece] = dict()
		self._piece_to_square_map_: Dict[Piece, Square] = dict()
		self._piece_moved_: Dict[Piece, bool] = dict()
		self._moves_history_ = moves_history

	def __getitem__(self, item: Union[Piece, Square, Player, Type[Piece]]) \
			-> Union[Square, Piece, List[Piece], Dict[Player, List[Piece]]]:
		if isinstance(item, Piece):  # square where piece is
			return self._piece_to_square_map_.get(item)
		elif isinstance(item, Square):  # piece on the square
			return self._square_to_piece_map_.get(item)
		elif isinstance(item, Player):  # pieces belonging to player
			return [piece for piece in self._piece_to_square_map_ if piece.player == item]
		elif issubclass(item, Piece):  # Returns the pieces of specified type on the board.
			return {
				Player.WHITE: [piece for piece in self._piece_to_square_map_
							   if isinstance(piece, item) and piece.player == Player.WHITE],
				Player.BLACK: [piece for piece in self._piece_to_square_map_
							   if isinstance(piece, item) and piece.player == Player.BLACK],
			}

	def add(self, piece: Piece, square: Square):
		self._square_to_piece_map_[square] = piece
		self._piece_to_square_map_[piece] = square

	def moved(self, piece: Piece) -> bool:
		return self._piece_moved_.get(piece)

	def make_move(self, move: Move):
		# updates the positions of (and removes) pieces on the board.
		# NOTE: Expects all the required fields for the move to be populated (including promotion)

		# Typical move
		self._piece_to_square_map_[move.piece] = move.new_square
		self._square_to_piece_map_[move.new_square] = move.piece
		del self._square_to_piece_map_[move.old_square]
		self._piece_moved_[move.piece] = True
		if move.captured_piece:  # If any captured, remove from board.
			del self._piece_to_square_map_[move.captured_piece]

		# En-passant move
		if move.en_passant_pawn:
			del self._piece_to_square_map_[move.en_passant_pawn]
			del self._square_to_piece_map_[move.en_passant_pawn_square]

		# Castle
		if move.castle_rook:
			self._piece_to_square_map_[move.castle_rook] = move.rook_new_square
			self._square_to_piece_map_[move.rook_new_square] = move.castle_rook
			del self._square_to_piece_map_[move.rook_old_square]
			self._piece_moved_[move.castle_rook] = True

		# Pawn Promotion
		if move.pawn_promoted and move.new_piece:
			del self._piece_to_square_map_[move.piece]
			self._piece_to_square_map_[move.new_piece] = move.new_square
			self._square_to_piece_map_[move.new_square] = move.new_piece
			self._piece_moved_[move.new_piece] = True

	def undo_move(self, move: Move):
		# Undo's the move, and restores pieces back to their previous positions on the board/
		# NOTE: The move must be the previously applied move on the board.

		# Typical move
		self._piece_to_square_map_[move.piece] = move.old_square
		self._square_to_piece_map_[move.old_square] = move.piece
		del self._square_to_piece_map_[move.new_square]
		self._piece_moved_[move.piece] = move.piece_moved
		if move.captured_piece:
			self._piece_to_square_map_[move.captured_piece] = move.new_square
			self._square_to_piece_map_[move.new_square] = move.captured_piece

		# En-passant move
		if move.en_passant_pawn:
			self._piece_to_square_map_[move.en_passant_pawn] = move.en_passant_pawn_square
			self._square_to_piece_map_[move.en_passant_pawn_square] = move.en_passant_pawn

		# Castle
		if move.castle_rook:
			self._piece_to_square_map_[move.castle_rook] = move.rook_old_square
			self._square_to_piece_map_[move.rook_old_square] = move.castle_rook
			del self._square_to_piece_map_[move.rook_new_square]
			self._piece_moved_[move.castle_rook] = move.rook_moved  # Not necessary, it must be false

		# Pawn Promotion
		if move.pawn_promoted and move.new_piece:
			del self._piece_to_square_map_[move.new_piece]  # remove new piece

	@property
	def last_move(self) -> Move:
		# Should board maintain the sequences of steps or the chess class?
		return self._moves_history_.top()

	def attacked_pieces(self, player: Player) -> List[Piece]:
		# Returns all (enemy) pieces under attack by pieces of `player`
		squares = set()
		for piece in self[player]:
			piece.attack_squares()
			squares.update(piece)
		pieces = []
		# Get all enemy pieces in the attacked squares of `player`
		for piece in self[player.enemy]:
			if piece.square in squares:
				pieces.append(piece)
		return pieces

	def attacked_squares(self, player: Player) -> Set[Piece]:
		# Returns all squares, where pieces of `player` can capture enemy piece.
		squares = set()
		for piece in self[player]:
			squares.update(piece.attack_squares())
		return squares

	@staticmethod
	def highlight_square(win: Surface, square: Square, color: Tuple[int, int, int], alpha=128, width=0):
		rect = pygame.Rect(BOARD_LEFT + square.x * SQUARE, BOARD_TOP + square.y * SQUARE, SQUARE, SQUARE)
		square_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
		square_surf.set_colorkey((0, 0, 0))  # color -- which will become transparent
		square_surf.set_alpha(alpha)  # 255 -- opaque
		pygame.draw.rect(square_surf, color, (0, 0, SQUARE, SQUARE), width)
		win.blit(square_surf, rect)

	@staticmethod
	def highlight_circle(win: Surface, square: Square, color: Tuple[int, int, int], alpha=128, width=0, rf=1.0):
		# rf -- radius factor -- how much to shrink the radius (0.0 to 1.0)
		rect = pygame.Rect(BOARD_LEFT + square.x * SQUARE, BOARD_TOP + square.y * SQUARE, SQUARE, SQUARE)
		square_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
		square_surf.set_colorkey((0, 0, 0))  # color -- which will become transparent
		square_surf.set_alpha(alpha)  # 255 -- opaque
		pygame.draw.circle(square_surf, color, (SQUARE // 2, SQUARE // 2), int(rf * SQUARE // 2), width)
		win.blit(square_surf, rect)

	@staticmethod
	def draw(win: Surface, font: Font):
		pygame.draw.rect(win, BLACK_SQUARE_COLOR, BOARD_RECT_WITH_MARGIN)
		pygame.draw.rect(win, WHITE_SQUARE_COLOR, BOARD_RECT, 5)
		for i in range(8):	# Ranks
			text_surf: Surface = font.render(f"{8 - i}", True, WHITE_SQUARE_COLOR)
			text_rect: pygame.Rect = text_surf.get_rect()
			text_rect.center = (BOARD_LEFT - BOARD_MARGIN // 2, BOARD_TOP + SQUARE * i + SQUARE // 2)
			win.blit(text_surf, text_rect)

		for j in range(8):	# Files
			text_surf: Surface = font.render(f"{chr(65 + j)}", True, WHITE_SQUARE_COLOR)
			text_rect: pygame.Rect = text_surf.get_rect()
			text_rect.center = (BOARD_LEFT + SQUARE * j + SQUARE // 2, BOARD_TOP + 8 * SQUARE + BOARD_MARGIN // 2)
			win.blit(text_surf, text_rect)
		for x in range(8):
			for y in range(8):
				color = BLACK_SQUARE_COLOR if (x + y) % 2 else WHITE_SQUARE_COLOR
				rect = (BOARD_LEFT + x * SQUARE, BOARD_TOP + y * SQUARE, SQUARE, SQUARE)
				pygame.draw.rect(win, color, rect)
