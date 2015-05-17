from Graphics import *
from Vec2 import Vec2
from Body import Body
import pdb

MAX_SUBNODES = 4
MAX_OBJECTS = 10
INIT_DEPTH = 100
MAX_DEPTH = 10

class QuadTree(object):

  def __init__(self, x, y, width, height, depth, surface = None):
    # Spatial partioning
    self.x = x
    self.y = y
    self.w = width
    self.h = height
    
    # Precomputed values for lazy evaluation
    self.midX = self.x + self.w/2
    self.maxX = self.x + self.w
    self.midY = self.y + self.h/2
    self.maxY = self.y + self.h
    
    # The subnodes and objects that this node contains.
    self.objects = [] * MAX_OBJECTS
    self.subNodes = [None] * MAX_SUBNODES
    self.depth = depth

    # Don't draw the gui help
    self.hasAppearance = False
    self.surface = None

    if not surface == None:
      self.surface = surface
      self.giveAppearance(surface)
      surface.add(self.text)
      surface.add(self.appearance)
  
  def toStringObjects(self):
    '''Print the nodes's objects '''

    string = ""
    for x in self.objects:
      string += x.toString()
    return string

  def giveAppearance(self, surface):
    '''Initialize the extra gui help'''

    surface.giveAppearance(self)
    self.appearance.fill = Color("white")
    self.appearance.fill.alpha = 0

    self.text = Text((self.x, self.y), "")
    self.text.color = Color("black")

    self.hasAppearance = True

  def updateAppearance(self):
    if self.hasAppearance == False:
      return
    if self.subNodes[0] is None:
      self.surface.remove(self.text)
      self.text = Text((self.x + 10, self.y + 10), str(self.objects.__len__()))
      self.surface.add(self.text)
    else:
      for x in self.subNodes:
        x.updateAppearance()

  def getBody(self, obj):
    if not isinstance(obj, Body):
      if hasattr(obj, "body"):
        return obj.body
      else: 
        raise ValueError("This object does not have a body attached to it.")
    return obj
  
  def insert(self, obj):
    body = self.getBody(obj)
    return self.insertBody(obj, body.x, body.y, body.w, body.h)
  
  def insertBody(self, obj, x, y, width, height):
    '''Adds a child node to the node, returning the depth where 
    the child was added.
    Return 0 if node insertion was unsuccessful.
    Returns the depth of the new node is successful.'''
    idx = -1
    if self.subNodes[0] != None:
      idx = self.getIndices(obj)
      if idx != -1:  
        for x in idx:
          depth = self.subNodes[x].insertBody(obj, x, y, width, height)
        return depth
      else:
        return -1

    self.objects.append(obj)
    
    if self.objects.__len__() > MAX_OBJECTS: # Make some room
      self.split()
      self.partition()
      return self.depth
    
    return self.depth
  
  def clear(self):
    for x in self.subNodes:
      if x != None:
        x.clear()
      x = None
    self.objects = []
        
  def isEmpty(self):
    return self.objects.__len__() == 0
  
  def getIndices(self, body):
    indices = [False] * 4
    if body.x + body.w < self.x or body.x > self.maxX:
      return -1

    if body.y + body.h < self.y or body.y > self.maxY:
      return -1

    topQuadrant = body.y <= self.midY
    bottomQuadrant = body.y + body.w >= self.midY
    topAndBottomQuadrant = body.y <= self.midY and body.y + body.h >= self.midY

    if topAndBottomQuadrant:
      topQuadrant = False
      bottomQuadrant = False

    # Check if object is in left and right quad
    if body.x + body.w + 1 >= self.midX and body.x - 1 <= self.midX:
      if topQuadrant:
        # 0 = bottom right
        # 1 = bottom left
        # 2 = top right
        # 3 = top left
        
        indices[2] = True
        indices[3] = True

      elif bottomQuadrant:
        indices[0] = True
        indices[1] = True

      elif topAndBottomQuadrant:
        indices[0] = True
        indices[1] = True
        indices[2] = True
        indices[3] = True

    if body.x + 1 >= self.midX:
      if topQuadrant:
        indices[2] = True
        
      elif bottomQuadrant:
        indices[0] = True

      elif topAndBottomQuadrant:
        indices[0] = True
        indices[2] = True

    elif body.x + body.w <= self.midX:
      if topQuadrant:
        indices[3] = True
        
      elif bottomQuadrant:
        indices[1] = True

      elif topAndBottomQuadrant:
        indices[3] = True
        indices[1] = True

    res = []
    x = 0
    while x < 4:
      if indices[x] == True:
        res.append(x)
      x += 1
    # if body.name == "Bobby":
    #   print "Bobby"+str(res)
    return res
      
  def split(self):
    if self.depth + 1 >= MAX_DEPTH:
      print "Error:"
      print self.toString()
      for x in self.objects:
        print x.toString()
      raise ValueError("Max depth of QuadTree reached")

    if self.hasAppearance:
      self.surface.remove(self.text)
    subWidth  = self.w/2
    subHeight = self.h/2
    # 0 = bottom right
    # 1 = bottom left
    # 2 = top right
    # 3 = top left
    self.subNodes[0] = QuadTree(self.midX, self.midY, subWidth, subHeight, self.depth+1, self.surface)
    self.subNodes[1] = QuadTree(self.x, self.midY, subWidth, subHeight, self.depth+1, self.surface)
    self.subNodes[2] = QuadTree(self.midX, self.y, subWidth, subHeight, self.depth+1, self.surface)
    self.subNodes[3] = QuadTree(self.x, self.y, subWidth, subHeight, self.depth+1, self.surface)

  def partition(self):
    # Attempt to add the existing nodes to the new QuadTree
    i = self.objects.__len__() - 1

    while i >= 0:
      # Make sure we have a Body here
      obj = self.objects.pop(i)
      body = self.getBody(obj)
      
      # Where should this Body be sent to?
      idx = self.getIndices(body)

      if idx != -1:
        for x in idx:
          self.subNodes[x].insertBody(obj, body.x, body.y, body.w, body.h)
      else:
        pass
        # print "Error" + body.toString()
        # Doesn't fit in any subnodes
      i-= 1
  
  def toString(self):
    return "QuadTree[x="+str(self.x)+", y="+str(self.y)+", w="+str(self.w)+", h="+str(self.h)+"]"

  def size(self):
    return self.objects.__len__()

  def retrieve(self, obj):
    # Find out where this object is located
    idx = self.getIndices(obj)

    possibleCollisions = []

    # If the specified index is a subnode
    if idx != -1 and self.subNodes[0] != None:
        # Recursive call
        for x in idx:
          possibleCollisions += self.subNodes[x].retrieve(obj)
          
    elif self.subNodes[0] == None:
      possibleCollisions += self.objects
    
    return possibleCollisions