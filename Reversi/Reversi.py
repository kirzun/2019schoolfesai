# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np

SCR_RECT = Rect(0, 0, 1024, 768) #画面サイズ
BOX = 24

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
    
    def update(self):
        if self.playerflag:
            self.player()
        else:
            self.ai()

        self.checkBoard()
    
    def draw(self, screen):
        self.screen = screen
        self.banDraw()
        self.stoneDraw()
        self.banDataDraw()
        self.resultDraw()
        self.recordDraw()
    
    def checkBoard(self): #石反転チェック
        #置かれた場所から8方向を見て反転する石の座標を渡す
        
        """
        if 石反転できるなら
            self.reversi()
        """
    
    def reversi(self): #石反転
        pass
    
    def player(self): #プレイヤー処理
        self.setStone()
    
    def ai(self): #AI処理
        """
        AIに盤面を渡して結果を受け取る
        """
        self.setStone()
    
    def setStone(self): #石配置
        pass
    
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
        
def sceneMgr():
    pass
    
if __name__ == "__main__":
    main()