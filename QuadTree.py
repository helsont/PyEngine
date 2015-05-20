from Graphics import *
from Vec2 import Vec2
from Body import Body

MAX_SUBNODES = 4
MAX_OBJECTS = 10
INIT_DEPTH = 100
MAX_DEPTH = 10

class QuadTree(object):
  '''QuadTree that holds objects in the leaves.'''

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

    # Default is to not draw the gui help
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

    self.text = Text((self.x + 10, self.y + 10), "")
    self.text.color = Color("black")
    
    self.hasAppearance = True

  def updateAppearance(self):
    '''Redraws the text counter if necessary.'''

    if self.hasAppearance == False:
      return
    # Only update the text for leaves (the only nodes that have text)
    if self.subNodes[0] is None and not self.text == None and not self.text.getText() == str(self.size()):
        self.text.setText(str(self.size()))
    else:
      # Update subnodes
      if not self.subNodes[0] == None:
        for x in self.subNodes:
          x.updateAppearance()

  def getBody(self, obj):
    '''Gets the body attribute from the object specified.'''

    if not isinstance(obj, Body):
      if hasattr(obj, "body"):
        return obj.body
      else: 
        raise ValueError("This object does not have a body attached to it.")
    return obj
  
  def insert(self, obj):
    '''Inserts the object into the QuadTree.'''
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
    '''Clears this node from elements and subnodes.'''

    for x in self.subNodes:
      if x != None:
        x.clear()
      x = None
    self.objects = []
        
  def isEmpty(self):
    '''Returns True if it has no elements.'''
    return self.size() == 0
  
  def removeText(self):
    '''Removes the text (element counter) from the screen.'''

    if self.text:
      self.text.undraw()
      self.surface.remove(self.text)
      self.text = None

  def getIndices(self, body):
    '''Gets the nodes that the body is contained by.'''

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

    return res
      
  def split(self):
    '''Splits the node into four subnodes.'''

    if self.depth + 1 >= MAX_DEPTH:
      raise ValueError("Max depth of QuadTree reached")

    if self.hasAppearance:
      self.removeText()

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
    '''Attempts to add the existing nodes to subnodes of the four new quadtrees.'''

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
      i-= 1
  
  def toString(self):
    '''String representation of the QuadTree.'''

    return "QuadTree[x="+str(self.x)+", y="+str(self.y)+", w="+str(self.w)+", h="+str(self.h)+"]"

  def size(self):
    '''The number of elements in the QuadTree.'''

    return self.objects.__len__()

  def retrieve(self, obj):
    '''Retrieves the possible collisions which is the other objects that share the node
    with the specified object.'''

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