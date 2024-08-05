import random

class Board:

    def __init__(self, rows: int, cols: int, filled: str): 
        self._rows= rows
        self._cols = cols
        self._game_over = False
        if 'CONTENT' in filled:
            self._board = self.create_filled_field()
        elif 'CUSTOM' in filled:
            self._board = self._create_custom_field()
        else:
            self._board = self.create_empty_field()

    def create_random_faller(self):
        col_list = [1, 2, 3, 4, 5, 6]
        jewel_list = ['R', 'O', 'Y', 'G', 'B', 'P']
        col = random.choice(col_list)
        top_jewel = random.choice(jewel_list)
        mid_jewel = random.choice(jewel_list)
        bot_jewel = random.choice(jewel_list)
        faller = Faller(col, top_jewel, mid_jewel, bot_jewel)
        return faller

    def no_fallers(self) -> bool:
        'returns True if there are no active fallers and false otherwise'
        no_faller = True
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self.is_faller(self._board[i][j]):
                    no_faller = False
        return no_faller


    def tick(self, faller) -> None:
        'advances the game'
        while self.are_gaps():
            self.fall_jewels()
        if faller != None:
            self.drop_faller(faller)
            self.freeze_landed_fallers()
            self.land_fallers(faller)
        self.clear_matches()
        while self.are_gaps():
            self.fall_jewels()
        self.check_horizontal_matches()
        self.check_vertical_matches()
        while self.are_gaps():
            self.fall_jewels()

    def start_game(self) -> None:
        'begins the game'
        while self.are_gaps():
            self.fall_jewels()
        self.check_horizontal_matches()
        self.check_vertical_matches()
        while self.are_gaps():
            self.fall_jewels()
        self.print_board()
        

    def check_horizontal_matches(self) -> None:
        'checks for horizontal matches'
        for i in range(len(self._board)):
            for j in range(len(self._board[0]) - 2):
                try:
                    if self._board[i][j] == self._board[i][j+1] == self._board[i][j+2] and self._board[i][j] != '   ':
                        self._board[i][j] = '*' + self._board[i][j][1] + '*'
                        self._board[i][j + 1] = '*' + self._board[i][j + 1][1] + '*'
                        self._board[i][j + 2] = '*' + self._board[i][j + 2][1] + '*'
                except IndexError:
                    pass
            
    def check_vertical_matches(self) -> None:
        'checks for vertical matches'
        for i in range(len(self._board) - 2):
            for j in range(len(self._board[0])):
                try:
                    if self._board[i][j] == self._board[i + 1][j] == self._board[i + 2][j] and self._board[i][j] != '   ':
                        self._board[i][j] = '*' + self._board[i][j][1] + '*'
                        self._board[i + 1][j] = '*' + self._board[i + 1][j][1] + '*'
                        self._board[i + 2][j] = '*' + self._board[i + 2][j][1] + '*'
                except IndexError:
                    pass
            
    def clear_matches(self) -> None:
        'clears all entries with aterisks'
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if '*' in self._board[i][j]:
                    self._board[i][j] = '   '

    def is_faller(self, elem: str) -> None:
        'checks if an element in the board is a faller or not'
        if '[' in elem:
            return True
        elif '|' in elem:
            return True
        else:
            return False

    def rotate(self, faller: 'Faller') -> None:
        'updates the board to express a faller rotation'
        faller_count = self.faller_count()
        first_pass = True
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if faller_count == 1 and self.is_faller(self._board[i][j]):
                    self._board[i][j] = faller.bot()
                if faller_count == 2 and self.is_faller(self._board[i][j]) and first_pass:
                    self._board[i][j] = faller.mid()
                    self._board[i + 1][j] = faller.bot()
                    first_pass = False
                if faller_count == 3 and self.is_faller(self._board[i][j]) and first_pass:
                    self._board[i][j] = faller.top()
                    self._board[i + 1][j] = faller.mid()
                    self._board[i + 2][j] = faller.bot()
                    first_pass = False

    def faller_can_move(self, direction) -> bool:
        'confirms the faller is not obstructed'
        can_move = True
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                try:
                    if self.is_faller(self._board[i][j]) and self._board[i][j + direction] != '   ':
                        can_move = False
                except IndexError:
                    pass
        return can_move
        
    def move_faller_left(self):
        'moves all visible fallers to the left'
        if self.faller_can_move(-1):
            for i in range(len(self._board), -1, -1):
                for j in range(len(self._board[0])):
                    try:
                        if self.is_faller(self._board[i][j]) and j + -1 >= 0:
                            #print('moved a faller')
                            self._board[i][j + -1] = self._board[i][j]
                            self._board[i][j] = '   '
                    except IndexError:
                        pass
        
    def move_faller_right(self):
        'moves all visible fallers to the right'
        if self.faller_can_move(1):
            for i in range(len(self._board)):
                for j in range(len(self._board[0]), -1, -1):
                    try:
                        if self.is_faller(self._board[i][j]):
                            self._board[i][j + 1] = self._board[i][j]
                            self._board[i][j] = '   '
                    except IndexError:
                        pass

    def drop_faller(self, faller: 'Faller'):
        'moves all visible fallers down one'
        moved = False
        for i in range(len(self._board), -1, -1):
            for j in range(len(self._board[0])):
                try:
                    if '[' in self._board[i][j] and self._board[i + 1][j] == '   ':
                        moved = True
                        self._board[i + 1][j] = self._board[i][j] #space underneath becomes original space
                        self._board[i][j] = '   ' #oringal space becomes empty
                        if self.faller_count() == 1:
                            self._board[i][j] = faller.mid()
                        if self.faller_count() == 2 and i > 0:
                            self._board[i][j] = faller.mid()
                            self._board[i-1][j] = faller.top()
                except IndexError:
                    pass
        #check if landed
        return moved

        
    def land_fallers(self, faller) -> bool:
        'changes a fallers brackets to vertical lines if it has landed'
        board_copy = Board(self._rows, self._cols, 'EMPTY')
        board_copy._set_board(self._board)
        moved = board_copy.drop_faller(faller)
        if not moved: #dropping faller did nothing
            for i in range(len(self._board)):
                for j in range(len(self._board[0])):
                    if '[' in self._board[i][j]:
                        self._board[i][j] = self._board[i][j].replace('[', '|')
                        self._board[i][j] = self._board[i][j].replace(']', '|')
                        faller.set_top('|' + faller.top()[1] + '|')
                        faller.set_mid('|' + faller.mid()[1] + '|')
                        faller.set_bot('|' + faller.bot()[1] + '|')

                    
    def freeze_landed_fallers(self) -> None:
        'removes the vertical bars from landed fallers'
        frozen_count = 0
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):  
                if '|' in self._board[i][j]:
                    self._board[i][j] = self._board[i][j].replace('|', ' ')
                    frozen_count += 1
        if frozen_count == 1 or frozen_count == 2:
            self._game_over = True

    def faller_count(self) -> int:
        'returns the amount of visible fallers'
        count = 0
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self.is_faller(self._board[i][j]):
                    count += 1
        return count 

     
    def set_element(self, row: int, col: int, elem: str) -> None:
        self._board[row][col] = elem

    def get_board(self) -> list[list]:
        return self._board.copy()
    
    def _set_board(self, nested_list: list[list]) -> None:
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                    self._board[i][j] = nested_list[i][j]
    
    def get_game_over(self) -> bool:
        return self._game_over
    
    def set_game_over(self, game_over: bool) -> None:
        self._game_over = game_over

    def create_filled_field(self) -> list[list]:
        field = [ ['   ']*self._cols for i in range(self._rows)]
        i = 0
        j = 0
        for k in range(self._rows):
            j = 0
            x = input();
            to_add_list = []
            for letter in x:
                to_add_list.append(' ' + letter + ' ')
            for l in range(self._cols):
                field[i][j] = to_add_list[j]
                j += 1
            i += 1
        return field

    def _create_custom_field(self):
        nested_list = [[' ', 'Y', ' ', 'X'], ['S', ' ', 'V', ' '], ['T', 'X', 'Y', 'S'], ['X', ' ', 'X', 'Y']]
        custom_field = [[None for i in range(len(nested_list))] for j in range(len(nested_list[0]))]
        for i in range(len(nested_list)):
            for j in range(len(nested_list[i])):
                custom_field[i][j] = ' ' + nested_list[i][j] + ' '
        return custom_field

    def fall_jewels(self):
        'moves all frozen jewels down if possible'
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                try:
                    if self._board[i + 1][j] == '   ' and not self.is_faller(self._board[i][j]): #if space underneath is empty
                        self._board[i + 1][j] = self._board[i][j] #space underneath becomes original space
                        self._board[i][j] = '   ' #oringal space becomes empty
                except IndexError:
                    pass
            
    def create_empty_field(self) -> list[list]:
        field = [ ['   ']*self._cols for i in range(self._rows)]
        return field

    def are_gaps(self) -> bool:
        'confirms there are gaps beneath frozen jewels'
        gaps = False
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                try:
                    if self._board[i][j] != '   ' and self._board[i + 1][j] == '   ' and not self.is_faller(self._board[i][j]): #if entry is not empty and entry beneath is a space and entry is not a faller
                        gaps = True
                except IndexError:
                    pass
        return gaps
                    
        
    def print_board(self) -> None:
        for row in self._board:
            print('|', end = '')
            for entry in row:
                print(entry, end = '')
            print('|')
        print(' ' + '-'*3*self._cols + ' ')

class Faller:

    def __init__(self, col: int, top: str, mid: str, bot: str):
        self._col = col
        self._top = '[' + top +']'
        self._mid = '[' + mid + ']'
        self._bot = '[' + bot + ']'
        self._jewels = [self._bot, self._mid, self._top]
    
    def rotate(self) -> None:
        temp = self._bot
        self._bot = self._mid
        self._mid = self._top
        self._top = temp


    
    def top(self):
        return self._top

    def mid(self):
        return self._mid
    
    def bot(self):
        return self._bot

    def set_top(self, top: str):
        self._top = top
    
    def set_mid(self, mid: str):
        self._mid = mid

    def set_bot(self, bot:str):
        self._bot = bot

    def col(self):
        return self._col

    
