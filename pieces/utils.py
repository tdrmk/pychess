from __future__ import annotations

from pygame import image

import constants
from . import King, Queen, Rook, Bishop, Knight, Pawn


def load_images():
	King.set_image(image.load(constants.KING_WHITE_IMG), image.load(constants.KING_BLACK_IMG))
	Queen.set_image(image.load(constants.QUEEN_WHITE_IMG), image.load(constants.QUEEN_BLACK_IMG))
	Rook.set_image(image.load(constants.ROOK_WHITE_IMG), image.load(constants.ROOK_BLACK_IMG))
	Bishop.set_image(image.load(constants.BISHOP_WHITE_IMG), image.load(constants.BISHOP_BLACK_IMG))
	Pawn.set_image(image.load(constants.PAWN_WHITE_IMG), image.load(constants.PAWN_BLACK_IMG))
	Knight.set_image(image.load(constants.KNIGHT_WHITE_IMG), image.load(constants.KNIGHT_BLACK_IMG))
