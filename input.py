import pygame as pg


class Key:
	REPEAT_DELAY = 150

	def __init__(self, key):
		self.key = key
		self._pressed = False
		self._last_eat = pg.time.get_ticks()
		self._just_pressed = False

	def pump(self, event):
		if event.type == pg.KEYDOWN and event.key == self.key:
			self._pressed = True
			self._just_pressed = True
		if event.type == pg.KEYUP and event.key == self.key:
			self._pressed = False
			self._just_pressed = False

	def poll(self):
		current = pg.time.get_ticks()
		if self._just_pressed and self._pressed:
			self._just_pressed = False
			self._last_eat = current
			return True
		if current - self._last_eat >= self.REPEAT_DELAY and self._pressed:
			self._last_eat = current
			return True
		return False

	def get(self):
		return self._pressed

	def is_just_pressed(self):
		ret = self._just_pressed and self._pressed
		self.poll()
		return ret


class KeyMap:
	def __init__(self, init=None):
		if init is None:
			init = {}
		self._map = init
		self._current = {}
		self.poll()

	def pump(self, event):
		for k in self._map.values():
			k.pump(event)

	def set(self, name: str, key: Key):
		self._map[name] = key

	def poll(self):
		for k in self._map.items():
			self._current[k[0]] = k[1].poll()

	def get(self, name: str):
		return self._current[name]

	def is_just_pressed(self, name):
		return self._map[name].is_just_pressed()

	def is_held(self, name):
		return self._map[name].get()
