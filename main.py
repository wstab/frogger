import os

root, directories, files = next(os.walk('.'))

# returns user file selection
def select_game_file():
    frog_files = []
    # prints files and numbers
    for x in files:
        if '.frog' in x:
            frog_files.append(x)
    for i in range(len(frog_files)):
        print(f'[{i+1}] {frog_files[i]}')
    # asks user for option for file
    choice = int(input('Enter an option: ')) - 1
    # error filtering
    while choice not in range(len(frog_files)):
        print("This isn't a valid choice")
        choice = int(input('Enter an option or filename: ')) - 1
    # returns file selection
    return frog_files[choice]

# displays the roads and the frog at the given indexes (frog_row, frog_col)
def display_board(roads, frog_row, frog_col):
    temp = list(roads[frog_row])
    if frog_col >= len(roads[frog_row]):
        temp.append('\U0001318F')
    else:
        temp[frog_col] = '\U0001318F'
    roads[frog_row] = ''.join(temp)
    for i in range(len(roads)):
        print(roads[i])

# rotates the roads x amount of times based on which turn it is
def rotate(roads, speeds, turn):
    if turn == 0:
        return roads
    board = [' '*len(roads[0])]
    for i in range(len(speeds)):
        speed = int(speeds[i])
        board.append(roads[i+1][-speed:] + roads[i+1][:-speed])
    board.append(' '*len(roads[0]))
    return rotate(board, speeds, turn-1)

# takes in the game file and the type of information we are looking for and returns it
def get_data(game_file, info):
    with open(game_file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if '\n' in lines[i]:
                lines[i] = lines[i][:-1]
        if info == 'board':
            roads = [' '*len(lines[2])] + lines[2:] + [' '*len(lines[2])]
            return roads
        elif info == 'speeds':
            return lines[1]
        elif info == 'jumps':
            first = lines[0].split(' ')
            return first[2]

# checks for any user inputs the would cause index errors or type errors, etc
def check_error(roads, move, frog_row, frog_col, jumps):
    if move not in 'wasdquit' and 'j' not in move[0] or ('j' in move[0] and len(move) != 5):
        print("This isn't a valid input")
        return True
    elif (move == 'w' and frog_row == 0) or (move == 'd' and frog_col == len(roads[frog_row]) - 1) or (move == 'a' and frog_col == 0):
        print("You can't move there")
        return True
    elif 'j' in move:
        move = move.split(' ')
        if jumps == 0:
            print("You've run out of jumps")
            return True
        elif frog_row - int(move[1]) not in range(-1, 2):
            print("You can't jump that far")
            return True
        elif int(move[1]) not in range(len(roads) - 1) or int(move[2]) not in range(len(roads[0]) - 1):
            print("This isn't a valid position to jump")
            return True
    return False


def frogger_game(game_file):
    roads = get_data(game_file, 'board')
    jumps = int(get_data(game_file, 'jumps'))
    speeds = get_data(game_file, 'speeds').split(' ')
    frog_row = 0
    frog_col = len(roads[0])//2
    i = 1
    print(i)
    display_board(roads, frog_row, frog_col)
    loss = False
    move = input('WASDJ >> ').lower()
    # game loop; quit to exit
    while move != 'quit':
        while check_error(roads, move, frog_row, frog_col, jumps):
            move = input('WASDJ >> ')
        print(i+1)
        if move == 's':
            frog_row++
        elif move == 'w':
            frog_row--
        elif move == 'a':
            frog_col--
        elif move == 'd':
            frog_col++
        elif 'j' in move:
            move = move.split(' ')
            frog_row = int(move[1])
            frog_col = int(move[2]) - 1
            jumps -= 1
        # if the row is not 0 or the len(roads) - 1 then the frog must be on a log
        if frog_row != 0 and frog_row != len(roads) - 1 and move != 's' and move != 'w' and 'j' not in move:
            # adds to frog_col to counter the rotation
            frog_col += int(speeds[frog_row - 1])
        rotated_road = rotate(roads, speeds, i)
        # checks for loss or win
        if frog_col >= len(roads[0]) or rotated_road[frog_row][frog_col] == '_':
            loss = True
        display_board(rotated_road, frog_row, frog_col)
        if loss:
            print('You Lost, Sorry Frog')
            move = 'quit'
        elif frog_row == len(roads)-1:
            print('You won, Frog lives to cross another day.')
            move = 'quit'
        else:
            move = input('WASDJ >> ').lower()
        # counts turn
        i++

# calls frogger_game to initialize the game
if __name__ == '__main__':
  selected_game_file = select_game_file()
  frogger_game(selected_game_file)
