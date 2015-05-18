import math
class Vec2(object):
	def __init__(self, x,y):
		self.x = x
		self.y = y

		self.angle = None
		self.magnitude = None

	def __add__(self, other):
		return Vec2(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Vec2(self.x-other.x, self.y-other.y)

	def __mul__(self, other):
		return Vec2(self.x * other, self.y * other)

	def toString(self):
		return "Vec2[x="+str(self.x)+", y="+str(self.y)+"]"

	def getAngle(self):
		if self.angle != None:
			return self.angle
		self.angle = math.atan2(self.y, self.x)
		return self.angle

	def dotProduct(self, other):
		return self.x * other.x + self.y * other.y

	def normL(self):
		return Vec2(self.y * -1, self.x)

	def normR(self):
		return Vec2(self.y, self.x * -1)
	
	def getMagnitude(self):
		if self.magnitude != None:
			return self.magnitude
		magnitude = math.sqrt(self.y * self.y + self.x * self.x)
		return magnitude

	def unitVector(self):
		mag = self.getMagnitude()
		return Vec2(self.x / mag, self.y / mag)
	# https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types