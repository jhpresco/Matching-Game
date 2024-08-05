import project4_rules as game

def run() -> None:
    rows = int(input())
    cols = int(input())
    filled = input()
    board = game.Board(rows, cols, filled)

    faller = None
    board.start_game()
    
    #main game loop
    while not board.get_game_over():
        inp = input()
        if inp == 'Q':
            board.set_game_over(True)
        elif 'F ' in inp:
            params = inp.split(' ')
            faller = game.Faller(int(params[1]), params[2], params[3], params[4])
            if board.get_board()[0][faller.col() - 1] != '   ':
                board.set_game_over(True)
            else:
                if board.get_board()[1][faller.col() - 1] == '   ':
                    board.set_element(0, faller.col() - 1, faller.bot())
                else:
                    board.set_element(0, faller.col() - 1, '|' + faller.bot()[1] + '|')
        elif '>' in inp:
            board.move_faller_right()
        elif '<' in inp:
            board.move_faller_left()
        elif 'R' in inp:
            faller.rotate()
            board.rotate(faller)
        # elif 'P' in inp:
        #     print(board.faller_count())
        else:
            board.tick(faller)
            
        if board.get_game_over() == False:
            board.print_board()
            #print(board.faller_count())
        # else:
        #     print('GAME OVER')

if __name__ == '__main__':
    run()