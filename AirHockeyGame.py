import pymunkoptions
pymunkoptions.options["debug"] = False
import pyglet
# Importuję żeby stworzyć dostosowane okno gry
from pyglet.window import  FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random

collision_types = {
    "puck":1,
    "rail":2,
    "player":3
}

class Puck(pymunk.Body):
    def __init__(self, space):
        super().__init__(1, pymunk.inf)
        self.position = 425, 475
        shape = pymunk.Circle(self, 10)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["puck"]
        self.spc = space
        self.on_puck = True
        self.velocity_func = self.constant_velocity

        # nie używam
        #self.joint = pymunk.GrooveJoint(space.static_body, self, (100,118), (1180,118), (0,0))

        space.add(self, shape)

    def strike_on_puck(self):
        self.on_puck = False
        self.spc.remove(self.joint)
        direction = Vec2d(random.choice([((50,500), (-50,500))]))
        self.apply_impulse_at_local_point(direction)

    def constant_velocity(self, body, gravity, damping, dt):
        body.velocity = body.velocity.normalized()*600


class Player(pymunk.Body):
    def __init__(self, space):
        super().__init__(10, pymunk.inf)
        self.position = 425, 100
        shape = pymunk.Circle(self, 20)
        shape.elasticity = 0.98
        shape.collision_type = collision_types["player"]

        #joint którego nie potrzebuję
        #joint = pymunk.GrooveJoint(space.static_body, self, (100,100), (1180,100), (0,0))

        space.add(self, shape)


class Rail:
    def __init__(self, space):
        left = pymunk.Segment(space.static_body, (10,10), (10,970), 10)
        top = pymunk.Segment(space.static_body, (10, 970), (840, 970), 10)
        right = pymunk.Segment(space.static_body, (840, 10), (840, 970), 10)
        bottom = pymunk.Segment(space.static_body, (10, 10), (840, 10), 10)

        left.elasticity = 0.98
        top.elasticity = 0.98
        right.elasticity = 0.88
        bottom.elasticity = 0.98

        # nie używam
        # left.sensor = True
        # left.collision_type = collision_types["puck"]

        space.add(left,top,right,bottom)


# Nie rozumiem po co jest funkcja super
class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(500, 50)
        self.fps = FPSDisplay(self)

        self.space = pymunk.Space()
        self.options = DrawOptions()

        self.player = Player(self.space)
        self.puck = Puck(self.space)
        self.rail = Rail(self.space)

    #Metoda służąca do rysowania, wpisujemy co ma rysować
    def on_draw(self):
        #czyści okno na fpsach
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player.velocity = 600, 0
        if symbol == key.LEFT:
            self.player.velocity = -600, 0
        if symbol == key.UP:
            self.player.velocity = 0, 600
        if symbol == key.DOWN:
            self.player.velocity = 0, -600

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT, key.UP, key.DOWN):
            self.player.velocity = 0, 0

    def update(self, dt):
        self.space.step(dt)

# Tworzę okienko o określonych parametrach
if __name__ == "__main__":
    window = GameWindow(850, 980, "Breakout game", resizable=False)
    #60 razy na sekundę odświeża ekran
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()