# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np
from Reversi_ai import reversiAI

AI = reversiAI
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
        self.cb = np.array(([-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1]))
        self.skipflag = False
        self.endcount = 0
        self.endflag = False
    
    def update(self):
        if self.endGame(self.stonecolor):
            self.endcount += 1
            if self.endcount == 2:
                self.endflag = True
            elif self.playerflag:
                self.stonecolor, self.playerflag, self.skipflag = self.boolNot(self.stonecolor, self.playerflag, self.skipflag)
            else:
                self.stonecolor, self.playerflag, self.skipflag = self.boolNot(self.stonecolor, self.playerflag, self.skipflag)
        else:
            self.endcount = 0
            if self.playerflag:
                if self.player():
                    self.stonecolor, self.playerflag, self.skipflag = self.boolNot(self.stonecolor, self.playerflag, self.skipflag)
            else:
                if self.ai():
                    self.stonecolor, self.playerflag, self.skipflag = self.boolNot(self.stonecolor, self.playerflag, self.skipflag)
    
    def draw(self, screen):
        self.screen = screen
        self.banDraw()
        self.stoneDraw()
        self.banDataDraw()
        self.resultDraw()
        if self.endflag:
            self.recordDraw()
        
    def player(self): #プレイヤー処理
        if self.setStone():
            return True
        else:
            return False
    
    def ai(self): #AI処理
        """
        AIに盤面を渡して結果を受け取る
        """
        
        if self.setStone():
            return True
        else:
            return False
    
    def checkBoardReversi(self): #チェックと反転
        tp = self.setpos
        flag = False
        st = self.board[tp[0], tp[1]]
        
        for i, tc in enumerate(self.cb):
            c = tc.copy()
            if 0 <= tp[0] + c[0] <= 7 and 0 <= tp[1] + c[1] <= 7:
                nst = self.board[tp[0] + c[0], tp[1] + c[1]]
                if nst != 0 and nst != st:
                    for j in range(1, 8):
                        c += self.cb[i]
                        if not 0 <= tp[0] + c[0] <= 7 or not 0 <= tp[1] + c[1] <= 7:
                            break
                        elif self.board[tp[0] + c[0], tp[1] + c[1]] == 0:
                            break
                        elif self.board[tp[0] + c[0], tp[1] + c[1]] == st:
                            for k in range(j, 0, -1):
                                c -= self.cb[i]
                                self.board[tp[0] + c[0], tp[1] + c[1]] = st
                            flag = True
                            break
        if flag:
            return True
        else:
            return False
            
    def setStone(self): #石配置
        if pygame.mouse.get_pressed()[0]:
            pygame.time.wait(100) #処理が速すぎるので100ミリ秒止める
            pos = pygame.mouse.get_pos()
            if 200 <= pos[0] <= 760 and 150 <= pos[1] <= 710:
                self.setpos = [int((pos[0] - 200) / BOX), int((pos[1] - 150) / BOX)]
                if self.stonecolor:
                    if self.board[self.setpos[0], self.setpos[1]] == 0:
                        self.board[self.setpos[0], self.setpos[1]] = 1
                        if not self.checkBoardReversi():
                            self.board[self.setpos[0], self.setpos[1]] = 0
                        else:
                            return True
                else:
                    if self.board[self.setpos[0], self.setpos[1]] == 0:
                        self.board[self.setpos[0], self.setpos[1]] = 2
                        if not self.checkBoardReversi():
                            self.board[self.setpos[0], self.setpos[1]] = 0
                        else:
                            return True
        else:
            return False
        
    def endGame(self, st): #終了処理
        if not np.any(self.board == 0):
            return True
        if st:
            st = 1
        else:
            st = 2
        for x in range(0, 8):
            for y in range(0, 8):
                if self.board[x, y] == 0:
                    for i, tc in enumerate(self.cb):
                        c = tc.copy()
                        if 0 <= x + c[0] <= 7 and 0 <= y + c[1] <= 7:
                            nst = self.board[x + c[0], y + c[1]]
                            if nst != 0 and nst != st:
                                for j in range(1, 8):
                                    c += self.cb[i]
                                    if not 0 <= x + c[0] <= 7 or not 0 <= y + c[1] <= 7:
                                        break
                                    elif self.board[x + c[0], y + c[1]] == 0:
                                        break
                                    elif self.board[x + c[0], y + c[1]] == st:
                                        return False
                                
        return True
    
    def boolNot(self, a, b, c): #boolean反転
        return not(a), not(b), not(c)

#====================================作ってもらうやつここから
    
    def banDraw(self): #盤面描画
        font=pygame.font.Font(None,50)
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen,(0,100,0),(200,150,560,560)) #緑のやつ
        #勝率表示
        grades=font.render("win:"+str(1)+" lose:"+str(1)+" draw:"+str(1),True,(255,255,255))
        self.screen.blit(grades,[300,100])

        #縦線
        for xpos in range(200,761,70):
            pygame.draw.line(self.screen,0xFFFFFF,(xpos,710),(xpos,150))
        #横線
        for ypos in range(150,740,70):
            pygame.draw.line(self.screen,0xFFFFFF,(200,ypos),(760,ypos))

        if self.playerflag == True:
            text=font.render("Turn:prayer",True,(255,255,255))
            self.screen.blit(text,[800,300])
        else:
            text=font.render("Turn:AI",True,(255,255,255))
            self.screen.blit(text,[800,300])
        #白の数,黒の数を表示
        black_count=font.render("black:"+str(20),True,(255,255,255)) #変数を入れる
        self.screen.blit(black_count,[800,350])
        white_count=font.render("white:"+str(20),True,(255,255,255)) #変数を入れる
        self.screen.blit(white_count,[800,400])
        pass
    
    def stoneDraw(self): #石描画
        for x in range(0,8):
            for y in range(0,8):
                if self.board[x,y]==1:
                    pygame.draw.circle(self.screen,(255,255,255),(235+(70*x),185+(70*y)),30)
                elif self.board[x,y]==2:
                    pygame.draw.circle(self.screen,(0,0,0),(235+(70*x),185+(70*y)),30)
    
    def banDataDraw(self): #盤面情報描画 盤面描画とまとめた
        pass
    
    def resultDraw(self): #戦績描画　盤面描画とまとめた
        pass
    
    def recordDraw(self): #勝敗結果描画
        font=pygame.font.Font(None,150)
        #if
        lose=font.render("player:lose",True,(0,0,0))
        pygame.draw.rect(self.screen,(255,255,255),(180,350,600,140))
        self.screen.blit(lose,[200,358])
        #else:
        lose=font.render("AI:lose",True,(0,0,0))
        pygame.draw.rect(self.screen,(255,255,255),(230,350,500,110))
        self.screen.blit(lose,[300,358])
        pass
    
#====================================ここまで
    
if __name__ == "__main__":
    main()