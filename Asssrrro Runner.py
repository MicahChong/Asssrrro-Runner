import pygame
import math
import random


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    clock = pygame.time.Clock() 
    fs = False # CHANGE THIS TO TRUE FOR FULL SCREEN!
    if fs == True:
        screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Asssrrro Runner')
    game_over = False
    MainMenu = True
    
    # Img Assets
    mainsprite = pygame.image.load('imgs/sprite.png')
    background = pygame.image.load('imgs/background.png')
    mainasteroid = pygame.image.load('imgs/asteroid.png')
    damage = pygame.image.load('imgs/damage.png')
    resetbutton = pygame.image.load('imgs/resetbutton.png')
    startbutton = pygame.image.load('imgs/startbutton.png')
    exitbutton = pygame.image.load('imgs/exitbutton.png')
    gameoverbg = pygame.image.load('imgs/gameoverbg.jpg')
    logo = pygame.image.load('imgs/logo.png')
    coin_image = pygame.image.load('imgs/coin.png')
    
    #Sounds Assests
    pygame.mixer.music.load('sounds/Music.wav')
    pygame.mixer.music.set_volume(0.5)
    damagefx = pygame.mixer.Sound('sounds/DamageSound.wav')
    damagefx.set_volume(0.06)
    buttonfx = pygame.mixer.Sound('sounds/buttonclick.wav')
    buttonfx.set_volume(0.6)
    coinfx = pygame.mixer.Sound('sounds/coin.wav')
    coinfx.set_volume(0.6)
    
    #Health Bar Class
    class HealthBar():
        def __init__(self, x, y, w, h, max_hp):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "grey", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "blue", (self.x, self.y, self.w * ratio, self.h))

    #Button Class
    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False
       
        def draw(self):
            action = False
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            screen.blit(self.image, self.rect)
            return action

    #Damaged Function
    def damaged():
        damagefx.play()
        health_bar.hp = health_bar.hp - 10
        
    #GameOver
    def gameover():
        screen.blit(gameoverbg2, (0,0))
        if exit_button.draw():
         running = False
        damagefx.set_volume(0)
        pygame.mixer.music.fadeout(4000)
        pygame.mouse.set_visible(True)
        screen.blit(score_text, (575, 425))
        if restart_button.draw():
            buttonfx.play()
            main()
            
    #Buttons Transform
    resetbutton2 = pygame.transform.scale_by(resetbutton, (0.2))
    startbutton2 = pygame.transform.scale_by(startbutton, (0.15))
    exitbutton2 = pygame.transform.scale_by(exitbutton, (0.06))
    
    #Coin Transform
    coin_image = pygame.transform.scale_by(coin_image, 0.05)

    #Damage Transform
    damage2 = pygame.transform.scale(damage, (1280,720))

    #Sprite Transform
    sprite2 = pygame.transform.scale_by(mainsprite, (0.08))
    sprite2_rect = sprite2.get_rect()

    #Game Over BG Transform
    gameoverbg2 = pygame.transform.scale(gameoverbg, (1280, 720))

    # Background Transform
    background2 = pygame.transform.scale(background, (1280, 720))

    # Asteroid Transform
    asteroid2 = pygame.transform.scale_by(mainasteroid, (0.05))

    num_coins = 5  #Number of coins to spawn
    coins = []
    score = 0
    # Spawn Location for Coins
    def spawn_coin():
        x = random.randint(0, 1280 - coin_image.get_width())
        y = random.randint(0, 600 - coin_image.get_height())
        return coin_image.get_rect(topleft=(x, y))
    for _ in range(num_coins):
        coin_rect = spawn_coin()
        coins.append(coin_rect)
    
    # Generate Multiple Asteroids
    num_asteroids = 10  # Number of asteroids to spawn
    asteroids = []

    # Spawn Location
    def spawn_asteroid():
        # Randomly choose to spawn asteroid from any side of the screen
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, 1280)
            y = -50
        elif side == 'bottom':
            x = random.randint(0, 1280)
            y = 720 + 50
        elif side == 'left':
            x = -50
            y = random.randint(0, 720)
        elif side == 'right':
            x = 1280 + 50
            y = random.randint(0, 720)
        speed_x = random.uniform(-3, 3)
        speed_y = random.uniform(-3, 3)
        asteroid_rect = asteroid2.get_rect(topleft=(x, y))
        return asteroid_rect, speed_x, speed_y

    # Makes Asteroids
    for i in range(num_asteroids):
        asteroid_rect, speed_x, speed_y = spawn_asteroid()
        asteroids.append([asteroid_rect, speed_x, speed_y])

    speed_multiplier = 1.0
    speed_increment = 0.0005  # How Fast Speed Increases Over Time
    health_bar = HealthBar(450, 10, 300, 10, 100)
    restart_button = Button(570, 450, resetbutton2)
    exit_button = Button(10, 10, exitbutton2)
    start_button = Button(525, 530, startbutton2)
    font = pygame.font.Font(None, 36)
    
    # Main Game Loop
    running = True
    while running:
        screen.blit(background2, (random.randint(0,1),random.randint(0,1)))
        # Position for Mouse
        pos = pygame.mouse.get_pos()
        if exit_button.draw():
             running = False
        if MainMenu == True:
         screen.blit(logo, (random.randint(360,362),random.randint(100,102)))
         if start_button.draw():
             pygame.mixer.music.play(-1,0.0, 5000)
             buttonfx.play()
             MainMenu = False
        else:
                pygame.mouse.set_visible(False)
                # Sprite Angle Calculation
                dx = pos[0] - sprite2_rect.centerx
                dy = pos[1] - sprite2_rect.centery
                angle = math.degrees(math.atan2(-dx, -dy))
                
                # Sprite Rotation
                if pos != sprite2_rect.center:
                    rotated_sprite2 = pygame.transform.rotate(sprite2, angle)
                    rotated_rect = rotated_sprite2.get_rect(center=sprite2_rect.center)
                
                if game_over == False:
                # Sprite Position
                    sprite2_rect.center = pos
                    screen.blit(rotated_sprite2, rotated_rect.topleft)
                
                # Asteroid Load
                for asteroid in asteroids:
                    asteroid_rect = asteroid[0]
                    speed_x = asteroid[1]
                    speed_y = asteroid[2]
                    
                    #Asteroids Speed/Multipler
                    asteroid_rect.x += speed_x * speed_multiplier
                    asteroid_rect.y += speed_y * speed_multiplier
                    
                    # Reset
                    if asteroid_rect.right < 0 or asteroid_rect.left > 1280 or asteroid_rect.bottom < 0 or asteroid_rect.top > 720:
                        new_asteroid, new_speed_x, new_speed_y = spawn_asteroid()
                        asteroid[0], asteroid[1], asteroid[2] = new_asteroid, new_speed_x, new_speed_y
                    screen.blit(asteroid2, asteroid_rect)
                    
                    if game_over == False:
                        # Collision detection
                        if sprite2_rect.colliderect(asteroid_rect):
                            screen.blit(damage2, (0, 0))
                            damaged()
                    
                    # Coin Load
                for coin in coins:
                    screen.blit(coin_image, coin)
                    # Coin Collected
                    if sprite2_rect.colliderect(coin):
                        coinfx.play()
                        coins.remove(coin)
                        score += 1
                        new_coin = spawn_coin()
                        coins.append(new_coin)

                       # Score Display
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                screen.blit(score_text, (550, 20))
                    
                    #Health
                health_bar.draw(screen)
                if health_bar.hp <= 0:
                 gameover()
                 game_over = True
                       
                # Increase Speed
                speed_multiplier += speed_increment     
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        
        # Frame Rate
        clock.tick(60)
    pygame.quit()
main()