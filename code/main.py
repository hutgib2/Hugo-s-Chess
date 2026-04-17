from settings import *
from support import *
from textSprite import TextSprite
from chessBoard import ChessBoard
from button import InteractiveButton
from pieces.piece import *
from animator import Animator
from notifier import notifier
from timer import Timer
import json
import time

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

class Chess2026():
    def __init__(self):
        self.players = {
            "white": Player('white'),
            "black": Player('black')
        }
        self.create_new_game()
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_blocked = False
        self.switch_turn_timer = Timer(1000, self.switch_turn)

        self.rulebook_surf = pygame.image.load(join('assets', 'images', 'rules', 'rulebook.png'))
        self.rulebook = InteractiveButton(self.rulebook_surf, (200, 200), (256, 256), (), self.show_rules)
        self.rules_screen = pygame.image.load(join('assets', 'images', 'rules', 'rules_screen.png'))
        self.rules_rect = self.rules_screen.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.rules_shown = False
        
        self.animator = Animator()

        # audio
        self.kill_sound = pygame.mixer.Sound(join('assets', 'audio', 'kill.wav'))
        self.move_sound = pygame.mixer.Sound(join('assets', 'audio', 'move.wav'))
        self.swap_sound = pygame.mixer.Sound(join('assets', 'audio', 'swap.wav'))

    def create_new_game(self):
        with open('assets/saved_games/new_game.json', 'r') as file:
            data = json.load(file)
            self.board = ChessBoard(BOARD_SURFS['chess_board'], data, self.players)
    
    def load_game(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.board.apply_snapshot(data)
        notifier.notify('Game Loaded!')

    def reset_game(self):
        self.create_new_game()
        notifier.notify('New Game!')
        self.players['white'].set_score(0)
        self.players['black'].set_score(0)

    def save_game(self):
        with open('assets/saved_games/save_game.json', 'w') as file:
            data = self.board.take_snapshot()
            json.dump(data, file)
        notifier.notify('Game Saved!')
        
    def show_rules(self):
        self.rules_shown = not self.rules_shown

    def switch_turn(self):
        self.game_blocked = False
        self.board.deselect_piece()
        self.board.turn = 'black' if self.board.turn == 'white' else 'white'
        self.board.round_num += 1
        if self.board.in_check(self.board.turn):
            notifier.notify('Check!')
        self.board.resolve_timers()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.save_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.load_game('assets/saved_games/save_game.json')
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and self.board.selected_square:
                self.board.deselect_piece()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rulebook.rect.collidepoint(event.pos):
                    self.rulebook.is_clicked()
                    continue
                if self.rules_shown or self.game_blocked:
                    continue
                if not self.board.rect.collidepoint(event.pos) and self.board.selected_square:
                    print(f'event pos: {event.pos} {type(event.pos)}')
                    self.board.deselect_piece()
                    self.board.update()
                    continue
                    
                action = None
                # handling game play clicks
                for row in range(8):
                    for col in range(8):
                        click_square = self.board.squares[row][col]
                        if not click_square.rect.collidepoint(event.pos):
                            continue
                        if click_square.is_swappable:
                            self.swap_sound.play()
                            self.animator.swap([self.board.selected_square.rect, click_square.rect])
                            self.board.swap_piece(self.board.selected_square, click_square)
                            self.board.deselect_piece()
                            action = 'swap'
                        elif click_square.piece and click_square.piece.color == self.board.turn and not click_square.piece.is_stunned:
                            self.board.select_piece(click_square)
                            action = 'select'
                        elif click_square.is_possible_move:
                            self.move_sound.play() 
                            self.board.move_piece(self.board.selected_square, click_square)
                            action = 'move'
                        elif click_square.is_attack_move:
                            self.kill_sound.play()
                            self.animator.attack(self.board.selected_square, click_square, self.players[click_square.piece.color].pieces)
                            score = self.board.attack_piece(self.board.selected_square, click_square)
                            self.players[self.board.turn].set_score(self.players[self.board.turn].score + score)
                            self.board.deselect_piece()
                            action = 'attack'
                        elif click_square.piece == None and self.board.selected_square:
                            self.board.deselect_piece()
                            action = 'deselect'

                if action:
                    self.board.update()
                if action == 'swap' or action == 'move':
                    self.switch_turn()
                elif action == 'attack':
                    self.game_blocked = True
                    self.switch_turn_timer.activate()

                
                    
    def draw_game(self, dt):
        screen.fill((127, 127, 127))
        self.board.render()
        notifier.update()
        self.animator.update(dt, self.board.round_num)
        self.rulebook.update()
        self.players['white'].update()
        self.players['black'].update()

        if self.rules_shown == True:
            pygame.display.get_surface().blit(self.rules_screen, self.rules_rect)
        pygame.display.update()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.switch_turn_timer.update()
            self.handle_events()
            self.draw_game(dt)
            if self.board.checkmate:
                time.sleep(2)
                self.running = False
            
        
game = Chess2026()
game.run()
pygame.quit()