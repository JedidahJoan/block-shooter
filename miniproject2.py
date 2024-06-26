import pygame
import os
import random
pygame.font.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOT!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE=(11 , 11, 80)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
OBSTACLE_HEIGHT, OBSTACLE_WIDTH = 30, 150
OBSTACLES = []
OBSTACLE_VEL = 2

BORDER = pygame.Rect(0, 425, WIDTH, 3)
BACKGROUND=pygame.Rect(0,0, WIDTH , HEIGHT)



HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)



TARGET_HIT = pygame.USEREVENT + 1
POINT_LOSS = pygame.USEREVENT + 2



# RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.image.load("C:\dev\python\miniproject\Assets\spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

# SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load("C:\dev\python\miniproject\Assets\space.png"), (WIDTH, HEIGHT))


def random_x():
    return random.randint(0, WIDTH-OBSTACLE_WIDTH)
OLD_OBSTACLE= pygame.Rect(random_x(), 0 , OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
last_obstacle_creation_time = 0



def draw_window(red, red_bullets, red_health):
    WIN.blit(SPACE, (0, 0))
    # pygame.draw.rect(WIN, BLUE, BACKGROUND)
    pygame.draw.rect(WIN, WHITE, BORDER)
                
    game_time = pygame.time.get_ticks()
    global last_obstacle_creation_time

    if(game_time - last_obstacle_creation_time > 2000):
        createObstacle()
        last_obstacle_creation_time = game_time
    
    for obstacle in OBSTACLES:
        pygame.draw.rect(WIN, YELLOW, obstacle)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    score_text = SCORE_FONT.render(
        "Score: " + str(score), 1, WHITE)
    WIN.blit(score_text, (WIDTH-250, 10))


    
    WIN.blit(RED_SPACESHIP, (red.x, HEIGHT-60))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL+SPACESHIP_WIDTH< WIDTH:  # RIGHT
        red.x += VEL


def handle_point_loss():
    for obstacle in OBSTACLES:
        if obstacle.colliderect(BORDER):
                pygame.event.post(pygame.event.Event(POINT_LOSS))
                OBSTACLES.remove(obstacle)
def handle_bullets(red_bullets, OBSTACLES):

                
    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            red_bullets.remove(bullet)
        for obstacle in OBSTACLES:
            if obstacle.colliderect(bullet):
                pygame.event.post(pygame.event.Event(TARGET_HIT))
                red_bullets.remove(bullet)
                OBSTACLES.remove(obstacle)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def createObstacle():
    OBSTACLE = pygame.Rect(random_x(), 0 , OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    OBSTACLES.append(OBSTACLE)
    return OBSTACLE

def main():
    red = pygame.Rect(WIDTH/2 - SPACESHIP_WIDTH//2, HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    

    red_bullets = []
    global score
    score = 0    
    red_health = 5
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for obstacle in OBSTACLES: 
            obstacle.y += OBSTACLE_VEL


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width//2-2, HEIGHT-60, 5, 10)
                    red_bullets.append(bullet)
                   

            if event.type == POINT_LOSS:
                red_health -= 1
            if event.type == TARGET_HIT:
                score += 1
               
                

        
        winner_text = ""
        if red_health <= 0:
            winner_text = "YOU LOSE!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        handle_point_loss()
        handle_bullets(red_bullets, OBSTACLES)
        

        draw_window(red,  red_bullets, red_health)

    main()


if __name__ == "__main__":
    main()

