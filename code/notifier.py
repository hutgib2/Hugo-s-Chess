from settings import *
from textSprite import TextSprite
from timer import Timer

class Notifier():
    def __init__(self):
        self.duration = 1250
        self.pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.color = 'blue'
        self.size  = 128
        self.start_time = 0
        self.notification = None

    def notify(self, text):
        self.notification = TextSprite(text, self.pos, self.color, self.size, ())
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.notification:
            self.notification.update()
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.notification = None
                self.start_time = 0


notifier = Notifier()