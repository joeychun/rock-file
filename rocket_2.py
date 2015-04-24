from tkinter import *
import time
import random
import copy
from key_controller import key_controller

MIN_X = 0
MAX_X = 400
MIN_Y = 0
MAX_Y = 400 
ROCKET_WIDTH = 10
ROCKET_HEIGHT = 40
MINE_ROCKET_X = 200
MINE_ROCKET_Y = 350
CPU_ROCKET_X = 200
CPU_ROCKET_Y = 50
X_GAP = 10
X_VEL = 5 * 25
Y_VEL = 5 * 25

class game:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("fighting at space")
        self.tk.wm_attributes("-topmost",1)
        self.canvas=Canvas(self.tk,width=500,height=500)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height=500
        self.canvas_width=500
        self.bg = PhotoImage(file="SPACE.gif")
        self.canvas.create_image(0,0,image=self.bg,anchor='nw')
        self.tk.update()
        print('game start')
        self.rockets = []
        self.guns = []
        self.t0 = time.time()

    def add_rocket(self, rocket):
        self.rockets.append(rocket)

    def add_gun(self, gun):
        self.guns.append(gun)

    def delete_gun(self, gun):
        self.guns.remove(gun)

    def main_loop(self):
        while True:
            t1 = time.time()
            span = t1 - self.t0
            self.t0 = t1
            for r in self.rockets:
                r.move(span)
            for g in self.guns:
                g.move(span)
            self.canvas.update()
        
class coords:
    def __init__(self,x1=float(0),x2=float(0),y1=float(0),y2=float(0)):
        self.x1= min(x1, x2)
        self.x2= max(x1, x2)
        self.y1= min(y1, y2)
        self.y2= max(y1, y2)

    def add(self, other):
        new_coords = coords(self.x1+other.x1, self.x2+other.x2, self.y1+other.y1, self.y2+other.y2)
        return new_coords
    
class rocket:
    def __init__(self, coords):
        self.bounding_boxes = []
        self.coords = coords
        
    def register_bounding_box(self, x1, x2, y1, y2):
        self.bounding_boxes.append(coords(x1, x2, y1, y2))

    def collision_check(self, obj):
        #obj must have bounding_boxes and coords
        for box_a in self.bounding_boxes:
            for box_b in obj.bounding_boxes:
                a = self.coords.add(box_a)
                b = self.coords.add(box_b)
                overlap_x = (a.x1 > b.x1 and a.x1 < b.x2) or (a.x1 < b.x1 and a.x2 > b.x1)
                overlap_y = (a.y1 > b.y1 and a.y1 < b.y2) or (a.y1 < b.y1 and a.y2 > b.y1)

class gun:
    def __init__(self, coords):
        self.bounding_boxes = []
        self.coords = coords
    def register_bounding_box(self, x1, x2, y1, y2):
        self.bounding_boxes.append(coords(x1, x2, y1, y2))

class mine_rocket(rocket):
    def __init__(self,game,coords):
        rocket.__init__(self, coords)
        self.register_bounding_box(40, 60, 40, 72)
        self.register_bounding_box(30, 70, 65, 72)
        self.game = game
        self.canvas=game.canvas
        self.bg = PhotoImage(file="rocketshipMINE.gif")
        self.image = self.canvas.create_image(coords.x1,coords.y1,image=self.bg,anchor='nw')
        self.key_controller = key_controller()
        self.canvas.bind_all('<Key>', self.key_controller.key)
        self.canvas.bind_all('<KeyRelease>', self.key_controller.key_release)
        self.game.add_rocket(self)
        self.t0 = time.clock()
        
    def shoot(self):
        t1 = time.time()
        if t1 - self.t0 > 3:
            mine_rocket_gun(self.game, self.coords)
            self.t0 = t1

    def move(self, span):
        self.key_controller.loop()
        if self.key_controller.direction is None:
            pass
        elif self.key_controller.direction is 'Left':
            distance = span * X_VEL
            if self.coords.x1 - distance >= MIN_X:
                self.canvas.move(self.image, -distance, 0)
                self.coords.x1 -= distance
        else:
            distance = span * X_VEL
            if self.coords.x1 + distance <= MAX_X:
                self.canvas.move(self.image, distance, 0)
                self.coords.x1 += distance
           
class mine_rocket_gun(gun):
    def __init__(self,game,coords):
        gun.__init__(self, coords)
        self.game = game
        self.canvas=game.canvas
        self.bg = PhotoImage(file="bulletMINE.gif")
        self.image = self.canvas.create_image(self.coords.x1,self.coords.y1,image=self.bg,anchor='nw', tags='gun')
        self.game.add_gun(self)
        
    def move(self, span):
        if self.coords.y1 > MIN_Y:
            self.canvas.move(self.image, 0, -span * Y_VEL)
            self.coords.y1 -= span * Y_VEL
        if self.coords.y1 <= MIN_Y + 10:
            self.canvas.delete('gun')
            self.game.delete_gun(self)
            
class cpu_rocket(rocket):
    def __init__(self,game):
        self.game = game
        self.canvas=game.canvas
        self.bg = PhotoImage(file="rocketshipCPU.gif")
        self.canvas.create_image(200,50,image=self.bg,anchor='nw')
        self.game.add_rocket(self)
    def move(self, span):
        pass

class cpu_rocket_gun(gun):
    pass

if __name__ == "__main__":
    g=game()
    mine=mine_rocket(g,coords(MINE_ROCKET_X, MINE_ROCKET_X + ROCKET_WIDTH, MINE_ROCKET_Y, MINE_ROCKET_Y + ROCKET_HEIGHT))
    cpu=cpu_rocket(g)
    g.main_loop()
 

