import pygame
import os
import math
from settings import WIN_WIDTH, WIN_HEIGHT

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        x1, y1 = enemy.get_pos()  # 取得enemy位置
        distance = math.sqrt((x1 - self.center[0])**2 + (y1 - self.center[1])**2)  # enemy和tower的距離
        if distance <= self.radius:  # 如果距離小於半徑 -> 敵人在攻擊範圍內 => 回傳True
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 100  #透明度
        pygame.draw.circle(transparent_surface, (192, 192, 192, transparency), self.center, self.radius)  # surface, color, center, radius
        win.blit(transparent_surface, (0, 0))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        if self.cd_count < self.cd_max_count:  #冷卻時間達 60 frame則歸零
            self.cd_count += 1
            return False                       
        else:
            self.cd_count = 0
            return True                        #冷卻完成回傳 True
            

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        if self.is_cool_down():  # 冷卻完成 -> is_cool_down()回傳True
            for enemy in enemy_group.get():  # enemy_group.get()：Get the enemy list
                if self.range_circle.collide(enemy):  # enemy在攻擊範圍 -> Circle.collide()回傳True
                    enemy.get_hurt(self.damage)  # enemy扣血
                    return






    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # 設定tower選取範圍
        if self.rect.x <= x <= self.rect.topright[0] and self.rect.y <= y <= self.rect.bottomleft[1]:
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

