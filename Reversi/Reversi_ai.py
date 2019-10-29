# -*- coding: utf-8 -*-
import numpy as np
import random as rnd
import copy as cp

class reversiAI:
    def __init__(self):
        #盤面評価値
        self.BP = np.array([[ 45, -11,  4, -1, -1,  4, -11,  45],
                            [-11, -16, -1,  3,  3, -1, -16, -11],
                            [  4,  -1,  2, -1, -1,  2,  -1,   4],
                            [ -1,  -3, -1,  0,  0, -1,  -3,  -1],
                            [ -1,  -3, -1,  0,  0, -1,  -3,  -1],
                            [  4,  -1,  2, -1, -1,  2,  -1,   4],
                            [-11, -16, -1,  3,  3, -1, -16, -11],
                            [ 45, -11,  4, -1, -1,  4, -11,  45],])
        self.board = None
        self.stone = None
        self.cb = np.array(([-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1]))
    
    def BPf(self, board, stone): #盤面評価計算
        bp = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if board[i, j] == stone:
                    bp = self.BP[i, j] * rnd.random() * 3
                    
        return bp
    
    def FSf(self, board, stone): #相手に取られない確定石の評価計算
        stonek = [0, 0]
        for i in range(0, 8, 7):
            for j in range(0, 8):
                if board[i, j] == stone:
                    stonek[0] += 1
                elif board[i, j] != stone and board[i, j] != 0:
                    stonek[1] += 1
                    
        for i in range(0, 8):
            for j in range(0, 8, 7):
                if board[i, j] == stone:
                    stonek[0] += 1
                elif board[i, j] != stone and board[i, j] != 0:
                    stonek[1] += 1
                    
        return ((stonek[0] - stonek[1]) + rnd.random() * 3) * 11
        
    def CNf(self, board, stone): #候補数(着手可能なマス数)の評価計算
        k = 0
        
        for x in range(0, 8):
            for y in range(0, 8):
                for i, tc in enumerate(self.cb):
                    c = tc.copy()
                    if 0 <= x + c[0] <= 7 and 0 <= y + c[1] <= 7:
                        nst = board[x + c[0], y + c[1]]
                        if nst != 0 and nst != stone:
                            for j in range(1, 8):
                                c += self.cb[i]
                                if not 0 <= x + c[0] <= 7 or not 0 <= y + c[1] <= 7:
                                    break
                                elif board[x + c[0], y + c[1]] == 0:
                                    break
                                elif board[x + c[0], y + c[1]] == stone:
                                    k += 1
                                    break
                            
        return (k + rnd.random() * 2) * 10
    
    def NegaScout(self, board, pos, stone, a, b, depth): #ネガスカウト法
        maxv, v, Mpos, stc = -float("inf"), -float("inf"), [0, 0], 2
        if stone:
            stc = 1
        if depth == 0:
            return -self.Eva(board, stone), None
        
        # 置ける手全てを試して置いた後(ひっくり返した)と座標を配列に格納していく
        nodes = [] # 手、　座標
        ECpos = [] # 着手可能な座標
        ECpos = self.EC(board, stc)
        if ECpos:
            for pos in ECpos:
                cboard = cp.deepcopy(board)
                nodes.append(self.CBR(cboard, pos, stc))
        
        if not nodes:
            return -self.Eva(board, stone), None
        
        child = nodes[0]
        Mpos = child[1]
        v, _ = self.NegaScout(child[0][0], child[1], not(stone), -b, -a, depth - 1)
        maxv = v
        if b <= v:
            return -v, None
        elif a < v:
            a = v
            
        for x in range(1, len(nodes)):
            v, _ = self.NegaScout(nodes[x][0][0], nodes[x][1], not(stone), -a - 1, -a, depth - 1)
            if b <= v:
                return -v, None
            elif a < v:
                a = v
                v, _ = self.NegaScout(nodes[x][0][0], nodes[x][1], not(stone), -b, -a, depth - 1)
                if b <= v:
                    return -v, None
                elif a < v:
                    a = v
            if maxv < v:
                maxv = v
                Mpos = nodes[x][1]
        return -maxv, Mpos[0]
        
    def EC(self, board, stone): #着手可能なマスを見つける
        pos = []
        for x in range(0, 8):
            for y in range(0, 8):
                if board[x, y] == 0:
                    for i, tc in enumerate(self.cb):
                        c = tc.copy()
                        if 0 <= x + c[0] <= 7 and 0 <= y + c[1] <= 7:
                            nst = board[x + c[0], y + c[1]]
                            if nst != 0 and nst != stone:
                                for j in range(1, 8):
                                    c += self.cb[i]
                                    if not 0 <= x + c[0] <= 7 or not 0 <= y + c[1] <= 7:
                                        break
                                    elif board[x + c[0], y + c[1]] == 0:
                                        break
                                    elif board[x + c[0], y + c[1]] == stone:
                                        pos.append([x, y])
                                        break
                            
        return pos
                                
    def CBR(self, board, pos, stone): # 反転
        st = stone
        board[pos[0], pos[1]] = st
        for i, tc in enumerate(self.cb):
            c = tc.copy()
            if 0 <= pos[0] + c[0] <= 7 and 0 <= pos[1] + c[1] <= 7:
                nst = board[pos[0] + c[0], pos[1] + c[1]]
                if nst != 0 and nst != st:
                    for j in range(1, 8):
                        c += self.cb[i]
                        if not 0 <= pos[0] + c[0] <= 7 or not 0 <= pos[1] + c[1] <= 7:
                            break
                        elif board[pos[0] + c[0], pos[1] + c[1]] == 0:
                            break
                        elif board[pos[0] + c[0], pos[1] + c[1]] == st:
                            for k in range(j, 0, -1):
                                c -= self.cb[i]
                                board[pos[0] + c[0], pos[1] + c[1]] = st
                            break
                        
        return [[board], [pos]]
        
    def Eva(self, board, stone): #評価計算
        eva = 0 #総評価値
        eva += self.BPf(board, stone) * 2
        eva += self.FSf(board, stone) * 5
        eva += self.CNf(board, stone)
        return eva
        
    def play(self, board, stone):
        self.board = board
        self.stone = stone
        return self.NegaScout(board, None, stone, -float("inf"), float("inf"), 4)
        