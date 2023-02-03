import pygame as pg



class Object :
	def __init__ (self, name, pos, rot) :
		self.img = pg.transform.rotate(pg.image.load(f'objects/{name}.png'), rot).convert_alpha()

		self.pos = pos

		self.rot = rot

		self.name = name


	def render (self, frame) :
		frame.blit(self.img, self.pos)