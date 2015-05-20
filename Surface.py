from Graphics import *
from Myro import *
import math

RAD_TO_DEGREES = 57.2957795
BOX_ARROW_INDEX = 0
BOX_LINE_INDEX = 1
class Surface(object):
	def __init__(self, name, width, height, layers = 1):
		self.name = name
		self.w = width
		self.h = height
		self.window = Window(name, width, height)
		self.window.mode = 'manual'
		self.numLayers = layers
		self.layers = [None] * layers
		self.temporary = []

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

	def giveVectorAppearance(self, box, vector, x, y, num):
		magnitude = vector.getMagnitude()

		endX = x + vector.x + magnitude * math.cos(vector.getAngle())
		endY = y + vector.y + magnitude * math.sin(vector.getAngle())

		degrees = -RAD_TO_DEGREES * vector.getAngle()
		a = Arrow((endX, endY), degrees)

		if hasattr(box, "composite") and not box.composite[num] == None:
			# Update if the vector has an apperance (a.k.a "composite" because
			# the apperance is a grouping of two figures)
			# Update the arrow position
			arrow = box.composite[num][BOX_ARROW_INDEX]
			arrow.moveTo(endX, endY)
			
			# Update the line position
			line = box.composite[num][BOX_LINE_INDEX]
			line.setX(endX - vector.x)
			line.setY(endY - vector.y)
		else:
			if not hasattr(box, "composite") :
				# If a composite hasn't been created, create a new one.
				box.composite = [None]*4

			# Otherwise, create the individual shape for the composite.
			box.composite[num] = [a, Line(Point(x,y), Point(endX, endY))]

			# Add it to the surface to be added
			self.addComposite(box.composite)

	def addComposite(self, obj):
		for x in obj:
			if hasattr(x, "__len__"):
				self.addComposite(x)
			else:
				if not x == None:
					self.add(x)

	def add(self, obj):
		if hasattr(obj, "appearance"):
			obj.appearance.draw(self.window)
		else:
			obj.draw(self.window)
	
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