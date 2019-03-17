"""
Jeff's Tic Tac Toe Game - a Udemy Python Bootcamp exercise Coded in Python February 17, 2019
"""

import msvcrt
from subprocess import call

call('color a', shell=True)  # this sets the color to light green
tic_tac = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3']]  # Perhaps I should make this a tuple.


def populate_marks(letter, row, col, lst):
    patterns = {0: '  ooo     ooo  ', 1: '   ooo   ooo   ', 2: '    ooo ooo    ', 3: '     ooooo     ',
                4: '    ooooooo    ',
                5: '  oooo   oooo  ', 6: '  ooo     ooo  '}
    mark_pattern = {'X': [0, 1, 2, 3, 2, 1, 0], 'O': [4, 5, 6, 6, 6, 5, 4], }
    for line in range(0, 7):
        lst[row][line][col] = patterns[mark_pattern[letter][line]]
    return lst


def prnt_game(pattern_lst):
    print()
    for row in range(0, 3):
        if row != 0:
            print('               +               +')
        for line in range(0, 7):
            print(*pattern_lst[row][line])


def prnt_game_map():
    r = 0
    print(2 * '\n')
    for line in range(1, 6):
        if (line == 1) or (line == 3) or (line == 5):
            print(f'            {tic_tac[r][0]} │ {tic_tac[r][1]} │ {tic_tac[r][2]}')
            r += 1
        elif (line == 2) or (line == 4):
            print(f'           ---+---+---')


def diagonal_up_check():
    x_count, o_count = 0, 0
    if tic_tac_display[0][2] == 'X':
        x_count += 1
    if tic_tac_display[1][1] == 'X':
        x_count += 1
    if tic_tac_display[2][0] == 'X':
        x_count += 1
    if tic_tac_display[0][2] == 'O':
        o_count += 1
    if tic_tac_display[1][1] == 'O':
        o_count += 1
    if tic_tac_display[2][0] == 'O':
        o_count += 1
    if (x_count == 3) or (o_count == 3):
        return True
    else:
        return False


def diagonal_down_check():
    x_count, o_count = 0, 0
    # Check for up-sloping diagonal winner.
    for i in reversed(range(0, 3)):
        if tic_tac_display[i][i] == 'X':
            x_count += 1
        if tic_tac_display[i][i] == 'O':
            o_count += 1
    if (x_count == 3) or (o_count == 3):
        return True
    else:
        return False


def winner_check():
    win_status = False
    # Check for horizontal winner.
    for row in range(0, 3):
        if (tic_tac_display[row].count('X') == 3) or (tic_tac_display[row].count('O') == 3):
            win_status = True
    # Check for vertical winner.
    for col in range(0, 3):
        x_count, o_count = 0, 0
        for row in range(0, 3):
            if tic_tac_display[row][col] == 'X':
                x_count += 1
            if tic_tac_display[row][col] == 'O':
                o_count += 1
        if (x_count == 3) or (o_count == 3):
            win_status = True
    if diagonal_up_check():
        win_status = True
    if diagonal_down_check():
        win_status = True
    return win_status


def get_cell():
    ok_inputs = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    input_num = ''
    while input_num not in ok_inputs:
        try:
            input_num = int(msvcrt.getch())
        except ValueError:
            print('Input a number between 1 and 9.')
            continue
    return input_num


def game_func(max_window):
    # line_pattern = ['               ', '               ', '               ']
    # row_pattern = 7 * [line_pattern]
    # game_pattern = 3 * [row_pattern]
    game_pattern = [[['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               ']],
                    [['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               ']],
                    [['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               '],
                     ['               ', '               ', '               ']]]
    cells_blank = 9
    print("\tTic Tac Toe\n")
    print("\tJeff's Python Bootcamp milestone project coded February, 2019" + 7 * '\n\n')
    if max_window:
        print('\tMaximize the window before starting this game.\n')
    print("\n\tWho goes first - X's or O's?" + 3 * '\n')

    while True:
        answer = str(msvcrt.getch())
        if ('x' in answer) or ('X' in answer):
            mark = 'X'
            break
        elif ('o' in answer) or ('O' in answer):
            mark = 'O'
            break
        else:
            print("\n\tYour choices are 'X' or 'O'.\n")

    call('cls', shell=True)
    prnt_game(game_pattern)
    prnt_game_map()

    while cells_blank > 0:
        print(f"\n\t Enter your mark location with number keys.\n")
        print(f"\n\t It is {mark}'s turn... \n")

        # cell_num = str(int(msvcrt.getch()))
        cell_num = str(get_cell())

        for row in range(0, 3):
            for col in range(0, 3):
                if tic_tac[row][col] == cell_num:
                    tic_tac_display[row][col] = mark
                    game_pattern = populate_marks(mark, row, col, game_pattern)

        call('cls', shell=True)
        prnt_game(game_pattern)
        prnt_game_map()

        if winner_check():
            print(3 * '\n')
            print(f"         {mark}'s W I N !!!")
            break
        else:
            if cells_blank == 1:
                print('\n\t This game is a draw!')
                break
        cells_blank -= 1
        if mark == 'X':
            mark = 'O'
        else:
            mark = 'X'


play = True
maximize_window_note = True
while play:
    tic_tac_display = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    print(80 * '\n')
    game_func(maximize_window_note)
    maximize_window_note = False
    print(f"\n\t Play again?... (Y/N)\n")
    play_again = str(msvcrt.getch())
    if 'n' in play_again or 'N' in play_again:
        play = False
