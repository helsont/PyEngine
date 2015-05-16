from Vec2 import Vec2
class PhysicsCharacter:

    JUMPING = 2
    NOT_JUMPING = 3
    ON_GROUND = False
    GRAVITY = 300
    FRICTION = Vec2(8,0)

    def __init__(self, win):
        self.win = win
        self.state = character.LIVE
        self.onGround = True
        self.jump = character.NOT_JUMPING
        self.force = None

    # Vec2 Force: the force being applied
    def applyForce(self, force):
        self.force = self.force + force

    def update(self, step):
        self.appearance.x += self.force.x * step
        self.appearance.y += self.force.x * step
        self.force.y += character.GRAVITY * step
        
        if self.velocityX > 0:
            self.force -= FRICTION
            
        if self.velocityX < 0:
            self.force += FRICTION

    def setOnGround(self, platform):
        self.force.y = 0
        self.onGround = True
        self.jump = character.NOT_JUMPING
        self.appearance.y = platform.appearance.y - self.appearance.getHeight()/2 - 5
    
    def setOffLeft(self,platform):
        self.force.x = 0
        self.onGround = False
        self.jump = character.JUMPING
        self.appearance.x = platform.appearance.x - platform.width/2 - self.appearance.getWidth()/2

    def setOffRight(self, platform):
        self.force.x = 0
        self.onGround = False
        self.jump = character.JUMPING
        self.appearance.x = platform.appearance.x + platform.width/2 + self.appearance.getWidth()/2

    def setUnderGround(self,platform):
        self.force.y = 0
        self.onGround = False
        self.jump = character.JUMPING
        self.appearance.y = platform.appearance.y + 1

    def collidedWith(self, other):
        return