import pygame, random
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode([WINDOW_WIDTH
                                     , WINDOW_HEIGHT])
pygame.display.set_caption('Smileeeeeeeeeeeeeeeeeee')
keep_going = True
pic = pygame.image.load('./resources/ball.bmp')
colorkey = pic.get_at((0, 0))
pic.set_colorkey(colorkey)
picx = 0
picy = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
timer = pygame.time.Clock()
speedx = 5
speedy = 5
PADDLE_WIDTH = 50
PADDLE_HEIGHT = 25
paddlex = 300
paddley = 550
picw = 100
pich = 100
points = 0
lives = 5
font = pygame.font.SysFont("Times", 24)
pygame.mixer.init()
pop = pygame.mixer.Sound('./resources/pop.wav')

def check_exit():
    global event, keep_going
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False


def update_direction(speedx, speedy):
    if picx <= 0 or picx + pic.get_width() >= WINDOW_WIDTH:
        speedx = -speedx
    if picy <= 0:
        speedy = -speedy
    return speedx, speedy


def lose_life_update(speedy, lives):
    if picy >= WINDOW_HEIGHT - pic.get_height():
        lives -= 1
        speedy = -speedy
    return lives, speedy


def redraw_screen():
    screen.fill(BLACK)
    screen.blit(pic, (picx, picy))


def draw_paddle():
    paddlex = pygame.mouse.get_pos()[0]
    paddlex -= PADDLE_WIDTH / 2
    pygame.draw.rect(screen, WHITE, (paddlex, paddley, PADDLE_WIDTH, PADDLE_HEIGHT))
    return paddlex


def update_score(points, speedy):
    if picy + pic.get_height() >= paddley and picy + pic.get_height() <= paddley + PADDLE_HEIGHT and speedy > 0:
        if picx + picw / 2 >= paddlex and picx + picw / 2 <= paddlex + PADDLE_WIDTH:
            points += 1
            speedy = -speedy
            pop.play()
    return points, speedy


def draw_game_over_message(speedx, speedy):
    notification = 'Lives' + str(lives) + 'Points : ' + str(points)
    if lives < 1:
        speedx = speedy = 0
        notification = "Game Over. Your score was: " + str(points)
        notification += ". Press F1 to play again. "
    text = font.render(notification, True, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text, text_rect)
    pygame.display.update()
    return speedx, speedy


def check_for_press_key(keep_going):
    global points, lives, picx, picy, speedx, speedy
    timer.tick(60)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F1:
            points = 0
            lives = 5
            picx = 0
            picy = 0
            speedx = 5
            speedy = 5

        if event.key == pygame.K_ESCAPE:
            keep_going = False

    return keep_going

while keep_going:
    check_exit()
    picx += speedx
    picy += speedy

    speedx, speedy = update_direction(speedx, speedy)
    lives, speedy = lose_life_update(speedy, lives)

    redraw_screen()

    paddlex = draw_paddle()

    points, speedy = update_score(points, speedy)
    speedx, speedy = draw_game_over_message(speedx, speedy)
    keep_going = check_for_press_key(keep_going)

pygame.quit()