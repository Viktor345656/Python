from pygame import *
 
win_width = 700
win_height = 500
n_speed_x = 4
n_speed_y = 4
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')

 
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, size_x, size_y, player_x, player_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
 
    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,
                                      p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                     p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)
 
 
w1 = GameSprite('wall.png', 50, 300, 410, 92)
w2 = GameSprite('wall.png', 50, 280, 275, 220)
w3 = GameSprite('wall.png', 50, 400, 140, 0)
w4 = GameSprite('wall.png', 50, 280, 545, 220)
w5 = GameSprite('wall.png', 280, 50, 180, 85)
w6 = GameSprite('wall.png', 50, 280, 0, 220)
wall_1 = GameSprite('wall.png', 80, 180, 180, 250)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
 
packman = Player('people.png', 0, 0, 80, 80, 0, 0)
# ghost_x = 0
enemy = GameSprite('minotaur.png', 80, 80, 545, 80)
treasure = GameSprite('exit.png', 70, 70, 615, 430)
power = GameSprite('hidden.png', 60, 60, 200, 10)
back = (119, 210, 223)
 
ghost_x = 0
power_active = False
 
run = True
while run:
    time.delay(50)
    window.fill((44, 99, 1))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
 
    if not power_active:
        power.reset()
    packman.reset()
    enemy.reset()
    treasure.reset()
    packman.update()
 
    barriers.draw(window)
 
    if sprite.collide_rect(packman, enemy) and not power_active:
        img = image.load('background_game_over.jpg')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        run = False
 
    if sprite.collide_rect(packman, treasure):
        img_lose = image.load('background3.png')
        window.blit(transform.scale(img_lose, (700, 500)), (90, 0))
        run = False
 
    if sprite.collide_rect(packman, power):
        power_active = True
    display.update()
    w1.reset()
    w2.reset()
    w3.reset()
    w4.reset()
    w5.reset()
    w6.reset()
    
    enemy.rect.x += n_speed_x
    enemy.rect.y += n_speed_y
    if sprite.collide_rect(enemy, w1) or sprite.collide_rect(enemy, w2) or sprite.collide_rect(enemy, w4) or sprite.collide_rect(enemy, w5) or enemy.rect.x > win_width - 80:
        n_speed_x *= -1
    if enemy.rect.y > win_height - 80 or enemy.rect.y < 0:
        n_speed_y *= -1