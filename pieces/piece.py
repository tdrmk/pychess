from __future__ import annotations

from typing import TYPE_CHECKING, List

from constants import SQUARE, BOARD_LEFT, BOARD_TOP
from utils import Player, Square

if TYPE_CHECKING:
	from board import Board
	from pygame import Surface, Rect
	from utils import Move


class Piece:
	def __init__(self, player: Player, board: Board):
		self._player = player
		self._board = board

	@property
	def player(self) -> Player:
		return self._player

	@property
	def board(self) -> Board:
		return self._board

	@property
	def square(self) -> Square:
		return self.board[self]

	@property
	def moved(self) -> bool:  # indicates if piece moved from it's initial square
		return self.board.moved(piece=self)

	def possible_moves(self) -> List[Move]:
		# Returns ALL possible moves the piece can take! (without considering consequences like check)
		raise NotImplemented

	def attack_squares(self):
		# Returns ALL squares where piece can capture (except en-passant).
		raise NotImplemented

	def __str__(self):
		return f'{self.player} {self.__class__.__name__} {self.square}'

	def __repr__(self):
		return f'{self.__class__.__name__}({self.player}, <board>)'

	def __hash__(self):
		return hash(id(self))

	# Necessary to set the images for the pieces (king, queen, ...) for drawing.
	IMG = {Player.WHITE: None, Player.BLACK: None}


	@property
	def notation(self) -> str:
		raise NotImplemented

	@classmethod
	def set_image(cls, white_img: Surface, black_img: Surface):
		# set the images, before attempting to draw the pieces
		cls.IMG = {Player.WHITE: white_img, Player.BLACK: black_img}

	def draw(self, win: Surface):
		img: Surface = self.IMG[self.player]
		img_rect: Rect = img.get_rect()
		img_rect.center = (BOARD_LEFT + SQUARE * self.square.x + SQUARE // 2,
						   BOARD_TOP + SQUARE * self.square.y + SQUARE // 2)
		win.blit(self.IMG[self.player], img_rect.topleft)
