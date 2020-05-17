import argparse
import os

import pygame

import chess
import constants
import pieces
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--file', default='moves.txt', help='file contains the moves to replay. default `moves.txt`')
parser.add_argument('--delay', default=100, type=int, help='delay between moves (in ms). default `1000`ms')
args = parser.parse_args()

if not os.path.exists(args.file):
	print('Specified file does not exist.')
	exit(0)

MOVES_FILE = args.file
MOVES_DELAY = args.delay

NEXT_MOVE = pygame.USEREVENT


def game():
	pygame.init()
	win: pygame.Surface = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))
	small_font = pygame.font.Font(None, constants.FONT_SIZE_SMALL)
	large_font = pygame.font.Font(None, constants.FONT_SIZE_LARGE)
	pygame.display.set_caption('Chess')
	clock = pygame.time.Clock()

	# Read the move notations from the specified file
	move_notations = utils.read_notations(MOVES_FILE)

	pieces.load_images()
	chess_instance = chess.from_initial()
	run = True
	pygame.time.set_timer(NEXT_MOVE, MOVES_DELAY)
	replay_mode = bool(move_notations)	# replay mode

	while run:
		chess_instance.draw(win, small_font)
		chess_instance.draw_status(win, small_font)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT or \
					(event.type == pygame.KEYDOWN and event.key == pygame.K_q):
				run = False
			if event.type == NEXT_MOVE:
				chess_instance.make_move(utils.Move.from_notation(move_notations[0], chess_instance))
				move_notations = move_notations[1:]
				if not move_notations:
					pygame.time.set_timer(NEXT_MOVE, 0)
					replay_mode = False

			if not replay_mode:	# Support user actions after replay is over.
				if event.type == pygame.KEYDOWN:
					chess_instance.handle_keypress(key=event.key)

				if event.type == pygame.MOUSEBUTTONDOWN:
					chess_instance.handle_click(pos=event.pos)
		clock.tick(constants.FPS)
	pygame.quit()


if __name__ == '__main__':
	game()
