import time

TIME_GAP = 0.01

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
        if event.keysym == 'Right':
            self.right_press_time = time.time()
        if event.keysym == 'space':
            pass

    def key_release(self, event):
        if event.keysym == 'Left':
            self.left_release_time = time.time()
        if event.keysym == 'Right':
            self.right_release_time = time.time()
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
