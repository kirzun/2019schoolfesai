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
        self.cb = np.array(([-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1]))
        self.move = None
        self.skip = 0
        self.count = 0
    
    def BPf(self, board, stone): #盤面評価計算
        return np.sum(self.BP[np.where(board == stone)] * rnd.random() * 3)
    
    def FSf(self, board, stone, st): #相手に取られない確定石の評価計算
        return (((np.count_nonzero(board[0:8:7, :] == stone) + np.count_nonzero(board[:, 0:8:7] == stone)) - \
                 (np.count_nonzero(board[0:8:7, :] == st) + np.count_nonzero(board[:, 0:8:7] == st))) + rnd.random() * 3) * 11
    
    def CNf(self, board, stone, nst): #候補数(着手可能なマス数)の評価計算
        k = 0
        
        for x in range(0, 8):
            for y in range(0, 8):
                for i, tc in enumerate(self.cb):
                    c = tc.copy()
                    if 0 <= x + c[0] <= 7 and 0 <= y + c[1] <= 7:
                        if nst == board[x + c[0], y + c[1]]:
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
        maxv, minv, v, Mpos, stc, stcr = -float("inf"), float("inf"), -float("inf"), [0, 0], 2, 1
        self.count += 1
        if self.count % 1000 == 0:
            print(self.count)
        if stone:
            stc = 1
            stcr = 2
        if depth == 0:
            return self.Eva(board, stc, stcr), None
        
        # 置ける手全てを試して置いた後(ひっくり返した)と座標を配列に格納していく
        self.skip = 0
        iflag = jflag = False
        while(1):
            nodes = [] # 手、　座標
            ECpos = [] # 着手可能な座標
            ECpos = self.EC(board, stc, stcr)
            
            if ECpos:
                cboard = cp.deepcopy(board)
                nodes = [self.CBR(cboard, pos, stc, stcr) for pos in ECpos]
                nodeEva = np.argsort([self.Eva(board, stc, stcr) for child in nodes])[::-1]
                tempnodes = nodes.copy()
                nodes = [tempnodes[i] for i in nodeEva]
                break
            else:
                self.skip += 1
                stone = not(stone)
                if stone:
                    stc = 1
                    stcr = 2
                    iflag = True
                else:
                    stc = 2
                    stcr = 1
                    jflag = True
                if iflag and jflag:
                    self.skip = 0
                    return self.Eva(board, stc, stcr), None
        
        child = nodes[0]
        Mpos = child[1]
        
        if self.move == stone:
            maxv = v = self.NegaScout(child[0][0], child[1], not(stone), a, b, depth - 1)[0]

            if b <= v:
                return v, None
            elif a < v:
                a = v
                
            for child in nodes:
                v = self.NegaScout(child[0][0], child[1], not(stone), b - 1, b, depth - 1)[0]
                if b <= v:
                    return v, None
                elif a < v:
                    a = v
                    v = self.NegaScout(child[0][0], child[1], not(stone), a, b, depth - 1)[0]
                    if b <= v:
                        return v, None
                    elif a < v:
                        a = v
                if maxv < v:
                    maxv = v
                    Mpos = child[1]
                    
            return maxv, Mpos[0]
            
        else:
            minv = v = self.NegaScout(child[0][0], child[1], not(stone), a, b, depth - 1)[0]

            if v <= a:
                return v, None
            elif b > v:
                b = v
                
            for child in nodes:
                v = self.NegaScout(child[0][0], child[1], not(stone), b - 1, b, depth - 1)[0]
                if v <= a:
                    return v, None
                elif b > v:
                    b = v
                    v = self.NegaScout(child[0][0], child[1], not(stone), a, b, depth - 1)[0]
                    if v <= a:
                        return v, None
                    elif b > v:
                        b = v
                if minv > v:
                    minv = v
                    Mpos = child[1]
                    
            return minv, Mpos[0]
    
    def EC(self, board, stone, nst): #着手可能なマスを見つける
        pos = []
        for x in range(0, 8):
            for y in range(0, 8):
                if board[x, y] == 0:
                    for i, tc in enumerate(self.cb):
                        c = tc.copy()
                        if 0 <= x + c[0] <= 7 and 0 <= y + c[1] <= 7:
                            if nst == board[x + c[0], y + c[1]]:
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
     
    def CBR(self, board, pos, stone, nst): # 反転
        board[pos[0], pos[1]] = stone
        for i, tc in enumerate(self.cb):
            c = tc.copy()
            if 0 <= pos[0] + c[0] <= 7 and 0 <= pos[1] + c[1] <= 7:
                if nst == board[pos[0] + c[0], pos[1] + c[1]]:
                    for j in range(1, 8):
                        c += self.cb[i]
                        if not 0 <= pos[0] + c[0] <= 7 or not 0 <= pos[1] + c[1] <= 7:
                            break
                        elif board[pos[0] + c[0], pos[1] + c[1]] == 0:
                            break
                        elif board[pos[0] + c[0], pos[1] + c[1]] == stone:
                            for k in range(j, 0, -1):
                                c -= self.cb[i]
                                board[pos[0] + c[0], pos[1] + c[1]] = stone
                            break

        return [[board], [pos]]
        
    def Eva(self, board, stone, st): #評価計算
        eva = 0 #総評価値
        eva += self.BPf(board, stone) * 2
        eva += self.FSf(board, stone, st) * 5
        eva += self.CNf(board, stone, st)
        eva = eva * (self.skip + 1)
        self.skip = 0
        return eva
        
    def play(self, board, stone):
        k = np.count_nonzero(board == 0)
        k = 8 - k // 10
        if k % 2 == 1:
            k -= 1
        self.count = 0
        print("---------------------")
        print(k)
        self.move = stone
        return self.NegaScout(board, None, stone, -float("inf"), float("inf"), k)
        