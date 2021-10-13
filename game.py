from board import *
from tetromino import *
from input import *
import sys


class Game:
	GRID_SIZE = 25
	GRAVITY = 200

	def __init__(self):
		self.display = pg.display.set_mode((250, 500))
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
		if self.piece.left() + amount >= 0 and self.piece.right() + amount < self.board.WIDTH:
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
				pg.draw.rect(self.display, color, rect)

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
					pg.draw.rect(self.display, get_color(x + self.piece.x, y + self.piece.y), rect)

	def draw(self):
		self.display.fill((0, 0, 0))
		self._draw_board()
		self._draw_piece()
		pg.display.flip()

	def drop(self):
		self.piece.y = self._get_piece_drop()
		self.board.add_piece(self.piece)
		self.piece = random_tetromino()

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
			self.piece = self.piece.rotate(1)
		if self.input_buffer.get('rotate right'):
			self.piece = self.piece.rotate(-1)

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
		self.draw()
		self.clock.tick(60)

	def start(self):
		while True:
			self.loop()


if __name__ == "__main__":
	pg.init()
	Game().start()
