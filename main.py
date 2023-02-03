import pygame as pg
pg.font.init()
pg.init()

from tkinter import filedialog
from os import listdir

import core



class FaithWorldBuilder :
	def __init__ (self) :
		# config
		self.size, self.rez = (1000, 800), (250, 200)
		self.title = 'Faith - World Builder'
		
		self.timeMult = 1
		self.fps = 60

		# window
		self.window = pg.display.set_mode(self.size)
		self.frame  = pg.Surface(self.rez)
		self.clock  = pg.time.Clock()
		pg.display.set_caption(self.title)


	def update (self) :
		# mouse pos aligned to ratio 
		self.mousePos = pg.mouse.get_pos()
		self.mousePos = [round(self.mousePos[0]*0.25), round(self.mousePos[1]*0.25)]

		# add objects if mouse if pressed
		if self.mousePressed[1] :
			part = self.parts[self.selected]
			self.objects.append(core.Object(part['name'], self.mousePos, self.rotation))

		# add collider if mouse if pressed
		if self.mousePressed[2] : self.startedHoltingAt = self.mousePos

		if not pg.mouse.get_pressed()[2] and self.startedHoltingAt :
			self.colliders.append((
				self.startedHoltingAt[0],
				self.startedHoltingAt[1],
				self.mousePos[0]-self.startedHoltingAt[0],
				self.mousePos[1]-self.startedHoltingAt[1]))
			self.startedHoltingAt = None

		# load and save level
		keys = pg.key.get_pressed()

		if keys[pg.K_LCTRL] :
			if keys[pg.K_s] :
				self.writeLevel()
			elif keys[pg.K_o] :
				self.loadLevel()


	def render (self) :
		self.frame.fill((0, 0, 0))
		################
		# render objects
		for obj in self.objects :
			obj.render(self.frame)
			if self.showInterface : pg.draw.rect(self.frame, (0, 255, 0), (obj.pos[0], obj.pos[1], obj.img.get_width(), obj.img.get_height()), 1)

			if self.showInterface :
				pg.draw.circle(self.frame, (255, 0, 0), (obj.pos[0], obj.pos[1]), 2)
				if pg.Rect((obj.pos[0]-2, obj.pos[1]-2, 4, 4)).colliderect((self.mousePos[0], self.mousePos[1], 1, 1)) and self.mousePressed[0] :
					self.objects.remove(obj)

		# delete collider button
		if self.showInterface :
			for collider in self.colliders :
				pg.draw.rect(self.frame, (0, 0, 255), collider, 1)

				pg.draw.circle(self.frame, (255, 0, 0), (collider[0], collider[1]), 2)
				if pg.Rect((collider[0]-2, collider[1]-2, 4, 4)).colliderect((self.mousePos[0], self.mousePos[1], 1, 1)) and self.mousePressed[0] :
					self.colliders.remove(collider)

		# render selected object
		if self.showInterface : self.frame.blit(pg.transform.rotate(self.parts[self.selected]['img'], self.rotation), self.mousePos)

		# render selection rect
		if self.startedHoltingAt and self.showInterface :
			pg.draw.rect(self.frame, (0, 255, 0), (
				self.startedHoltingAt[0],
				self.startedHoltingAt[1],
				self.mousePos[0]-self.startedHoltingAt[0],
				self.mousePos[1]-self.startedHoltingAt[1]), 1)
		
		# objects menu
		surface = self.font.render(self.parts[self.selected]['name'], 0, (255, 255, 255))
		self.frame.blit(surface, (125, 0))

		################
		self.window.blit(pg.transform.scale(self.frame, self.size), (0, 0))
		self.clock.tick(self.fps)
		pg.display.flip()


	def run (self) :
		self.onStart()

		self.running = 1
		while self.running :
			self.mousePressed = [0, 0, 0]

			for event in pg.event.get() :
				if event.type == pg.QUIT :
					self.running = 0

				if event.type == pg.MOUSEBUTTONDOWN :
					self.mousePressed = pg.mouse.get_pressed()

				if event.type == pg.KEYDOWN :
					# show / hide interface
					if event.key == pg.K_w :
						if not self.showInterface : self.showInterface = 1
						elif   self.showInterface : self.showInterface = 0

					if event.key == pg.K_a and self.selected > 0 : self.selected -= 1
					if event.key == pg.K_d and self.selected < len(self.parts)-1 : self.selected += 1

					if event.key == pg.K_e : self.rotation += 90


			self.update()
			self.render()


	def loadLevel (self) :
		path = filedialog.askopenfile(mode='r', filetypes=[('Level file', '*.json')])
		content = core.loadFromJSON(path.name)

		self.colliders, self.objects = [], []

		# load object
		try : rot = obj['rot']
		except : rot = 0
		[self.objects.append(core.Object(obj['name'], obj['pos'], rot)) for obj in content['objects']]

		# load colliders
		[self.colliders.append(tuple(collider)) for collider in content['colliders']]


	def writeLevel (self) :
		path = filedialog.asksaveasfile(mode='w', defaultextension='.json')

		objects = []
		for obj in self.objects : objects.append({'name': obj.name, 'pos': obj.pos, 'rot': obj.rot})

		core.writeToJSON(path.name, {'objects': objects, 'colliders': self.colliders})


	def loadParts (self) :
		self.parts = []

		[self.parts.append({'img': pg.image.load(f'objects/{part}').convert_alpha(), 'name': part[:-4:]}) for part in listdir('objects/')]


	def onStart (self) :
		self.mousePressed = [0, 0, 0]
		self.startedHoltingAt = None
		self.showInterface = 1
		self.menuY = -25

		self.rotation = 0

		self.colliders, self.objects = [], []	

		self.font = pg.font.SysFont('Arial', 10)
		self.selected = 0

		self.loadParts()



FaithWorldBuilder().run()