from tkinter import *
import time
import random
import copy

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
TIME_GAP = 0.01

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
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2

class rocket:
    pass
class gun:
    pass

class key_controller:
    def __init__(self):
        self.left_press_time = None
        self.right_press_time = None
        self.left_release_time = None
        self.right_release_time = None
        self.left_pressed = False
        self.right_pressed = False
        self.direction = None

    def key(self, event):
        if event.keysym == 'Left':
            self.left_press_time = time.time()
            #print ('left press')
        if event.keysym == 'Right':
            self.right_press_time = time.time()
            #print ('right press')
        if event.keysym == 'space':
            pass

    def key_release(self, event):
        if event.keysym == 'Left':
            self.left_release_time = time.time()
            #print ('left release')
        if event.keysym == 'Right':
            self.right_release_time = time.time()
            #print ('right release')
        if event.keysym == 'space':
            pass

    def check_pressed(self, press_time, release_time):
        if press_time is None:
            return False
        elif release_time is None:
            return True
        else:
            if press_time > release_time:
                return True
            else:
                current_time = time.time()
                gap = current_time - release_time
                return (gap < TIME_GAP)

    def loop(self):
        self.left_pressed = self.check_pressed(self.left_press_time, self.left_release_time)
        self.right_pressed = self.check_pressed(self.right_press_time, self.right_release_time)
        if self.left_pressed is False and self.right_pressed is False:
            self.direction = None
        elif self.left_pressed is True and self.right_pressed is False:
            self.direction = 'Left'
        elif self.left_pressed is False and self.right_pressed is True:
            self.direction = 'Right'
        elif self.left_pressed is True and self.right_pressed is True:
            if self.left_press_time > self.right_press_time:
                self.direction = 'Left'
            else:
                self.direction = 'Right'
        

class mine_rocket(rocket):
    def __init__(self,game,coords):
        self.game = game
        self.coords = coords
        self.next_coords = copy.copy(coords)
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
           
class mine_rocket_gun:
    def __init__(self,game,coords):
        self.game = game
        self.coords = copy.copy(coords)
        self.coords.y1 -= 20
        self.next_coords = copy.copy(self.coords)
        self.next_coords.y1 = 0
        self.canvas=game.canvas
        self.bg = PhotoImage(file="bulletMINE.gif")
        self.image = self.canvas.create_image(self.coords.x1,self.coords.y1,image=self.bg,anchor='nw', tags='gun')
        self.game.add_gun(self)
        
    def move(self, span):
        if self.next_coords.y1 + span * Y_VEL < self.coords.y1 and self.coords.y1 > MIN_Y:
            self.canvas.move(self.image, 0, -span * Y_VEL)
            self.coords.y1 -= span * Y_VEL
        elif self.coords.y1 + span * Y_VEL < self.next_coords.y1 and self.coords.y1 <= MAX_Y:
            self.canvas.move(self.image, 0, span * Y_VEL)
            self.coords.y1 += span * Y_VEL
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

if __name__ == "__main__":
    g=game()
    mine=mine_rocket(g,coords(MINE_ROCKET_X, MINE_ROCKET_X + ROCKET_WIDTH, MINE_ROCKET_Y, MINE_ROCKET_Y + ROCKET_HEIGHT))
    cpu=cpu_rocket(g)
    g.main_loop()
 

