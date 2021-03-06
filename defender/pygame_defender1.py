"""
  Pygame Defender first week
"""

import pygame
import copy
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)


 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (800, 500)
screenbottom = size[1]
screentop = 0
screen = pygame.display.set_mode(size)


# set up sprite lists
all_sprites_list = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
 
pygame.display.set_caption("Defender 1")

# load the sounds:
laser_sound = pygame.mixer.Sound("laser5.ogg")
explosion_sound = pygame.mixer.Sound("explosion.wav")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
ship = None

class Game():
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.over = True

    def update_screen(self, screen):
        if not self.over:
            message = "Score:{}".format(self.score)
            font = pygame.font.SysFont("Verdana", 30)
            text = font.render(message, False, BLACK)
            screen.blit(text, (10, 10))
            message = "Lives:{}".format(self.lives)
            text = font.render(message, False, BLACK)
            screen.blit(text, (600, 10))
            
        else:
            message = "Game Over!"
            message2 = "Press any key to play"
            font = pygame.font.SysFont("Verdana", 50)
            text = font.render(message, False, BLUE)
            screen.blit(text, (300, 200))
            text = font.render(message2, False, RED)
            screen.blit(text, (200, 300))

# our ship class
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("defender_ship.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 250
        self.updown = 0
        self.speed = 8
        self.exploding = False
        self.broken = False
        self.upgraded = 0

    def explode(self):
        ship.exploding = True
        self.image = pygame.image.load("exploding.png").convert()
        self.image.set_colorkey(WHITE)
        
    def upgrade(self):
        self.image = pygame.image.load("coolship.png").convert()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png").convert()
        self.image.set_colorkey(WHITE)
        self.image2 = self.image # store copy here
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.speed = 20        
        self.min_size = 4
        self.max_size = self.image.get_size()[0]
        

    def make_long(self, new_size):
        self.image = pygame.transform.scale(self.image2, (new_size, self.size[1]))
            
class Alien(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = size[0] - 50
        self.rect.y = y
        self.speedx = 5
        self.speedy = 0

    def switch_direction(self):
        move = random.randint(0,25)
        if move == 9:
            self.speedy = random.randint(-1,1) * 3

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("boomo.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.life = 0
        
 

game = Game()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    if game.score == 20 and ship.upgraded == 0:
        ship.upgraded = 1
        game.score = game.score - 20
        ship.upgrade()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and not game.over:
            # press space to fire
            if event.key == pygame.K_SPACE and not ship.exploding:
                if len(bullets) < 3:
                    laser_sound.play()
                    bullet = Bullet()
                    bullet.direction = 1
                    rect = copy.copy(ship.rect) # copy of the ship's position
                    rect[0] += ship.image.get_size()[0] # front of the ship
                    rect[1] += int(ship.image.get_size()[1]/2) # middle of the ship
                    bullet.rect = rect
                    bullet.make_long(bullet.min_size)
                    all_sprites_list.add(bullet)
                    bullets.add(bullet)
                                
            # if the up or down key is pressed, set the direction of movement
            if event.key == pygame.K_UP and not ship.exploding:
                ship.updown = -1
            if event.key == pygame.K_DOWN and not ship.exploding:
                ship.updown = 1
        if event.type == pygame.KEYDOWN and game.over:          
            ship = Ship()
            game = Game()
            game.over = False
            all_sprites_list.empty()
            all_sprites_list.add(ship)
        if event.type == pygame.KEYUP:
            # when you stop pressing, stop moving!
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                ship.updown = 0
                

 
    # --- Game logic should go here
    if not game.over:
        ship.rect.y += (ship.speed * ship.updown)
        if ship.rect.y > screenbottom:
            ship.rect.y = screentop
        if ship.rect.y < screentop:
            ship.rect.y = screenbottom
        for bullet in bullets:
            if bullet.image.get_size()[0]<bullet.max_size:
                bullet.make_long(bullet.image.get_size()[0] + bullet.speed)
            else: bullet.rect.x += bullet.speed
            if bullet.rect.x > size[0]:
                bullets.remove(bullet)
                all_sprites_list.remove(bullet)
           
    # Let's add an alien if we need one
    add_alien = random.randint(0,10)
    if add_alien == 9 and len(aliens) < 4 and ((ship is None) or not ship.exploding):
        alien_y = random.randint(0,size[1])
        alien = Alien(alien_y)
        aliens.add(alien)
        all_sprites_list.add(alien)

    # move the aliens
    for alien in aliens:
        alien.rect.x -= alien.speedx
        alien.rect.y += alien.speedy
        if alien.rect.x < 0:
            aliens.remove(alien)
            all_sprites_list.remove(alien)

        if alien.rect.y < 0:
            alien.rect.y = size[1]
        elif alien.rect.y > size[1]:
            alien.rect.y = 0
            
        alien.switch_direction()

    if not game.over:
        hit_list = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for hit in hit_list:
            explosion_sound.play()
            game.score += 1
            # free ship every 100 points:
            if game.score % 10 == 0:
                game.lives += 1
            explosion = Explosion(hit.rect.x, hit.rect.y)
            all_sprites_list.add(explosion)
            explosions.add(explosion)

        hit = pygame.sprite.spritecollideany(ship,aliens)
        if hit and not ship.exploding:
            ship.explode()
            game.lives -= 1
            if game.lives == 0:
                game.over = True
            
        for explosion in explosions:
            explosion.life += 1
            if explosion.life > 20:
                explosion.kill()

        if ship.exploding and len(aliens) == 0:
            ship.kill()
            ship = Ship()
            all_sprites_list.add(ship)
        
 
    # --- Screen-clearing code goes here
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    all_sprites_list.draw(screen)
    game.update_screen(screen)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
