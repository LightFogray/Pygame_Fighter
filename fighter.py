import pygame
import random
from os import path

WIDTH,HEIGHT,SPEED = 600,700,5

MISSILE_LIFETIME = 10000#10000毫秒
MISSILE_INTERVAL = 2000
#设定一个常量表示每隔多少毫秒生成一个敌人
NEW_ENEMY_GENERATE_INTERVAL = 500
#常用颜色
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
PLAYER_HP = 100
YELLOW = (255,255,0)
#。。。（）表示一种方法
#继承
class Player(pygame.sprite.Sprite):#大写的S表示为类
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((45,45))#精灵图像设置为surface，默认为矩形
        self.image = player_img#图片表示
        #self.image.fill((45,50,100))#在self.image里设置填充颜色为（0,255,0）
        #调整翻转
        self.image = pygame.transform.flip(self.image,False,False)

        #调整图片大小
        self.image = pygame.transform.scale(self.image,(58,50))

        #去掉黑色不透明的部分
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()#获取精灵的位置信息，存在self.rect里，确保以后对位置进行操作时，直接对get_rect方法进行改变
#初始化精灵的位置
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT
        #定义玩家生命及血量
        self.hp = PLAYER_HP
        self.live = 3
        self.score = 0
        self.hidden = False
        self.hide_time = 0#隐藏时间
        #导弹时间初始化
        self.is_missile_firing = False
        self.start_missile_time = 0
        self.last_missile_time = 0


    def update(self):
#用键盘控制上下左右的移动

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
           self.rect.x -= SPEED
        if key_state[pygame.K_RIGHT]:
           self.rect.x += SPEED
        if key_state[pygame.K_UP]:
           self.rect.y -= SPEED
        if key_state[pygame.K_DOWN]:
           self.rect.y += SPEED
        #判断是否出边界
        if self.rect.right > WIDTH:
           self.rect.right = WIDTH
        if self.rect.left < 0:
           self.rect.left = 0
        #if self.rect.top < 0:
           #self.rect.top = 0省略此限制可让玩家实现隐藏效果
        if self.rect.bottom > HEIGHT:
           self.rect.bottom = HEIGHT

        now = pygame.time.get_ticks()
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.bottom = HEIGHT
            self.rect.centerx = WIDTH/2
#若功能存在，则执行
        if self.is_missile_firing:
            if now - self.start_missile_time <= MISSILE_LIFETIME:
                if now - self.last_missile_time >= MISSILE_INTERVAL:
                    missile = Missile(self.rect.center)
                    missiles.add(missile)
                    self.last_missile_time = now
            else:
                self.is_missile_firing = False


#玩家进行射击操作
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        bullets.add(bullet)
        shoot_sound.play()

#隐藏玩家，让玩家损失一条命之后隐藏一小会儿
    def hide(self):
        self.hidden = True
        self.rect.y = -100#隐藏
        self.hide_time = pygame.time.get_ticks()
#导弹功能
    def fire_missile(self):
        self.is_missile_firing = True
        self.start_missile_time = pygame.time.get_ticks()

#定义一个敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            img_width = random.randint(30,100)#使陨石随机大小
            img_height = int(img_width*72/70)#使构图成比例
            #导入敌人图片表示
            self.image = enemy_img
            #调整敌人大小
            self.image = pygame.transform.scale(self.image,(img_width,img_height))

            #去掉不透明部分
            self.image.set_colorkey(BLACK)
            #self.image = pygame.Surface((30,30))
            #self.image.fill((0,255,0))
            #旋转需要保留一份原始图像
            self.image_origin = self.image.copy()#副本，相当于c中的传值
            self.rect = self.image.get_rect()
            #将碰撞检测边缘设为圆形
            self.radius = 30
            #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius,5)
            self.rect.x = random.randint(0,WIDTH - self.rect.w)

            self.rect.bottom = 0#使所有流星从最上方下落

            self.vx = random.randint(-2,2)#随机速度
            self.vy = random.randint(2,2)
            #旋转
            self.last_time = 0
            self.rotate_speed = random.randint(-5,5)

            self.rotate_angle = 0#旋转角
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

#若敌人碰撞到左右边缘，则反弹，只有被打中或从下面才可消失

        if self.rect.left <= 0:
            self.vx = -self.vx
        if self.rect.right > WIDTH:
            self.vx = -self.vx
        self.rotate()
    #敌人旋转
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 30:
            #旋转的效果
            self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
            self.image = pygame.transform.rotate(self.image_origin,self.rotate_angle)
            #分别获取新的和旧的两个尺寸中心点，再使得两个中心点重合
            #即可以使图片旋转适当
            old_center = self.rect.center#旧
            self.rect = self.image.get_rect()#获取新的
            #使两点重合
            self.rect.center = old_center
#子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img

        self.image = pygame.transform.scale(self.image,(10,30))

        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((10,20))
        #self.image.fill((100,71,56))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


    def update(self):
        self.rect.y -= 8
#导弹效果
class Missile(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img

        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((10,20))
        #self.image.fill((100,71,56))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):

        self.rect.y -= 4

#爆炸效果
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        #self.image = explosion_animation[0]
        self.image = pygame.transform.scale(explosion_animation[0],(75,75))#调整图片大小#此处仅仅更新了第一张
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center#使爆炸出现在一定位置
        self.frame = 0
        self.last_time = pygame.time.get_ticks()
        explosion_sound.play()

    #更新
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 40:#40微秒，控制每一帧的出现的时间
            if self.frame < len(explosion_animation):
                self.image = pygame.transform.scale(explosion_animation[self.frame],(75,75))#此处循环改变缩放值，确保九张都更新
                self.image.set_colorkey(BLACK)
                self.frame += 1
                self.last_time = now#每一次的更新
            else:
                self.kill()#播放完之后杀死自己，保证最后一帧图片不会保留在页面中


class PowerUp(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        random_num = random.random()
        #给每种补给品设置不同的概率得到
        if random_num >= 0 and random_num < 0.5:
            self.type = 'add_hp'
        elif random_num >= 0.5 and random_num < 0.8:
            self.type = 'add_missile'
        else:
            self.type = 'add_life'
        self.image = powerup_imgs[self.type]

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #self.image = pygame.Surface((10,20))
        #self.image.fill((100,71,56))
        self.rect.center = center

    def update(self):
        self.vx = random.randint(0,2)
        self.vy = random.randint(0,3)
        self.rect.y += self.vy
        self.rect.x += self.vx
#UI函数
color_change = GREEN#为以后改变颜色定义

#封装
def draw_text(text,surface,color,x,y,size):
    #添加字体
    font_name = pygame.font.match_font('arial')#字体
    font = pygame.font.Font(font_name,size)#大小
    #字体渲染
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

def draw_ui():
    #调整血槽的位置
    pygame.draw.rect(screen,color_change,(WIDTH-120,HEIGHT-27,player.hp,15))#血量
    pygame.draw.rect(screen,WHITE,(WIDTH-120,HEIGHT-27,100,15),2)#血槽

    draw_text(str("Current score:{}".format(player.score)),screen,WHITE,WIDTH/2,10,20)
    img_rect = player_img_small.get_rect()
    img_rect.right = WIDTH - 10
    img_rect.y = 10

    for i in range(player.live):
        screen.blit(player_img_small,img_rect)
        img_rect.right = img_rect.x - 10
#菜单
def show_menu():
    #定义全局变量
    global game_state,screen
    #这两个变量在此函数内部进行了改变，所以需要定义全局
    #其余变量杂此函数仅仅被引用，并未改变
    screen.blit(background_img,background_rect)
    draw_text('Welcome to',screen,WHITE,WIDTH/2,50,50)
    draw_text('XiaoQian fighter',screen,RED,WIDTH/2,100,60)
    draw_text('VS',screen,WHITE,WIDTH/2,150,80)
    draw_text('aliens',screen,RED,WIDTH/2,200,60)
    draw_text('Press Space key to start',screen,YELLOW,WIDTH/2,450,40)
    draw_text('Press Esc key to quit',screen,YELLOW,WIDTH/2,500,40)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                game_state = True
    pygame.display.flip()

#添加音效需要wav格式和ogg格式
#游戏初始化
pygame.mixer.pre_init(44100,-16,2,2048)#添加此句使得音效同步不会延时播放
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))#screeen也相当于一个surface的类型
        #可以在surface上画画，加载图片，填充颜色等
        #画布可进行叠加
        #Surface.blit（要画的surface，（x坐标，Y坐标））
        #blit：位块传送，位块传输
pygame.display.set_caption("小钱战机大战外星人")

clock = pygame.time.Clock()
#导入图片模块----放在游戏初始化之后
img_dir = path.join(path.dirname(__file__),'img')#当前程序文件所在目录与img合并为一个路径
#用path.join来表示：因各个系统表示路径不一样

background_dir = path.join(img_dir,'background.png')
background_img = pygame.image.load(background_dir).convert()
background_rect = background_img.get_rect()
#剩余角色导入图片
player_dir = path.join(img_dir,'player.png')
player_img = pygame.image.load(player_dir).convert()
#以缩小的玩家图案表示生命条数
player_img_small = pygame.transform.scale(player_img,(26,20))
player_img_small.set_colorkey(BLACK)
enemy_dir = path.join(img_dir,'enemy.png')
enemy_img = pygame.image.load(enemy_dir).convert()
bullet_dir = path.join(img_dir,'bullet.png')
bullet_img = pygame.image.load(bullet_dir).convert()
missile_dir = path.join(img_dir,'missile.png')
missile_img = pygame.image.load(missile_dir).convert()

#爆炸效果图片
explosion_animation = []#列表
for i in range(9):
    explosion_dir = path.join(img_dir,'regularExplosion0{}.png'.format(i))
    explosion_img = pygame.image.load(explosion_dir).convert()
    #列表添加载入的图片
    explosion_animation.append(explosion_img)
    #字典表示药物补给
    powerup_imgs = {}
    powerup_add_hp_dir = path.join(img_dir,'hp.png')
    powerup_imgs['add_hp'] = pygame.image.load(powerup_add_hp_dir).convert()
    powerup_add_life_dir = path.join(img_dir,'life.png')
    powerup_imgs['add_life'] = pygame.image.load(powerup_add_life_dir).convert()
    powerup_add_missile_dir = path.join(img_dir,'missileadd.png')
    powerup_imgs['add_missile'] = pygame.image.load(powerup_add_missile_dir).convert()

#导入声音文件

sound_dir = path.join(path.dirname(__file__),'sound')
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'shoot.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir,'explosion.wav'))
pygame.mixer.music.load(path.join(sound_dir,'bgm.wav'))

player = Player()#实例化玩家
#精灵编组
enemys = pygame.sprite.Group()#敌人小组
explosions = pygame.sprite.Group()#爆炸元素小组
#添加补给品的精灵小组
powerups = pygame.sprite.Group()
for i in range(6):
    enemy = Enemy()
    enemys.add(enemy)

bullets = pygame.sprite.Group()
missiles = pygame.sprite.Group()

last_enemy_generate_time = 0

game_over = False
#判断玩家当前处于什么场景
game_state = 0

#调节音量
pygame.mixer.music.set_volume(2)
#背景音乐循环播放：(loops = -1)loops代表循环次数，-1表示死循环
pygame.mixer.music.play(loops = -1)
#游戏的主循环
while not game_over:
    clock.tick(60)

    if game_state == 0:
        show_menu()
    elif game_state == 1:
        now = pygame.time.get_ticks()
        if now - last_enemy_generate_time > NEW_ENEMY_GENERATE_INTERVAL:
            enemy = Enemy()
            enemys.add(enemy)
            last_enemy_generate_time = now

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                #game_over = True
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_SPACE:
                    #bullet = Bullet(player.rect.centerx,player.rect.centery)
                    #bullets.add(bullet)
                        player.shoot()
        screen.fill(BLACK)
        screen.blit(background_img,background_rect)

        player.update()
        enemys.update()
        bullets.update()
        explosions.update()
        powerups.update()
        missiles.update()
            #碰撞
            #三个参数分别为精灵1，精灵2，发生碰撞后是否消失（true or false）
            #调整碰撞的缩放比例---pygame.sprite.collide_rect_ratio(比例)
        hits = pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_rect_ratio(0.8))#result显示为一个列表
        for hit in hits:
            player.hp -= hit.radius/2#不同半径大小的陨石打的血不一样，按比例来
            if player.hp < PLAYER_HP/4:
                color_change = RED#血量少于一定值时，血条变红
            if player.hp <= 0:
                player.live -= 1
                player.hp = 100
                player.hide()
                color_change = GREEN
                if player.hp < PLAYER_HP/4:
                    color_change = RED
            if player.live < 0:#玩家三条命都没了之后结束
        #if hits:#可以理解为：if len(hits)>0:
                game_over = True
        #两个精灵群组之间的碰撞
        #碰到之后，敌人与子弹都消失
        hits = pygame.sprite.groupcollide(enemys,bullets,True,True)
        #当消失一个敌人的时候，会再次出现一个新的敌人
        for hit in hits:
            enemy = Enemy()
            enemys.add(enemy)
            #检测碰撞后爆炸小组的出现
            explosion = Explosion(hit.rect.center)
            explosions.add(explosion)
            #玩家得分
            player.score += hit.radius
            #补给品
            if random.random() > 0.9:#随机生成0——1的数90%
                powerup = PowerUp(hit.rect.center)#在碰撞的中点生成补给
                powerups.add(powerup)
    #导弹碰到敌人会消失
        hits = pygame.sprite.groupcollide(enemys,missiles,True,True)
        for hit in hits:
            enemy = Enemy()
            enemys.add(enemy)
            #检测碰撞后爆炸小组的出现
            explosion = Explosion(hit.rect.center)
            explosions.add(explosion)
            #玩家得分
            player.score += hit.radius
            #补给品
            if random.random() > 0.9:#随机生成0——1的数90%
                powerup = PowerUp(hit.rect.center)#在碰撞的中点生成补给
                powerups.add(powerup)
        hits = pygame.sprite.spritecollide(player,powerups,True)
        for hit in hits:
            if hit.type == 'add_hp':
                player.hp += 25
                if player.hp > 100:
                    player.hp = 100#生命上限值
            elif hit.type == 'add_life':
                player.live += 1
                if player.live > 3:
                    player.live = 3#生命条数上限值
            else:
                #pass
                player.fire_missile()
                #当玩家碰到导弹补给的时候调用此函数




        screen.blit(player.image,player.rect)
        enemys.draw(screen)
        #enemy.update()
        #screen.blit(enemy.image,(enemy.rect.x,enemy.rect.y))
        bullets.draw(screen)
        explosions.draw(screen)
        powerups.draw(screen)
        missiles.draw(screen)
        #新增一个函数专门画UI

        draw_ui()
        pygame.display.flip()
#玩家最终得分：
print("您的最终得分为：{}".format(player.score))
#待添加功能：吃补给后的音效
#尝试改变主页背景图片
#其余图片仍有不完善
