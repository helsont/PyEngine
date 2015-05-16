class Vec2(object):
	def __init__(self, x,y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vec2(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Vec2(self.x-other.x, self.y-other.y)

	def __mul__(self, other):
		return Vec2(self.x * other, self.y * other)

	def toString(self):
		return "Vec2[x="+str(self.x)+", y="+str(self.y)+"]"
	# https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types