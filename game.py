from board import *
from tetromino import *
from input import *
import sys


class Game:
	GRID_SIZE = 25
	GRAVITY = 300

	def __init__(self):
		self.font = pg.font.Font('assets/font.TTF', 40)
		self.text = self.font.render("Tetris", False, (255, 255, 255))

		self.surf = pg.display.set_mode((250, 500))

		self.clock = pg.time.Clock()

		self.board = Board()
		self.piece = random_tetromino()

		self.last_gravity = pg.time.get_ticks()

		self.input_buffer = KeyMap({
			'left': Key(pg.K_LEFT),
			'right': Key(pg.K_RIGHT),
			'down': Key(pg.K_DOWN),
			'drop': Key(pg.K_SPACE),
			'rotate left': Key(pg.K_z),
			'rotate right': Key(pg.K_x),
		})

	def _shift_x(self, amount):
		if self.piece.left() + amount >= 0 and\
				self.piece.right() + amount < self.board.WIDTH and\
				not self.board.collides(self.piece, self.piece.x + amount, self.piece.y):
			self.piece.x += amount

	def _get_piece_drop(self):
		p_mask = self.piece.depth_mask()
		b_mask = self.board.height_mask(self.piece.bottom())
		tallest = 0
		for i in range(len(p_mask)):
			if i + self.piece.x >= len(b_mask) or p_mask[i] == -1:
				continue
			h = p_mask[i] + b_mask[i + self.piece.x]
			if h > tallest:
				tallest = h
		return self.board.HEIGHT - tallest

	def _draw_board(self):
		for x in range(self.board.WIDTH):
			for y in range(self.board.HEIGHT):
				rect = (x * self.GRID_SIZE, y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
				color = get_color(x, y) if self.board.get(x, y) else (0, 0, 0)
				pg.draw.rect(self.surf, color, rect)

	def _draw_piece(self):
		if self.piece is None:
			return
		for x in range(self.piece.WIDTH):
			for y in range(self.piece.HEIGHT):
				if self.piece.get(x, y):
					rect = (
						(x + self.piece.x) * self.GRID_SIZE,
						(y + self.piece.y) * self.GRID_SIZE,
						self.GRID_SIZE, self.GRID_SIZE
					)
					pg.draw.rect(self.surf, get_color(x + self.piece.x, y + self.piece.y), rect)

	def draw_tree(self):
		self.surf.fill((0, 0, 0))
		self._draw_board()
		self._draw_piece()
		self.surf.blit(self.text, (0, 0))
		pg.display.flip()

	def drop(self):
		self.piece.y = self._get_piece_drop()
		self.board.add_piece(self.piece)
		self.piece = random_tetromino()
		if self.board.collides(self.piece, self.piece.x, self.piece.y):
			pg.quit()
			sys.exit()

	def poll_input(self):
		for event in pg.event.get():
			self.input_buffer.pump(event)
			if event.type == pg.KEYDOWN and event.key == pg.K_p:
				print(self.board.height_mask())
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		self.input_buffer.poll()
		if self.input_buffer.get('left'):
			self._shift_x(-1)
		if self.input_buffer.get('right'):
			self._shift_x(1)
		if self.input_buffer.get('drop'):
			self.drop()
		if self.input_buffer.get('rotate left'):
			test = self.piece.rotate(1)
			test = self.board.bound_piece(test)
			if not self.board.collides(test, test.x, test.y):
				self.piece = test
				self.last_gravity = pg.time.get_ticks()
		if self.input_buffer.get('rotate right'):
			test = self.piece.rotate(-1)
			test = self.board.bound_piece(test)
			if not self.board.collides(test, test.x, test.y):
				self.piece = test
				self.last_gravity = pg.time.get_ticks()

	def apply_gravity(self):
		gravity = self.GRAVITY * 0.5 if self.input_buffer.is_held('down') else self.GRAVITY
		current = pg.time.get_ticks()
		if current - self.last_gravity >= gravity:
			if self._get_piece_drop() <= self.piece.y:
				self.drop()
			else:
				self.piece.y += 1
			self.last_gravity = current

	def loop(self):
		self.poll_input()
		self.apply_gravity()
		self.draw_tree()
		self.clock.tick(60)

	def start(self):
		while True:
			self.loop()


if __name__ == "__main__":
	pg.init()
	pg.font.init()
	Game().start()
