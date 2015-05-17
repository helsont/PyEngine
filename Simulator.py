from Graphics import *
from Myro import *
import random
from CollisionDetection import CollisionDetection 
from Body import Body
from Vec2 import Vec2
from GameLoop import GameLoop
from Surface import Surface

class Globals(object):
  Added = 0
  def __init__(self):
    pass

Globals = Globals()

Surface = Surface("Game", 1200, 700)
GameLoop = GameLoop(Surface)

character = Body(50, 50, 20, 20)

Surface.giveAppearance(character)
GameLoop.add(character)

floor = Body(0, Surface.getHeight() - 100, Surface.getWidth(), 10)
floor.setType('static')
Surface.giveAppearance(floor)
GameLoop.add(floor)

enemy = Body(100, 20, 40, 40)
Surface.giveAppearance(enemy)
GameLoop.add(enemy)

def keyboardListener(win):
  speed = 2
  if win.getKeyPressed('Left') == True:
    character.force += Vec2(-speed, 0)

  if win.getKeyPressed('Right') == True:
    character.force += Vec2(speed, 0)

  if win.getKeyPressed('Up') == True:
    character.force.y = -10

  if win.getKeyPressed('Down') == True:
    character.force += Vec2(0, speed)

  if win.getKeyPressed('space') == True:
    update()

def keyTyped(win):
  if win.getKeyPressed('p'):
    GameLoop.paused = not GameLoop.paused
  if win.getKeyPressed('r'):
    character.appearance.x = Surface.getWidth()/2
    character.appearance.y = Surface.getHeight()/2
    character.x = character.appearance.x
    character.y = character.appearance.y

def update():
  if Globals.Added <= 1000:
    Globals.Added += 1
    x = random.randrange(0, Surface.getWidth() - 10)
    y = random.randrange(0, Surface.getHeight() - 10)

    dx = random.randrange(-5, 5)
    dy = random.randrange(-5, 5)

    b = Body(x, y, 10, 10)
    b.force = Vec2(dx, dy)
    Surface.giveAppearance(b)

    GameLoop.add(b)

def mouseClickedListener(win):
  point = win.getMouseNow()
  newBody = Body(point[0], point[1], 10, 10)
  Surface.giveAppearance(newBody)
  newBody.name = "Bobby"
  GameLoop.add(newBody)
  GameLoop.pauseNext = True

GameLoop.addKeyPressListener(keyboardListener)
GameLoop.addKeyTypedListener(keyTyped)
GameLoop.addMouseClickedListener(mouseClickedListener)

GameLoop.run()