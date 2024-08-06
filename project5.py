import project4_rules as game 
import pygame
import random

_FRAME_RATE = 60
_INITIAL_WIDTH = 277
_INITIAL_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(175, 175, 175)
_ROWS = 13
_COLS  = 6

class ColumnsGame:
    def __init__(self):
        self._running = True
        self._board = game.Board(_ROWS, _COLS, 'EMPTY')
        self._faller = game.Faller(0, 'X', 'X', 'X')


    def run(self) -> None:
        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            tick = 0
            while self._running:
                if self._board.no_fallers():
                    self._faller = self._board.create_random_faller()
                    self._board.set_element(0, self._faller.col() - 1, self._faller.bot())
                clock.tick(_FRAME_RATE)
                self._handle_events()
                self._draw_frame()
                if tick == _FRAME_RATE:
                    self._board.tick(self._faller)
                    tick = 0
                tick += 1
                if self._board.get_game_over() == True:
                    self._running = False

        finally:
            pygame.quit()


    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)


    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)


    def _handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._board.move_faller_left()
                elif event.key == pygame.K_RIGHT:
                    self._board.move_faller_right()
                elif event.key == pygame.K_SPACE:
                    self._faller.rotate()
                    self._board.rotate(self._faller)

    def _draw_frame(self) -> None:
        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_board()
        self._draw_grid()
        pygame.display.flip()

    def _draw_board(self) -> None:
        current_width, current_height = pygame.display.get_surface().get_size()
        for i in range(len(self._board.get_board())):
            for j in range(len(self._board.get_board()[0])):
                if not self._board.is_faller(self._board.get_board()[i][j]) and self._board.get_board()[i][j] != '   ': # if frozen jewel
                    color = self.get_jewel_color(self._board.get_board()[i][j][1])
                    #draw rectangle
                    top_left_pixel_x = (current_width/_COLS * (j + 1) - (current_width/(_COLS * 2))) - (current_width/_COLS)/2
                    top_left_pixel_y = current_height/_ROWS * (i + 1) - (current_height/(_ROWS * 2)) - (current_height/_ROWS)/2                                                  
                    rect = pygame.Rect(
                    top_left_pixel_x, top_left_pixel_y,
                    current_width/_COLS, current_height/_ROWS)
                    pygame.draw.rect(self._surface, color, rect)
                    
                if self._board.is_faller(self._board.get_board()[i][j]): #if faller
                    #draw circle
                    color = self.get_jewel_color(self._board.get_board()[i][j][1])
                    top_left_pixel_x = (current_width/_COLS * (j + 1) - (current_width/(_COLS * 2))) - (current_width/_COLS)/2
                    top_left_pixel_y = current_height/_ROWS * (i + 1) - (current_height/(_ROWS * 2)) - (current_height/_ROWS)/2                                                  
                    rect = pygame.Rect(
                    top_left_pixel_x, top_left_pixel_y,
                    current_width/_COLS, current_height/_ROWS)
                    pygame.draw.ellipse(self._surface, color, rect)

    def get_jewel_color(self, jewel: str) -> None:
        colors = {'R': (255, 0, 0), 'Y': (255, 255, 0), 'O': (255, 150, 0), 'G': (0, 255, 0), 'B': (0, 0, 255), 'P': (221,75,221), 'I': (255,192,203)}
        return colors[jewel]

    def _draw_grid(self) -> None:
        current_width, current_height = pygame.display.get_surface().get_size()
        
        #draw vertical lines
        for i in range(int(current_width/_COLS), current_width - int(current_width/_COLS), int(current_width/_COLS)):
            pygame.draw.line(
                self._surface, pygame.Color(255, 255, 255),
                (i, 0), (i, current_height))
            
        #draw horizontal lines
        for i in range(int(current_height/_ROWS), current_height - int(current_height/_ROWS), int(current_height/_ROWS)):
            pygame.draw.line(
                self._surface, pygame.Color(255, 255, 255),
                (0, i), (current_width, i))


    def _stop_running(self) -> None:
        self._running = False





if __name__ == '__main__':
    ColumnsGame().run()
