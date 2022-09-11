from cgitb import small
from operator import indexOf
import numpy as np
from scipy.signal import convolve2d
from colorama import Fore, Back, Style
import helper

#colum means the number

class Connect_four:

    def __init__(self):
        self.board = np.zeros((7,6), dtype=int)
        self.width = len(self.board)
        self.height = len(self.board[0])
        self.display_dic = {
            0: " ",
            1: (Fore.RED + "X"),
            -1: (Fore.GREEN + "O")
        }
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        self.detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        self.state = np.zeros(self.width, dtype = int)

    def is_move_possible(self, column):
        return self.state[column] < self.height 

    def reset(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j] = 0

    def display(self):
        display_board = np.rot90(self.board)
        for i in range(self.height):
            print("|", end =" ")
            for j in range(self.width):
                print(self.display_dic[display_board[i][j]], end="")
                print(Style.RESET_ALL, end="")
                print(" | ", end="")
            print("")

    def winner (self, player, move):
        return self.column(move, player) or self.row(self.state[move]-1, player) or self.diagonal(move, player)

    def column(self, column, player):
        row = self.state[column]
        
        if row < 4 or player != self.board[column][row-1]:
            return False
        for i in range(1, 4):
            if self.board[column][row-1-i] != self.board[column][row-1]:
                return False
        return True

    def row(self, row, player): 
        for i in range(self.width-3):
            if player == self.board[i][row] == self.board[i+1][row] == self.board[i+2][row] == self.board[i+3][row]:
                return True
        return False

    def diagonal(self, column, player):
        row = self.state[column] - 1
        return self.diagonal2(column, row, player) or self.diagonal1(column, row, player) # descend à droite
        
    def diagonal1(self, column, row, player): #descendant
        new_row = min(self.height-1, row + column)
        column = column - (new_row - row)
        row = new_row

        i=0
        while column+(i+3) < self.width and row-(i+3) >= 0:
            if player == self.board[column+i][row-(i)] == self.board[column+(i+1)][row-(i+1)] == self.board[column+(i+2)][row-(i+2)] == self.board[column+(i+3)][row-(i+3)]:
                return True
            i+=1
        return False


    def diagonal2(self, column, row, player): #ascendant
        new_row = max(0, row-column)
        column = column - (row - new_row)
        row = new_row
        
        i=0
        while column+i+3 < self.width and row+i+3 < self.height:
            if player == self.board[column+i][row+i] == self.board[column+i+1][row+i+1] == self.board[column+i+2][row+i+2] == self.board[column+i+3][row+i+3]:
                return True
            i+=1
        return False
            
    def actions(self):
        res = np.arange(self.width)
        res = np.delete(res, np.where(self.state == self.height))
        return res

    def trans(self, column, player):
        self.board[column][self.state[column]] = player
        self.state[column] += 1
  
    def undo(self, column):
        self.state[column] -=1
        self.board[column][self.state[column]] = 0
        
    def final(self, move):
        if np.sum(self.state) < 7:
            return False
        return len(self.actions()) == 0 or self.winner(1, move) or self.winner(-1, move)

    

    def utility(self, move):
        # player : dernier joueur qui a joué
        if self.winner(-1, move):
            return -1
        elif self.winner(1, move):
            return 1
        else:
            res = 0
            for i in range(self.width):
                res += len(np.where(self.board[i] == -1)[0]) * abs((self.width-1)/2-i) # enlève points pour ennemis au centre
                res -= len(np.where(self.board[i] == 1)[0]) * abs((self.width-1)/2-i) # ajoute points pour ennemis au centre
            return helper.sigmoid(res)


    def mini_alphabeta(self, alpha, beta, player, move, depth):
        # comme minimax mais en regardant alpha ou beta
        # pour couper
        if depth == 0 or self.final(move):
            return self.utility(move)
        min_eval = np.inf
        for action in self.actions():
            self.trans(action, player)
            v = self.maxi_alphabeta(alpha, beta, -player, action, depth-1)
            min_eval = min(min_eval, v)
            self.undo(action)
            if min_eval <= alpha:
                break
            beta = min(beta, min_eval)     
        return min_eval

    def maxi_alphabeta(self, alpha, beta, player, move, depth):
        # comme minimax mais en regardant alpha ou beta
        # pour couper
        if depth == 0 or self.final(move):
            return self.utility(move)
        max_eval = -np.inf
        for action in self.actions():
            self.trans(action, player)
            v = self.mini_alphabeta(alpha, beta, -player, action, depth-1)
            max_eval = max(max_eval, v)
            self.undo(action)
            if beta <= max_eval:
                break
            alpha = max(alpha, max_eval)
        return max_eval

    def alphabeta(self, player, depth=6):
        # calcul de l'argmax
        beta = np.inf
        alpha = -np.inf
        maxi = -np.inf
        for action in self.actions():
            self.trans(action, player)
            eval = self.mini_alphabeta(alpha, beta, -player, action, depth)
            if eval > maxi:
                maxi = eval
                best_action = action
            self.undo(action)
                
        return best_action, maxi
        

    

        


