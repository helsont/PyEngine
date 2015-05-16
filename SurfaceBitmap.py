from Graphics import *
from Myro import *
from Viewport import Viewport

class SurfaceBitmap(object):
	def __init__(self, name, width, height, layers = 1):
		self.name = name
		self.w = width
		self.h = height
		self.window = Window(name, width, height)
		self.window.mode = 'bitmapmanual'
		self.numLayers = layers
		self.layers = [None] * layers
		self.viewport = Viewport(0, 0, width, height)
		
		if hasattr(layers, "len"):
			self.layers = layers
		else:
			# No python 'for range' loops in this code.
			i = 0
			while i < layers:
				self.layers[i] = Layer(0, 0, width, height, self)
				i += 1

	def getWidth(self):
		return self.w

	def getHeight(self):
		return self.h

	def add(self, obj):
		# if not hasattr(obj, "appearance"):
			# raise ValueError(str(obj) + " does not have an 'appearance' attribute.")
		self.layers[-1].add(obj)
		# self.layers[-1].dumpNow()
	def remove(self, obj):
		for x in self.layers:
			if x.remove(obj) == True:
				return True
		return False

	def clear(self):
		sq = Rectangle((0, 0), (self.w, self.h))
		sq.color = Color("white")
		sq.outline = None
		sq.draw(self.window)

	def paint(self):
		self.clear()
		for x in self.layers:
			x.paint()
		self.window.step()

class Layer(object):
	def __init__(self, x, y, width, height, surface):
		self.objects = []
		self.x = x
		self.y = y
		self.w = width
		self.h = height
		self.maxX = self.x + self.w
		self.maxY = self.y + self.h
		self.surface = surface

	def add(self, obj):
		self.objects.append(obj)

	def remove(self, obj):
		try:
			if not self.objects.remove(obj) == None:
				return True
		except ValueError:
			pass
		
	def paint(self):
		for i in self.objects:
			x = i.x
			y = i.y
			if hasattr(i, "appearance"):
				i.appearance.draw(self.surface.window)
			else:
				i.draw(self.surface.window)
	
	def inBounds(self, obj):
		return obj.x < self. x and obj.x + obj.w > self.x + self.w and obj.y < self.y and obj.y + obj.h > self.y + self.h

	def dumpNow(self):
		dumped = 0
		for x in self.objects:
			if not self.inBounds(x):
				self.objects.remove(x)
				dumped += 1
		return dumped

	def clearLayer(self):
		sq = Rectangle((self.x, self.y), (self.maxX, self.maxY))
		sq.color = "white"
		sq.outline = None
		sq.draw(self.surface.window)