import pygame

import chess
import constants
import pieces


def game():
	pygame.init()
	win: pygame.Surface = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))
	small_font = pygame.font.Font(None, constants.FONT_SIZE_SMALL)
	large_font = pygame.font.Font(None, constants.FONT_SIZE_LARGE)
	pygame.display.set_caption('Chess')
	clock = pygame.time.Clock()

	pieces.load_images()
	chess_instance = chess.from_initial()
	run = True
	while run:
		chess_instance.draw(win, small_font)
		chess_instance.draw_status(win, small_font, large_font)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT or \
					(event.type == pygame.KEYDOWN and event.key == pygame.K_q):
				run = False

			if event.type == pygame.KEYDOWN:
				chess_instance.handle_keypress(key=event.key)

			if event.type == pygame.MOUSEBUTTONDOWN:
				chess_instance.handle_click(pos=event.pos)
		clock.tick(constants.FPS)
	pygame.quit()


if __name__ == '__main__':
	game()
