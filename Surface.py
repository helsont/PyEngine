from Graphics import *
from Myro import *

class Surface(object):
	def __init__(self, name, width, height, layers = 1):
		self.name = name
		self.w = width
		self.h = height
		self.window = Window(name, width, height)
		self.window.mode = 'manual'
		self.numLayers = layers
		self.layers = [None] * layers
		
		if hasattr(layers, "len"):
			self.layers = layers
		else:
			# No python 'for range' loops in this code.
			i = 0
			while i < layers:
				self.layers[i] = Layer(0, 0, width, height, self)
				i += 1

	def giveAppearance(self, body):
		body.appearance = Rectangle(Point(body.x, body.y), Point(body.x + body.w, body.y + body.h))

	def add(self, obj):
		if not hasattr(obj, "appearance"):
			obj.draw(self.window)
		else:
			obj.appearance.draw(self.window)
		# self.layers[-1].add(obj)
	
	def remove(self, obj):
		pass

	def getWidth(self):
		return self.w

	def getHeight(self):
		return self.h

	def clear(self):
		sq = Rectangle((0, 0), (self.w, self.h))
		sq.color = Color("white")
		sq.outline = None
		sq.draw(self.window)

	def update(self):
		self.window.update()
		# Line((0, 0), (100, 100)).draw(self.window)
		# self.clear()
		# for x in self.layers:
		# x.paint()
		# 
		# 
		pass
class Layer(object):
	def __init__(self, x, y, width, height, surface):
		self.objects = []
		self.x = x
		self.y = y
		self.w = width
		self.h = height
		self.maxX = self.x + width
		self.maxY = self.y + height
		self.surface = surface

	def add(self, obj):
		self.objects.append(obj)

	def remove(self, obj):
		self.objects.remove(obj)

	def paint(self):
		for i in self.objects:
			x = i.x
			y = i.y
			if hasattr(i, "appearance"):
				i.appearance.draw(self.surface.window)
			else:
				i.draw(self.surface.window)

	def clearLayer(self):
		sq = Rectangle((self.x, self.y), (self.maxX, self.maxY))
		sq.color = "white"
		sq.outline = None
		sq.draw(self.surface.window)