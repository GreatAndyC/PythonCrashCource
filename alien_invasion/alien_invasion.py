import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()  #从同文件夹下的settings.py导入Settings类
        
        self.screen = pygame.display.set_mode(          #指定窗口大小
            (self.settings.screen_width, self.settings.screen_height))
    
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #全屏模式 
        # self.settings.screen_width = self.screen.get_rect().width  #更新宽度
        # self.settings.screen_height = self.screen.get_rect().height #更新高度
        
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self) #创建飞船实例
        self.bullets = pygame.sprite.Group() #创建一个用于存储子弹的编组

        #设置背景颜色
        self.bg_color = (230,230,230) #RGB颜色浅灰色
    
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self.ship.update()
            self.bullets.update()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:      #按下 持续向右移动，配合ship类里面的标志
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:       #松开 停止移动 注意缩进 不然持续移动
                self._check_keyup_events(event)
            
    
    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True       #按下右键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  #按下Q键退出
            sys.exit()
        elif event.key == pygame.K_SPACE: #按下空格键发射子弹
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        new_bullet = Bullet(self) #创建一个子弹实例
        self.bullets.add(new_bullet) #将子弹加入到编组中

    def _update_screen(self):
        #每次循环时都重绘屏幕,并切换到新屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme() #在指定位置绘制飞船
        for bullet in self.bullets.sprites(): #遍历编组中的每颗子弹
            bullet.draw_bullet() #在屏幕上绘制子弹
        #让最近绘制的屏幕可见
        pygame.display.flip()

    

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
