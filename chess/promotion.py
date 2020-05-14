from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Type

import pygame

from constants import PROMOTION_MODAL_RECT, PROMOTION_MODAL_COLOR, PROMOTION_QUEEN_RECT, PROMOTION_ROOK_RECT, \
	PROMOTION_BISHOP_RECT, PROMOTION_KNIGHT_RECT
from pieces import Queen, Rook, Bishop, Knight

if TYPE_CHECKING:
	from pygame import Surface
	from utils import Player
	from pieces import Piece


def draw_promotion_menu(win: Surface, player: Player):
	pygame.draw.rect(win, PROMOTION_MODAL_COLOR, PROMOTION_MODAL_RECT)
	win.blit(Queen.IMG[player], PROMOTION_QUEEN_RECT)
	win.blit(Rook.IMG[player], PROMOTION_ROOK_RECT)
	win.blit(Bishop.IMG[player], PROMOTION_BISHOP_RECT)
	win.blit(Knight.IMG[player], PROMOTION_KNIGHT_RECT)


def get_promotion_selection(pos: Tuple[int, int]) -> Type[Piece]:
	if pygame.Rect(PROMOTION_MODAL_RECT).collidepoint(*pos):
		if pygame.Rect(PROMOTION_QUEEN_RECT).collidepoint(*pos):
			return Queen
		elif pygame.Rect(PROMOTION_ROOK_RECT).collidepoint(*pos):
			return Rook
		elif pygame.Rect(PROMOTION_BISHOP_RECT).collidepoint(*pos):
			return Bishop
		elif pygame.Rect(PROMOTION_KNIGHT_RECT).collidepoint(*pos):
			return Knight
