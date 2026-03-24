from settings import *
from support import *
from textSprite import TextSprite
from chessBoard import ChessBoard
from button import InteractiveButton
import time

class Chess2026():
    def __init__(self):
        self.running = True
        self.board = ChessBoard(BOARD_SURFS['chess_board'])
        self.rulebook_surf = pygame.image.load(join('assets', 'images', 'rules', 'rulebook.png'))
        self.rulebook = InteractiveButton(self.rulebook_surf, (200, 200), (256, 256), (), self.show_rules)
        self.rules_screen = pygame.image.load(join('assets', 'images', 'rules', 'rules_screen.png'))
        self.rules_rect = self.rules_screen.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.rules_shown = False
        self.checkmate_text = TextSprite('Checkmate!', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 'green', 128, ())

        # audio
        self.kill_sound = pygame.mixer.Sound(join('assets', 'audio', 'kill.wav'))
        self.move_sound = pygame.mixer.Sound(join('assets', 'audio', 'move.wav'))
        
    def show_rules(self):
        self.rules_shown = not self.rules_shown

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.board.reset_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.board.save_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.board.load_game('assets/board_state/save_game.json')
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and self.board.selected_square:
                self.board.deselect_piece()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rulebook.rect.collidepoint(event.pos):
                    self.rulebook.is_clicked()
                    continue
                if self.rules_shown:
                    continue
                if not self.board.rect.collidepoint(event.pos) and self.board.selected_square:
                    self.board.deselect_piece()
                    continue

                for row in range(8):
                    for col in range(8):
                        click_square = self.board.squares[row][col]
                        if not click_square.rect.collidepoint(event.pos):
                            continue
                        if click_square.is_swappable:
                            self.board.swap_piece(self.board.selected_square, click_square)
                            self.board.switch_turn()                    
                        elif click_square.piece and click_square.piece.color == self.board.turn and not click_square.piece.is_stunned:
                            self.board.select_piece(click_square)
                        elif click_square.is_possible_move:
                            self.move_sound.play() 
                            self.board.move_piece(self.board.selected_square, click_square) 
                            self.board.switch_turn()                    
                        elif click_square.is_attack_move:
                            self.kill_sound.play()
                            self.board.attack_piece(self.board.selected_square, click_square)
                            self.board.switch_turn()
                        elif click_square.piece == None and self.board.selected_square:
                            self.board.deselect_piece()
                        
                        self.board.update()

    def run(self):
        while self.running:
            self.handle_events()
            
            screen.fill((100, 100, 100))
            self.board.render()
            if self.board.checkmate:
                self.checkmate_text.update()
                pygame.display.update()
                time.sleep(2)
                self.running = False
            self.rulebook.update()
            if self.rules_shown == True:
                pygame.display.get_surface().blit(self.rules_screen, self.rules_rect)
            pygame.display.update()
        
game = Chess2026()
game.run()
pygame.quit()