import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        self.aliens = pygame.sprite.Group() #创建一个用于存储外星人的编组

        self._create_fleet() #创建外星人群

        #设置背景颜色
        self.bg_color = (230,230,230) #RGB颜色浅灰色
    
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self.ship.update()
            self.bullets.update()
            self._check_events()
            self._update_bullets()
            self._update_aliens()

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
        if len(self.bullets) < self.settings.bullet_allowed: #如果屏幕上子弹数量超过允许的数量
            new_bullet = Bullet(self) #创建一个子弹实例
            self.bullets.add(new_bullet) #将子弹加入到编组中

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        #更新子弹的位置
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy(): #遍历编组中的每颗子弹的副本
            if bullet.rect.bottom <= 0: #如果子弹的底部小于等于0
                self.bullets.remove(bullet) #将子弹从编组中删除

    def _update_screen(self):
        #每次循环时都重绘屏幕,并切换到新屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme() #在指定位置绘制飞船
        for bullet in self.bullets.sprites(): #遍历编组中的每颗子弹
            bullet.draw_bullet() #在屏幕上绘制子弹
        self.aliens.draw(self.screen) #在屏幕上绘制外星人
        #让最近绘制的屏幕可见
        pygame.display.flip()

    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人，并计算一行可容纳多少个外星人
        #外星人间距为外星人宽度
        alien = Alien(self) 
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) #屏幕宽度-2个外星人宽度
        number_aliens_x = available_space_x // (2 * alien_width) #每个外星人占2个外星人宽度

        #计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien.rect.height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) #加入编组

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
    
    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 #改变方向

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
