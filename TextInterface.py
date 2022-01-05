import Checkers as C
import CheckersAI as CAI

def turn():
    if b.get_turn() == player:
        idx = None
        pieces = {}
        for i in range(8):
            for j in range(4):
                moves = b.get_moves(j, i)
                if moves:
                    pieces[(j, i)] = moves
        while idx == None or idx == -1:
            if len(pieces) == 1:
                x = list(pieces.keys())[0][0]
                y = list(pieces.keys())[0][1]
                moves = b.get_moves(x, y)
            else:
                for i, key in enumerate(list(pieces.keys())):
                    print(str(i+1)+'. Y: '+str(key[1]+1)+'   X: '+
                          str((key[0]+(1-(key[1]%2)))*2+(key[1]%2)))
                print('Above is a menu of all possible pieces that can be moved.')
                while True:
                    user = input('Please enter the index of the piece you would like to move (1-'+str(len(pieces))+'). ')
                    try:
                        user = int(user)-1
                        if user >= 0 and user < len(pieces):
                            break
                    except ValueError:
                        pass
                    print('Invalid Input.')
                x = list(pieces.keys())[user][0]
                y = list(pieces.keys())[user][1]
                moves = pieces[list(pieces.keys())[user]]
            if len(moves) > 1:
                move_dict = {'D':'Down', 'U':'Up', 'L':'Left', 'R':'Right'}
                for i, moveset in enumerate(moves):
                    print(str(i+1)+". "+move_dict[moveset[0]]+" and "+move_dict[moveset[1]])
                print('Above is a menu of all possible moves for the selected piece.')
                while True:
                    user = input('Please enter the index of the move you would like to make (1-'+str(len(moves))+'),\nor enter 0 to go back. ')
                    try:
                        idx = int(user)-1
                        if idx >= -1 and idx < len(moves):
                            break
                    except ValueError:
                        pass
                    print('Invalid Input.')
            elif len(moves) == 1:
                idx = 0
            else:
                print('The location you have selected does not have any legal moves. Please try again.')
        b.move(x, y, moves[idx][0], moves[idx][1])
    else:
        print('Calculating...')
        best = ai.best_move(b, bot)
        if best != None: 
            b.move(best[0], best[1], best[2], best[3])
    print(b.print())
    winner = b.get_winner()
    if winner != None:
        print(winner+' wins!')
        return winner
    turn()
            
while True:
    start = input('Would you like to start? Enter Y for yes or N for no. ')
    if start.upper() == 'Y':
        player = 'Black'
        bot = 'White'
        break
    elif start.upper() == 'N':
        player = 'White'
        bot = 'Black'
        break
    else:
        print('Invalid Input.')
while True:
    depth = input('Enter the desired depth of the bot.\nHigher depth means a better bot but longer calculation times.\nReccomended depth is 5. ')
    try:
        depth = int(depth)
        break
    except ValueError:
        print('Invalid Input.')
b = C.Board(player)
ai = CAI.Bot(depth)
b.reset_board()
print(b.print())
turn()
