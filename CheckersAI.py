import Checkers as C

class Bot:
    def __init__(self, depth=5):
        self.__depth = depth
    def __minimax(self, board, depth, colour, total_pieces, stalemate):
        c_reg, n_reg, c_king, n_king = board.get_count(colour)
        if depth == self.__depth:
            piece_diff = c_reg + 2*c_king - (n_reg + 2*n_king)
            return (piece_diff / total_pieces) * (self.__depth + 1 - depth)
        if board.get_winner() == colour:
            return self.__depth + 1 - depth
        if board.get_winner() != None:
            return (self.__depth + 1)*-1 + depth
        if c_king == 1 and n_king == 1 and c_reg + n_reg == 0:
            if stalemate:
                return 0
            else:
                stalemate = True
        if (colour == 'White' and colour == board.get_turn()) or (colour == 'Black' and colour != board.get_turn()):
            locs = board.get_white()
        else:
            locs = board.get_black()
        if not locs: print('Unable to find movable pieces')
        if colour == board.get_turn():
            best_val = None
            for x, y in locs:
                for move in board.get_moves(x, y):
                    temp_board = board.copy()
                    if temp_board.move(x, y, move[0], move[1]):
                        value = self.__minimax(temp_board, depth+1,
                                               colour, total_pieces, stalemate)
                        if best_val == None or value > best_val:
                            best_val = value
                    else:
                        print('Invalid Move?')
                    temp_board.destroy()
        else:
            best_val = None
            for x, y in locs:
                for move in board.get_moves(x, y):
                    temp_board = board.copy()
                    if temp_board.move(x, y, move[0], move[1]):  
                        value = self.__minimax(temp_board, depth+1,
                                               colour, total_pieces, stalemate)
                        if best_val == None or value < best_val:
                            best_val = value
                    else:
                        print('Invalid Move?')
                    temp_board.destroy()
        return best_val
    def best_move(self, board, colour):
        best_val = None
        best_move = None
        if not isinstance(board, C.Board):
            raise TypeError('board must be a Board class from the Checkers module.')
        if not isinstance(colour, str):
            raise TypeError('colour must be a string.')
        if colour != 'White' and colour != 'Black':
            raise ValueError('colour must be either "Black" or "White".')
        if colour == 'White':
            locs = board.get_white()
        else:
            locs = board.get_black()
        c_reg, n_reg, c_king, n_king = board.get_count(colour)
        total_pieces = c_reg + 2*c_king + n_reg + 2*n_king
        for (x, y) in locs:
            for move in board.get_moves(x, y):
                temp_board = board.copy()
                if temp_board.move(x, y, move[0], move[1]):
                    value = self.__minimax(temp_board, 0, colour, total_pieces, False)
                    if best_val == None or value > best_val:
                        best_val = value
                        best_move = (x,y,move[0],move[1])
                temp_board.destroy()
        return best_move
