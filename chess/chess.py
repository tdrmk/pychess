from __future__ import annotations

from typing import TYPE_CHECKING, List

import pygame
from pygame import K_LEFT, K_RIGHT

from board import Board
from constants import BOARD_TOP, BOARD_LEFT, BOARD_HEIGHT, BOARD_WIDTH, SQUARE, STATUS_RECT, BOARD_RECT
from pieces import King, Piece
from utils import Move, Square, History
from utils import Player, Memoize
from .promotion import get_promotion_selection, draw_promotion_menu

if TYPE_CHECKING:
	from pygame import Surface
	from pygame.font import Font

cache = Memoize()


class Chess:
	def __init__(self, board: Board, turn: Player, move_history: History[Move]):
		self._board: Board = board
		self._turn: Player = turn
		self._moves_: History[Move] = move_history
		self._kings = {
			Player.WHITE: next(filter(lambda piece: isinstance(piece, King), board[Player.WHITE])),
			Player.BLACK: next(filter(lambda piece: isinstance(piece, King), board[Player.BLACK]))
		}

		# UI state
		self._selected_piece: Piece = None  # the current selected piece
		self._promotion_move: Move = None  # the pending promotion move, which needs choosing

	@property
	def turn(self) -> Player:
		return self._turn

	@cache.memoize
	def __getitem__(self, item):
		return self._board[item]

	@cache.memoize
	def _can_make_move_(self, move: Move):
		# Checks if the given move can be made,
		# move cannot be applied, if it will result in a check to the player's king
		# that is, king cannot be captured by the enemy in the next move.
		self._board.make_move(move)
		will_check = self._kings[move.player].under_check()
		self._board.undo_move(move)
		return not will_check

	@cache.memoize
	def _possible_moves_(self, piece: Piece) -> List[Move]:
		# returns valid moves the piece of the player [current turn] can make
		return [move for move in piece.possible_moves() if self._can_make_move_(move)]


	# Broken get-move and broken-castle
	@cache.memoize
	def get_move(self, piece: Piece, new_square: Square) -> Move:
		# returns the move to make if piece can move to new_square
		assert piece.player == self._turn
		possible_moves = self._possible_moves_(piece)
		for move in possible_moves:
			if move.new_square == new_square:
				return move

	@cache.invalidate
	def make_move(self, move: Move):
		assert move.player == self._turn
		# Either pawn is not promoted or if promoted new_piece MUST be specified
		assert not move.pawn_promoted or move.new_piece
		self._board.make_move(move)
		self._moves_.push(move)
		self._turn = self._turn.enemy
		print('Now turn:', self._turn)

	# History -- UNDO a move
	@cache.invalidate
	def undo_move(self):
		move = self._moves_.back()
		if move:
			self._board.undo_move(move)
			self._turn = self._turn.enemy
			return True

	# History -- REDO a move
	@cache.invalidate
	def redo_move(self):
		move = self._moves_.forward()
		if move:
			self._board.make_move(move)
			self._turn = self._turn.enemy
			return True

	################# CHESS STATUS -- CHECK, CHECKMATE and STALEMATE ###########################
	@cache.memoize
	def is_check(self):
		return self._kings[self.turn].under_check()

	@cache.memoize
	def is_checkmate(self):
		if not self.is_check():
			return False  # checkmate needs a check
		for piece in self._board[self.turn]:
			if self._possible_moves_(piece):  # If a piece can move, then not a checkmate
				return False
		return True

	@cache.memoize
	def is_stalemate(self):
		if self.is_check():  # if under check, stalemate is note possible.
			return False
		for piece in self._board[self.turn]:
			if self._possible_moves_(piece):  # If a piece can move, then not a stalemate
				return False
		return True

	def __repr__(self):
		return 'Chess(<board>, <player_turn>, <move_history>)'

	################## UI FUNCTIONS	#######################################
	def draw(self, win: Surface):
		self._board.draw(win)
		if self._selected_piece:
			self._board.highlight_circle(win, self._selected_piece.square, (255, 0, 0))
			for move in self._possible_moves_(self._selected_piece):
				if move.captured_piece or move.en_passant_pawn:
					self._board.highlight_circle(win, move.new_square, (0, 0, 255))
				else:
					self._board.highlight_circle(win, move.new_square, (0, 255, 0))
		for piece in self._board[self._turn]:
			piece.draw(win)
		for piece in self._board[self._turn.enemy]:
			piece.draw(win)

		if self._promotion_move:
			draw_promotion_menu(win, self._promotion_move.player)

	# Draws the status (CHECK, CHECKMATE or STALEMATE?) of the game!
	def draw_status(self, win: Surface, small_font: Font, large_font: Font):
		status_rect = pygame.Rect(STATUS_RECT)
		board_rect = pygame.Rect(BOARD_RECT)
		pygame.draw.rect(win, (255, 255, 255), status_rect)
		turn_surf: Surface = small_font.render(f"Turn: {self._turn}", True, (0, 0, 0))
		turn_rect: pygame.Rect = turn_surf.get_rect()
		turn_rect.midleft = status_rect.midleft
		win.blit(turn_surf, turn_rect)

		state_surf: Surface = None
		if self.is_checkmate():
			state_surf = small_font.render(f"CHECKMATE!", True, (0, 0, 0))
			game_over_font = large_font.render(f"{self._turn.enemy} WINS!", True, (10, 255, 50))
			game_over_rect = game_over_font.get_rect()
			game_over_rect.center = board_rect.center
			win.blit(game_over_font, game_over_rect)
		elif self.is_check():
			state_surf = small_font.render(f"CHECK!", True, (0, 0, 0))
		elif self.is_stalemate():
			state_surf = small_font.render(f"STALEMATE!", True, (0, 0, 0))

		if state_surf:
			state_rect: pygame.Rect = state_surf.get_rect()
			state_rect.midright = status_rect.midright
			win.blit(state_surf, state_rect)

	def handle_keypress(self, key):
		if self._promotion_move:
			return

		if key == K_LEFT:
			if self.undo_move():
				self._selected_piece = None

		elif key == K_RIGHT:
			if self.redo_move():
				self._selected_piece = None

	def handle_click(self, pos):
		if self._promotion_move:  # Handle promotion
			piece_cls = get_promotion_selection(pos)
			if piece_cls:
				self._promotion_move.new_piece = piece_cls(self._promotion_move.player, self._board)
				self.make_move(self._promotion_move)
				self._promotion_move = None
				self._selected_piece = None
			return

		pos = pos[0] - BOARD_LEFT, pos[1] - BOARD_TOP
		if 0 <= pos[0] < BOARD_WIDTH and 0 <= pos[1] < BOARD_HEIGHT:
			clicked_square = Square(pos[0] // SQUARE, pos[1] // SQUARE)
			print('CLICKED SQUARE', clicked_square, 'SELECTED PIECE:', self._selected_piece)

			if self._selected_piece:  # if piece already selected
				if self._board[clicked_square] and self._board[clicked_square].player == self._turn:
					self._selected_piece = self._board[clicked_square]  # if player's on own piece, change selection
				else:
					move = self.get_move(self._selected_piece, clicked_square)
					print('MOVE:', move)
					if move:
						if move.pawn_promoted:  # Wait for user to make a choice
							self._promotion_move = move
						else:  # Make a move if not for promotion
							self.make_move(move)
						self._selected_piece = None
			else:  # if no piece was selected, select the piece on the square (if any) if belongs to (turn's) player
				if self._board[clicked_square] and self._board[clicked_square].player == self._turn:
					self._selected_piece = self._board[clicked_square]
