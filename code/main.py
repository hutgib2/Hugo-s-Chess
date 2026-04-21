from settings import *
from support import *
from button import InteractiveButton
import json
from chessReboot import ChessReboot


class Menu():
    def __init__(self):
        self.menu_surf = pygame.image.load(join('assets', 'images', 'menu', 'menu.png'))
        self.menu_rect = self.menu_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.running = True
        self.play_surf = pygame.image.load(join('assets', 'images', 'menu', 'play_button.png'))
        self.menu_sprites = pygame.sprite.Group()
        self.play_button = InteractiveButton(self.play_surf, (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/5), (300, 144), self.menu_sprites, self.create_new_game, 'New Game')
        self.load_button = InteractiveButton(self.play_surf, (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4), (300, 144), self.menu_sprites, self.load_game, 'Load Game')
        # create a load game button that loads the last saved game and runs it

    def create_new_game(self):
        with open('assets/saved_games/new_game.json', 'r') as file:
            data = json.load(file)
            self.game = ChessReboot(data)
        self.game.run()


    def load_game(self):
        with open('assets/saved_games/save_game.json', 'r') as file:
            data = json.load(file)
            self.game = ChessReboot(data)
        self.game.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button.rect.collidepoint(event.pos):
                    self.play_button.is_clicked()
                if self.load_button.rect.collidepoint(event.pos):
                    self.load_button.is_clicked()

    def run(self):
        while self.running:
            self.handle_events()
            screen.fill((127, 127, 127))
            screen.blit(self.menu_surf, self.menu_rect)
            self.menu_sprites.update()
            pygame.display.update()

# game = ChessReboot()
# game.run()
menu = Menu()
menu.run()
pygame.quit()