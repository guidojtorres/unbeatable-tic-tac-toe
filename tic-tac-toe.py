import random, copy
def new_board():
    board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
    ]
    return board
def is_board_full(board):
    for col in board:
        for sq in col:
            if sq is None:
                return False
    return True
def render(board):
    to_render = new_board()
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                to_render[x][y] = ' '
            elif board[x][y] == 'X':
                to_render[x][y] = 'X'
            else:
                to_render[x][y] = 'O'
    for x in range(len(to_render)):
        print('|'.join(to_render[x]))
        if x != 2:
            print('-----')
def get_move(board, player):
    while True:
        move = input('Your turn! Please input a number from 1 to 9: ')
        if move in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            break
        else:
            print('Please enter a valid input')
    if move == '1':
        return (0, 0)
    if move == '2':
        return (0, 1)
    if move == '3':
        return (0, 2)
    if move == '4':
        return (1, 0)
    if move == '5':
        return (1, 1)
    if move == '6':
        return (1, 2)
    if move == '7':
        return (2, 0)
    if move == '8':
        return (2, 1)
    if move == '9':
        return (2, 2)
def make_move(board, player, coords):
    new_board = [x for x in board]
    if player == 'player1':
        letter = 'X'
    elif player == 'player2':
        letter = 'O'
    if new_board[coords[0]][coords[1]] == None:
        new_board[coords[0]][coords[1]] = letter
    else:
        print('Invalid move! Try again')
        return make_move(board, player, get_move(board, player))
    return new_board
def get_player(board):
    countable = [item for sublist in board for item in sublist]
    if countable.count('X') == countable.count('O'):
        return 'player1'
    else:
        return 'player2'
def get_winner(board):
    possibilities = [x for x in board]
    possibilities.append([board[0][0], board[1][0], board[2][0]])
    possibilities.append([board[0][1], board[1][1], board[2][1]])
    possibilities.append([board[0][2], board[1][2], board[2][2]])
    possibilities.append([board[0][0], board[1][1], board[2][2]])
    possibilities.append([board[2][0], board[1][1], board[0][2]])
    for x in range(len(possibilities)):
        if possibilities[x].count('X') == 3:
            return 'player1'
        elif possibilities[x].count('O') == 3:
            return 'player2'
    return None
def get_opponent(player):
    if player == 'player1':
        return 'player2'
    else:
        return 'player1'
def random_ai(board, player):
    while True:
        coords = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        if board[coords[0]][coords[1]] == None:
            return coords
def find_winning_moves_ai(board, player):
    if player == 'player1':
        current_player = 'X'
    else:
        current_player = 'O'

    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                board[x][y] = current_player
                if get_winner(board) == player:
                    board[x][y] = None
                    return (x, y)
                else:
                    board[x][y] = None
    while True:
        coords = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        if board[coords[0]][coords[1]] == None:
            return coords
def find_winning_and_losing_moves_ai(board, player):
    if player == 'player1':
        current_player = 'X'
        opposite_player = ['O', 'player2']

    else:
        current_player = 'O'
        opposite_player = ['X', 'player1']

    #Return winning move
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                board[x][y] = current_player
                if get_winner(board) == player:
                    board[x][y] = None
                    return (x, y)
                else:
                    board[x][y] = None
    #Block winning move
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                board[x][y] = opposite_player[0]
                if get_winner(board) == opposite_player[1]:
                    board[x][y] = None
                    return (x, y)
                else:
                    board[x][y] = None

    #Random move
    while True:
        coords = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        if board[coords[0]][coords[1]] == None:
            return coords
def minmax_score(board, player, player_to_optimize):
    winner = get_winner(board)
    if winner is not None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif is_board_full(board):
        return 0

    legal_moves = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                legal_moves.append((x,y))
    scores = []
    for move in legal_moves:
        new_board = tuple(make_move(copy.deepcopy(board), player, move))
        opponent = get_opponent(player)
        score = minmax_score(new_board, opponent, player_to_optimize)
        scores.append(score)
    if player == player_to_optimize:
        return max(scores)
    else:
        return min(scores)
def minmax_ai(board, player):
    best_move = None
    best_score = None

    legal_moves = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                legal_moves.append((x,y))

    for move in legal_moves:
        new_board = make_move(copy.deepcopy(board), player, move)
        opponent = get_opponent(player)
        score = minmax_score(new_board, opponent, player)
        if best_score is None or score > best_score:
            best_move = move
            best_score = score
    return best_move
def play(p1, p2):
    board = new_board()
    while True:
        render(make_move(board, get_player(board), p1(board, 'player1')))
        countable_board = [item for sublist in board for item in sublist]
        if get_winner(board) == 'player1':
            print('Player1 has won!')
            return 1
        elif get_winner(board) == 'player2':
            print('Player2 has won!')
            return 2
        if countable_board.count('X') == 5:
            print('Its a draw!')
            return 0

        print('_____')
        render(make_move(board, get_player(board), p2(board, 'player2')))
        print('_____')
        if get_winner(board) == 'player1':
            print('Player1 has won!')
            return 1
        elif get_winner(board) == 'player2':
            print('Player2 has won!')
            return 2
        if countable_board.count('X') == 5:
            print('Its a draw!')
            return 0
def play_multiple(p1, p2, times):
    count = 0
    p1w = 0
    p2w = 0
    draws = 0
    while count < times:
        if play(p1, p2) == 1:
            p1w += 1
        elif play(p1, p2) == 2:
            p2w += 1
        else:
            draws += 1
        count += 1
    print('Player 1 wins: {} \nPlayer 2 wins: {} \nDraws: {}'.format(p1w, p2w, draws))
play(get_move, minmax_ai)
