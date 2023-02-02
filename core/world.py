import pygame as pg



class Object :
	def __init__ (self, name, pos) :
		self.img = pg.image.load(f'objects/{name}.png').convert_alpha()

		self.pos = pos

		self.name = name


	def render (self, frame) :
		frame.blit(self.img, self.pos)