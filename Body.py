from Graphics import Rectangle
from Graphics import Point
from Vec2 import Vec2

class Body(object):
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.force = Vec2(0,0)
    self.name = "kinematic"
    self.__type = None

  def getType(self):
    return self.__type

  def setType(self, bodyType):
    if bodyType == "static" or bodyType == "dynamic":
      self.__type = bodyType
      return
    raise ValueError("Body types must be static or dynamic.")

  def toString(self):
  	return "Body[x="+str(self.x)+", y="+str(self.y)+", w"+str(self.w)+", h"+str(self.h)+"]"