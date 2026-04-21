from settings import *
from textSprite import TextSprite

class Player():
    def __init__(self, color):
        self.emperor = None
        self.pieces = pygame.sprite.Group()
        self.color = color
        self.score = 0
        
        # text
        self.name_text_pos = (WINDOW_WIDTH / 8, WINDOW_HEIGHT / 2) if self.color == 'white' else (7*WINDOW_WIDTH / 8, WINDOW_HEIGHT / 2)
        self.name_text = TextSprite(self.color.title(), self.name_text_pos, self.color, 128, ())
        self.score_text_pos = list(self.name_text.rect.midright)
        self.score_text_pos[0] += 64
        self.score_text = TextSprite(str(self.score), self.score_text_pos, color, 128, ())

    def set_score(self, score):
        self.score = score
        self.score_text = TextSprite(str(self.score), self.score_text_pos, self.color, 128, ())

    def update(self):
        self.name_text.update()
        self.score_text.update()
