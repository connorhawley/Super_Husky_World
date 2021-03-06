from constants import *
from Ball import Ball
import time

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        #call parent constructor
        super().__init__()
        #create player sprite images

        self.left_images = self.create_sprite_sheet((72,48), 'data/sprites/husky_sprites.png', (0,0))
        self.right_images = self.create_sprite_sheet((72,48), 'data/sprites/husky_sprites.png', (0,48))
        self.jump_left_images = ['data/sprites/jumping/jumpingleft.png', 'data/sprites/jumping/midairleft.png',
                                 'data/sprites/jumping/landingleft.png']
        self.jump_right_images =['data/sprites/jumping/jumpingright.png', 'data/sprites/jumping/midairright.png',
                                 'data/sprites/jumping/landingright.png']
        self.right_images.reverse()
        self.rect = self.right_images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = self.right_images[2].convert_alpha()
        self.onGround = False
        self.jumping = False
        self.walkingLeft = False
        self.walkingRight = True
        self.dx = 0
        self.dy = 0
        self.image_framerate = 7
        self.image_count = len(self.left_images)
        self.ball_list = []
        self.last_time = pygame.time.get_ticks() #get time in milliseconds


    def update(self, platforms):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            if self.onGround:
                self.dy -= JUMP_HEIGHT
                self.onGround = False
                self.jumping = True
#                pygame.mixer.music.load("data/Audio/Jump.wav")
#                pygame.mixer.music.play(1, 0)
            if key[pygame.K_a]:
                self.move_left()
            if key[pygame.K_d]:
                self.move_right()

        if key[pygame.K_s]:
            pass

        if key[pygame.K_a]:
            self.move_left()

        if key[pygame.K_d]:
            self.move_right()

        if key[pygame.K_SPACE]:
            if self.walkingLeft:
                self.shoot('left')
                #pygame.mixer.music.load("data/Audio/Basketball Dribbling Sound EffectHD.wav")
                #pygame.mixer.music.play(1, 0)
            if self.walkingRight:
                self.shoot('right')
                #pygame.mixer.music.load("data/Audio/Basketball Dribbling Sound EffectHD.wav")
                #pygame.mixer.music.play(1, 0)

        if self.walkingLeft:  # if walking left, then animate the player sprite
            if key[pygame.K_a]:
                self.image = self.left_images[int(
                    time.time() * self.image_framerate % self.image_count)].convert_alpha()  # limits animation framerate
            if not key[pygame.K_a]:
                self.image = self.left_images[2].convert_alpha()
            if self.jumping:
                if self.dy > 0.5:
                    self.image = pygame.image.load(self.jump_left_images[2]).convert_alpha()
                elif -5 <= self.dy <= 5:
                    self.image = pygame.image.load(self.jump_left_images[1]).convert_alpha()
                else:
                    self.image = pygame.image.load(self.jump_left_images[0]).convert_alpha()


        if self.walkingRight:  # if walking right, then animate the player sprite
            if key[pygame.K_d]:
                self.image = self.right_images[int(
                    time.time() * self.image_framerate % self.image_count)].convert_alpha()  # limits animation framerate
            if not key[pygame.K_d]:  # if not pressing key then return to standing position sprite
                self.image = self.right_images[2].convert_alpha()
            if self.jumping:
                if self.dy > 0.5:
                    self.image = pygame.image.load(self.jump_right_images[2]).convert_alpha()
                elif -5 <= self.dy <= 5:
                    self.image = pygame.image.load(self.jump_right_images[1]).convert_alpha()
                else:
                    self.image = pygame.image.load(self.jump_right_images[0]).convert_alpha()

        if self.onGround == False:   #if not on the ground then apply gravity
            self.dy += GRAVITY

        if not(key[pygame.K_a] or key[pygame.K_d]): #if not moving left or right, don't change x coordinate
            self.dx = 0

        self.rect.left += self.dx
        #collision for x axis
        self.collide(self.dx, 0, platforms)
        self.rect.top += self.dy
        self.onGround = False
        #collision for y axis
        self.collide(0, self.dy, platforms)



    def shoot(self, direction):
        cooldown = SHOOT_COOLDOWN  #shoot cooldown in milliseconds (how long before you can shoot again)
        current_time = pygame.time.get_ticks()#get current time in milliseconds
        if current_time - self.last_time > cooldown: #if time passed is greater than cooldown
            self.last_time = current_time            #then set last time to current time and allow new ball to be shot
            ball = Ball(direction)                    #create new ball that is going right
            self.ball_list.add(ball)                #add ball to ball list (necessary in order to check collision and remove it)
            if direction == 'left':
                ball.rect.x = self.rect.left - 30       #spawn the ball on the left of the player if facing left
            else:
                ball.rect.x = self.rect.right           #spawn the ball at the top right of the player
            ball.rect.y = self.rect.top

    def move_right(self):
        self.dx = PLAYER_SPEED
        self.walkingLeft = False
        self.walkingRight = True

    def move_left(self):
        self.dx = -PLAYER_SPEED
        self.walkingRight = False
        self.walkingLeft = True

    def collide(self, dx, dy, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if dx > 0:
                    #colliding on the right, set right coordinate to left coordinate of platform
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right
                    #colliding on the left, set left coordinate to left coordinate of platform
                if dy > 0:
                    #you are on the ground
                    self.rect.bottom = platform.rect.top  #set bottom coordinate to top coordinate of platform
                    self.onGround = True
                    self.jumping = False
                    self.dy = 0
                if dy < 0:
                    self.rect.top = platform.rect.bottom  #set top coordinate to bottom coordinate of platform
                    self.dy += 2

    def noclip(self):
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_w]:
            self.dy = -PLAYER_SPEED*2
            self.rect.top += self.dy
        if keypressed[pygame.K_s]:
            self.dy = PLAYER_SPEED*2
            self.rect.top += self.dy
        if keypressed[pygame.K_a]:
            self.dx = -PLAYER_SPEED*2
            self.rect.left += self.dx
        if keypressed[pygame.K_d]:
            self.dx = PLAYER_SPEED*2
            self.rect.left += self.dx


    def create_sprite_sheet(self, size, file, initial_position):
        #sprites must be of the same size
        (sprite_width, sprite_height) = size  # sprite size
        (sprite_rect_x, sprite_rect_y) = initial_position  # where to find first sprite on sheet
        spritesheet = pygame.image.load(file).convert_alpha()  # Load the sheet
        spritesheet_rect = spritesheet.get_rect()
        sprite_list = [] #list that will contain the sprites
        for i in range(0, spritesheet_rect.height - sprite_height, sprite_height):  #loop through the rows of sprites
            for j in range(0, spritesheet_rect.width, sprite_width):                #loop through the colums of sprites
                spritesheet.set_clip(pygame.Rect(sprite_rect_x, sprite_rect_y, sprite_width, sprite_height)) #sets clip area for sprite
                sprite = spritesheet.subsurface(spritesheet.get_clip()) #clips out the sprite of specified size
                sprite_list.append(sprite) #add clipped sprite to sprite list
                sprite_rect_x += sprite_width #move onto next sprite
            sprite_rect_y += sprite_height
            sprite_rect_x = 0 #go back to the beginning of the row
        return sprite_list  #return the list of all of the sprites
