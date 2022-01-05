class Checker:
    def __init__(self, colour, king=False):
        if not isinstance(king, bool):
            raise TypeError('king must be a boolean.')
        if not isinstance(colour, str):
            raise TypeError('colour must be a string.')
        if not colour == 'Black' and not colour == 'White':
            raise ValueError('colour must be either "Black" or "White".')
        self.__king = king
        self.__colour = colour
    def is_king(self):
        return self.__king
    def set_king(self, king):
        if not isinstance(king, bool):
            raise TypeError('king must be a bool.')
        self.__king = king
    def get_colour(self):
        return self.__colour
    def copy(self):
        return Checker(self.__colour, king=self.__king)
    def destroy(self):
        del self

class Board:
    def __init__(self, close_side, board=[], last_move=None, winner=None, turn='Black'):
        if not isinstance(board, list):
            raise TypeError('board must be an 8x4 2D list containing only Checker and None types.')
        if not isinstance(close_side, str):
            raise TypeError('close_side must be a string.')
        if board and len(board) != 8:
            raise ValueError('board must have 8 rows.')
        if close_side != 'Black' and close_side != 'White':
            raise ValueError('close_side must be either "Black" or "White".')
        for row in board:
            if len(row) != 4:
                raise ValueError('board must have 4 columns for all rows.')
            for value in row:
                if value != None and not isinstance(value, Checker):
                    raise ValueError('board must only contain Checker and None types.')
        self.__board = [[None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None]]
        self.__close_side = close_side
        self.__last_move = last_move
        self.__winner = winner
        self.__turn = turn
        if close_side == 'Black':
            self.__far_side = 'White'
        else:
            self.__far_side = 'Black'
        if board:
            for i, row in enumerate(board):
                for j, value in enumerate(row):
                    if isinstance(value, Checker):
                        self.__board[i][j] = value.copy()
    def reset_board(self):
        for i, row in enumerate(self.__board):
                for j, value in enumerate(row):
                    if isinstance(value, Checker):
                        del value
                    if i < 3:
                        self.__board[i][j] = Checker(self.__far_side)
                    elif i > 4:
                        self.__board[i][j] = Checker(self.__close_side)
                    else:
                        self.__board[i][j] = None
    def print(self):
        string = '\n'
        for i, row in enumerate(self.__board):
            string+='+---+---+---+---+---+---+---+---+\n'
            if i%2:
                string+='|'
            for value in row:
                if not i%2:
                    string+='|   |'
                if isinstance(value, Checker):
                    if value.get_colour() == 'White':
                        if value.is_king():
                            string+= 'WK '
                        else:
                            string+=' ○ '
                    else:
                        if value.is_king():
                            string+= 'BK '
                        else:
                            string+=' ● '
                else:
                    string+='   '
                if i%2:
                    string+='|   |'
            if i%2:
                string+='\n'
            else:
                string+='|\n'
        string+='+---+---+---+---+---+---+---+---+\n'
        return string
    def copy(self):
        new_board = []
        for row in self.__board:
            new_row = []
            for value in row:
                if isinstance(value, Checker):
                    new_row.append(value.copy())
                else:
                    new_row.append(value)
            new_board.append(new_row)
        return Board(self.__close_side, board=new_board, last_move=self.__last_move,
                     winner = self.__winner, turn=self.__turn)
    def destroy(self):
        for row in self.__board:
            for value in row:
                if isinstance(value, Checker):
                    value.destroy()
        del self
    def get_black(self):
        lst = self.__get_colour('Black')
        if self.__far_side == 'Black':
            lst.reverse()
        return lst
    def get_white(self):
        lst = self.__get_colour('White')
        if self.__far_side == 'White':
            lst.reverse()
        return lst
    def __get_colour(self, colour):
        lst = []
        for i, row in enumerate(self.__board):
            for j, value in enumerate(row):
                if isinstance(value, Checker) and value.get_colour() == colour:
                    lst.append((j, i))
        return lst
    def get_winner(self):
        return self.__winner
    def get_turn(self):
        return self.__turn
    def get_count(self, colour):
        if not isinstance(colour, str):
            raise TypeError('colour must be a string.')
        if colour != 'Black' and colour != 'White':
            raise ValueError('colour must be either "Black" or "White".')
        c_reg = 0
        n_reg = 0
        c_king = 0
        n_king = 0
        for row in self.__board:
            for value in row:
                if isinstance(value, Checker):
                    if value.get_colour() == colour:
                        if value.is_king():
                            c_king += 1
                        else:
                            c_reg += 1
                    else:
                        if value.is_king():
                            n_king += 1
                        else:
                            n_reg += 1
        return c_reg, n_reg, c_king, n_king
    def __can_jump(self, x, y):
        checker = self.__board[y][x]
        dirs = []
        if not isinstance(checker, Checker):
            return dirs
        check_x = [(x-(y%2), x-1), (x+(1-(y%2)), x+1), (x-(y%2), x-1), (x+(1-(y%2)), x+1)]
        check_y = [(y-1, y-2), (y-1, y-2), (y+1, y+2), (y+1, y+2)]
        sides = [self.__close_side, self.__close_side, self.__far_side, self.__far_side]
        to_add = ['UL', 'UR', 'DL', 'DR']
        for i in range(4):
            if (check_y[i][0] >= 0 and check_y[i][0] <= 7 and
                check_x[i][0] >= 0 and check_x[i][0] <= 3 and
                check_y[i][1] >= 0 and check_y[i][1] <= 7 and
                check_x[i][1] >= 0 and check_x[i][1] <= 3):
                check_1 = self.__board[check_y[i][0]][check_x[i][0]]
                check_2 = self.__board[check_y[i][1]][check_x[i][1]]
                if ((checker.get_colour() == sides[i] or checker.is_king()) and
                    isinstance(check_1, Checker) and
                    check_1.get_colour() != checker.get_colour() and
                    isinstance(check_2, type(None))):
                    dirs.append(to_add[i])
        return dirs
    def move(self, x, y, ydir, xdir):
        if not isinstance(x, int):
            raise TypeError('x must be an integer.')
        if not isinstance(y, int):
            raise TypeError('y must be an integer.')
        if not isinstance(xdir, str):
            raise TypeError('xdir must be a string.')
        if not isinstance(ydir, str):
            raise TypeError('ydir must be a string.')
        if x < 0 or x > 3:
            raise ValueError('x must be between 0 and 3 (inclusive).')
        if y < 0 or y > 7:
            raise ValueError('y must be between 0 and 7 (inclusive).')
        if xdir != 'L' and xdir != 'R':
            raise ValueError('xdir must either be "L" or "R".')
        if ydir != 'U' and ydir != 'D':
            raise ValueError('ydir must either be "U" or "D".')
        valid_moves = self.get_moves(x, y)
        if not (ydir, xdir) in valid_moves:
            return False
        checker = self.__board[y][x]
        colour = checker.get_colour()
        dir_dict_1 = {'L':x-(y%2), 'R':x+(1-(y%2)), 'U':y-1, 'D':y+1}
        dir_dict_2 = {'L':x-1, 'R':x+1, 'U':y-2, 'D':y+2}
        jumps = self.__can_jump(x, y)
        if ydir+xdir in jumps:
            new_x = dir_dict_2[xdir]
            new_y = dir_dict_2[ydir]
            self.__board[dir_dict_1[ydir]][dir_dict_1[xdir]].destroy()
            self.__board[dir_dict_1[ydir]][dir_dict_1[xdir]] = None
            self.__last_move = (new_x, new_y)
        else:
            new_x = dir_dict_1[xdir]
            new_y = dir_dict_1[ydir]
            self.__last_move = None
        self.__board[new_y][new_x] = checker
        self.__board[y][x] = None
        if ((colour == self.__close_side and new_y == 0) or
            (colour == self.__far_side and new_y == 7)):
            checker.set_king(True)
        if not self.get_white():
            self.__winner = 'Black'
        elif not self.get_black():
            self.__winner = 'White'
        required_moves = []
        if self.__last_move != None:
            required_moves = self.__can_jump(self.__last_move[0], self.__last_move[1])
        if self.__turn == 'Black' and not required_moves:
            self.__turn = 'White'
        elif not required_moves:
            self.__turn = 'Black'
        return True
    def get_moves(self, x, y):
        if not isinstance(x, int):
            raise TypeError('x must be an integer.')
        if not isinstance(y, int):
            raise TypeError('y must be an integer.')
        if x < 0 or x > 3:
            raise ValueError('x must be between 0 and 3 (inclusive).')
        if y < 0 or y > 7:
            raise ValueError('y must be between 0 and 7 (inclusive).')
        valid_moves = []
        if self.__winner != None: return valid_moves
        if isinstance(self.__board[y][x], type(None)): return valid_moves
        required_moves = []
        colour = self.__board[y][x].get_colour()
        if self.__turn != colour: return valid_moves
        if self.__last_move != None:
            required_moves = self.__can_jump(self.__last_move[0], self.__last_move[1])
            if required_moves and (x != self.__last_move[0] or y != self.__last_move[1]):
                return valid_moves
        jumps = self.__can_jump(x, y)
        for move in jumps:
            valid_moves.append((move[0], move[1]))
        if valid_moves: return valid_moves
        all_pieces = self.__get_colour(colour)
        for ix, iy in all_pieces:
            if self.__can_jump(ix, iy):
                return valid_moves
        dir_dict = {'L':x-(y%2), 'R':x+(1-(y%2)), 'U':y-1, 'D':y+1}
        if self.__board[y][x].is_king(): ydirs = ['U', 'D']
        elif colour == self.__close_side: ydirs = ['U']
        else: ydirs = ['D']
        for ydir in ydirs:
            for xdir in ['L', 'R']:
                if (dir_dict[xdir] >= 0 and dir_dict[xdir] < 4 and
                    dir_dict[ydir] >= 0 and dir_dict[ydir] < 8 and
                    isinstance(self.__board[dir_dict[ydir]][dir_dict[xdir]], type(None))):
                    valid_moves.append((ydir, xdir))
        return valid_moves

if __name__ == '__main__':
    b = Board("Black")
    b.reset_board()
    print(b.print())
    def test_moves():
        for i in range(8):
            for j in range(4):
                print("Row "+str(i)+", Column "+str(j)+": "+str(b.get_moves(j, i)))
                    
