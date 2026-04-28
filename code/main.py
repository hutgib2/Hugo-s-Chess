from settings import *
from support import *
from button import InteractiveButton
from textSprite import InteractiveText
from chessReboot import ChessReboot
import json
import uuid
import datetime

# TODO: update save game links during session, remove save game when game completed

class Menu():
    def __init__(self):
        self.menu_surf = pygame.image.load(join('assets', 'images', 'menu', 'menu.png'))
        self.menu_rect = self.menu_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.running = True
        self.play_surf = pygame.image.load(join('assets', 'images', 'menu', 'play_button.png'))

        self.menu_sprites = pygame.sprite.Group()
        InteractiveButton(self.play_surf, (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/5), (300, 144), self.menu_sprites, self.create_new_game, 'New Game')
        InteractiveButton(self.play_surf, (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4), (300, 144), self.menu_sprites, self.show_saved_games, 'Load Game')

        self.showing_games = False
        self.saved_games_surf = pygame.image.load(join('assets', 'images', 'menu', 'saved_games.png'))
        self.saved_games_rect = self.saved_games_surf.get_frect(center=(WINDOW_WIDTH/6, WINDOW_HEIGHT/3))
        self.saved_game_links = pygame.sprite.Group()
        self.create_saved_game_links()

        # create a load game button that loads the last saved game and runs it

    def create_new_game(self):
        with open('assets/new_game.json', 'r') as file:
            data = json.load(file)
            now = datetime.datetime.now()
            game_id = now.strftime("%d-%m-%Y-%H%M")
            game = ChessReboot(game_id, data)
        self.run_game(game)

    def get_saved_game_ids(self):
        game_ids = []
        for folder_path, _, file_names in walk('assets/saved_games/'):
            for file_name in file_names:
                game_ids.append(file_name.split('.')[0])
        return game_ids

    def create_saved_game_links(self): 
        self.saved_game_links.empty()
        game_ids = self.get_saved_game_ids()
        i = 200
        for game_id in game_ids:
            InteractiveText(game_id, self.saved_games_rect.midtop + pygame.Vector2(0, i), 'white', (WINDOW_WIDTH / 64), lambda gid=game_id: self.load_game(gid), self.saved_game_links)
            i += 64
        
    def show_saved_games(self):
        self.create_saved_game_links()
        self.showing_games = not self.showing_games
        # deactivate all saved game link on not show
        for link in self.saved_game_links:
            link.reactivate() if self.showing_games else link.deactivate()

    def load_game(self, game_id):
        with open(f'assets/saved_games/{game_id}.json', 'r') as file:
            data = json.load(file)
            game = ChessReboot(game_id, data)
        self.run_game(game)


    def run_game(self, game):
        # close the menu
        self.showing_games = False
        game.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for menu_sprite in self.menu_sprites:
                    if menu_sprite.rect.collidepoint(event.pos):
                        menu_sprite.is_clicked()
                for link in self.saved_game_links:
                    if link.rect.collidepoint(event.pos):
                        link.is_clicked()

    def run(self):
        while self.running:
            self.handle_events()
            screen.fill((127, 127, 127))
            screen.blit(self.menu_surf, self.menu_rect)
            if self.showing_games:
                screen.blit(self.saved_games_surf, self.saved_games_rect)
                self.saved_game_links.update()
            self.menu_sprites.update()
            pygame.display.update()

# game = ChessReboot()
# game.run()
menu = Menu()
menu.run()
pygame.quit()