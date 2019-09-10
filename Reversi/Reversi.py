# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np

SCR_RECT = Rect(0, 0, 1024, 768) #画面サイズ
BOX = 70 #マス目サイズ

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    Gameflag = True
    fpsfont = pygame.font.Font(None, 48)
    titlemenu = TitleMenu()
    game = Game()
    while (1):
        clock.tick(60) #60fps
        if Gameflag:
            titlemenu.update()
            titlemenu.draw(screen)
        else:
            game.update()
            game.draw(screen)
        screen.blit(fpsfont.render(str(int(clock.get_fps())), True, (50,250,50)), (970, 15))
        pygame.display.update()#画面を更新
        screen.fill((0,0,0))
        keys = pygame.key.get_pressed()#キー処理
        if (Gameflag) & (keys[K_RETURN]):
            Gameflag = False
        elif (Gameflag) & (keys[K_SPACE]):
            Gameflag = False
            game.playerflag = False
        for event in pygame.event.get():#イベント処理
            if (event.type == QUIT) | ((Gameflag) & (keys[K_q])):#閉じるボタンが押されたら終了
                pygame.quit()#Pygameの終了
                sys.exit()
            elif (not Gameflag) & (keys[K_q]):
                Gameflag = True
                game.__init__()

class TitleMenu:
    def __init__(self):
        self.titlefont = pygame.font.Font(None, 210)
        self.title = self.titlefont.render("Reversi", True, (190,180,190))
        self.menufont = pygame.font.Font("ipaexg.ttf", 48)
        self.gmenu1 = self.menufont.render("先攻:ENTER", True, (160,190,230), (10,10,10))
        self.gmenu2 = self.menufont.render("後攻:SPACE", True, (160,190,230), (10,10,10))
        self.qmenu = self.menufont.render("終了:Q", True, (160,190,230), (10,10,10))
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.title, (245, 175))
        screen.blit(self.gmenu1, (380, 425))
        screen.blit(self.gmenu2, (380, 475))
        screen.blit(self.qmenu, (380, 525))
    
class Game:
    def __init__(self):
        self.playerflag = True
        self.screen = None
        self.board = np.zeros(8*8).reshape(8, 8)
        self.board[3:5, 3:5] = [[1, 2], [2, 1]]
        self.stonecolor = True #True:白 False:黒
        self.setpos = np.zeros(2)
    
    def update(self):
        if self.playerflag:
            if self.player():
                self.stonecolor = not(self.stonecolor)
                self.playerflag = not(self.playerflag)
        else:
            if self.ai():
                self.stonecolor = not(self.stonecolor)
                self.playerflag = not(self.playerflag)
    
    def draw(self, screen):
        self.screen = screen
        self.banDraw()
        self.stoneDraw()
        self.banDataDraw()
        self.resultDraw()
        self.recordDraw()
        
    def player(self): #プレイヤー処理
        if self.setStone():
            self.checkBoardReversi()
            print("pl")
            print(self.board)
            
            return True
        else:
            return False
            #置きなおし処理
    
    def ai(self): #AI処理
        """
        AIに盤面を渡して結果を受け取る
        """
        if self.setStone():
            self.checkBoardReversi()
            print("ai")
            print(self.board)
            
            return True
        else:
            return False
    
    def checkBoardReversi(self): #チェックと反転
        #上下左右斜め時計回り
        cb = np.array([[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1]])
        tp = self.setpos
        
        for i, tc in enumerate(cb):
            c = tc.copy()
            st = self.board[tp[0], tp[1]]
            nst = self.board[tp[0] + c[0], tp[1] + c[1]]
            if nst != 0 and nst != st:
                for j in range(1, 8):
                    c += cb[i]
                    if 0 > tp[0] + c[0] > 7 or 0 > tp[1] + c[1] > 7:
                        break
                    elif self.board[tp[0] + c[0], tp[1] + c[1]] == 0:
                        break
                    elif self.board[tp[0] + c[0], tp[1] + c[1]] == st:
                        for k in range(j, 0, -1):
                            c -= cb[i]
                            self.board[tp[0] + c[0], tp[1] + c[1]] = st
                        break
            
    
    def setStone(self): #石配置
        if pygame.mouse.get_pressed()[0]:
            pygame.time.wait(100) #処理が速すぎるので100ミリ秒止める
            pos = pygame.mouse.get_pos()
            #if 置ける範囲内なら(描画処理に合わせる)
            self.setpos = [int(pos[1] / BOX), int(pos[0] / BOX)]
            if self.stonecolor:
                self.board[self.setpos[0], self.setpos[1]] = 1
            else:
                self.board[self.setpos[0], self.setpos[1]] = 2
            
            return True
        else:
            return False

#====================================作ってもらうやつここから
    
    def banDraw(self): #盤面描画
        pass
    
    def stoneDraw(self): #石描画
        pass
    
    def banDataDraw(self): #盤面情報描画
        pass
    
    def resultDraw(self): #戦績描画
        pass
    
    def recordDraw(self): #勝敗結果描画
        pass
    
#====================================ここまで
    
if __name__ == "__main__":
    main()