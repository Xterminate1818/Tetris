import pygame as pg


class Widget:
	def __init__(self, surf: pg.Surface, x=0, y=0):
		self.surf = surf
		self.surf.convert()
		self.surf.fill((255, 255, 255, 0))

		self._children = []
		self.x = x
		self.y = y

	def handle_event(self, event=None):
		for c in self._children:
			c.handle_event(event)

	def draw(self, parent: pg.Surface = None):
		self.surf.fill((255, 255, 255, 0))
		parent.blit(self.surf, (self.x, self.y))
		for c in self._children:
			c.draw(parent)

	def update(self):
		for c in self._children:
			c.update()

	def add_child(self, c):
		self._children.append(c)
