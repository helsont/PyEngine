from Vec2 import Vec2

class Body(object):
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

    self.__points = []
    self.force = Vec2(0,0)
    self.__type = "kinematic"
    self.transform = None
    self.massData = None
    self.velocity = None
    

  def getType(self):
    return self.__type

  def getPoints(self):
    x = self.x
    y = self.y
    w = self.w
    h = self.h
    p = []
    # Middle point
    p.append(Vec2(x + w/2, y + h/2))
    # Top right, move clockwise
    p.append(Vec2(x + w , y    ))
    p.append(Vec2(x + w , y + h))
    p.append(Vec2(x     , y + h))
    p.append(Vec2(x     , y    ))
    return p
    
  def setType(self, bodyType):
    if bodyType == "static" or bodyType == "dynamic":
      self.__type = bodyType
      return
    raise ValueError("Body types must be static or dynamic.")

  def toString(self):
  	return "Body[x="+str(self.x)+", y="+str(self.y)+", w"+str(self.w)+", h"+str(self.h)+"]"