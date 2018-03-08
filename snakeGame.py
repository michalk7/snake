# Snake Game!
__author__ = 'Michał Kubara'
# our game imports
import pygame, sys, random, time, configparser, os

print("Witaj w grze Snake! \nWybierz poziom trudności:\n1 - łatwy\n2 - normalny\n3 - trudny\n4 - bardzo trudny\n5 - hardcore")
level = 0
while level not in range(1, 6):
    try:
        level = int(input("Wpisz jedną z powyższych cyfr: "))
    except ValueError:
        print("PROSZE WPROWADZIC LICZBE CALKOWITA Z PODANEGO ZAKRESU")
if level == 1:
    level *= 15
else:
    level *= 10

# check for initializing errors
check_errors = pygame.init()
# (6,0)
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized")

# Play surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption("Snake game!")

# Colors
red = pygame.Color(255, 0, 0)  # gameover
green = pygame.Color(0, 255, 0)  # snake
black = pygame.Color(0, 0, 0)  # score
white = pygame.Color(240, 240, 240)  # background, taki prawie white
brown = pygame.Color(165, 42, 42)  # food

# FPS Controller
fpsController = pygame.time.Clock()


def readhighscore():
    config = configparser.ConfigParser()
    pathname = os.path.dirname(sys.argv[0]) + "\\config.ini"
    if not os.path.isfile(pathname):
        config['Values'] = {'HighScore': '0'}
        with open(pathname, 'w') as configfile:
            config.write(configfile)
    config2 = configparser.ConfigParser()  # ?
    config2.read(pathname)
    highscorefun = int(config2['Values']['HighScore'])
    return highscorefun

# Important Variables
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]

foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0
highscore = readhighscore()

newGame = False


# Game over function
def gameover():
    game_over_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = game_over_font.render("Game over!", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (360, 15)
    playSurface.blit(game_over_surface, game_over_rect)
    showscore(0)
    pygame.display.flip()
    new_game_condition = True
    while new_game_condition:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # time.sleep(5)
                pygame.quit()   # pygame exit
                sys.exit(0)      # console exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_game_condition = False
                    playSurface.fill((0, 0, 0, 0))
                    pygame.display.flip()
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))


def showscore(choice=1):
    if choice == 1:
        score_font = pygame.font.SysFont('monaco', 24)
        score_surface = score_font.render("Score: {0}".format(score), True, black)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (80, 10)
        playSurface.blit(score_surface, score_rect)
    else:
        score_font = pygame.font.SysFont('monaco', 24)
        score_surface = score_font.render("Score: {0}".format(score), True, black)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (360, 120)
        playSurface.blit(score_surface, score_rect)
        score_surface2 = score_font.render("Highscore: {0}".format(highscore), True, black)
        score_rect2 = score_surface2.get_rect()
        score_rect2.midtop = (360, 150)
        playSurface.blit(score_surface2, score_rect2)


def savehighscore(highscorefun):
    if score > highscore:
        highscorefun = score
        config = configparser.ConfigParser()
        pathname = os.path.dirname(sys.argv[0]) + "\\config.ini"
        config.read(pathname)
        config['Values']["HighScore"] = str(score)
        with open(pathname, 'w') as configfile:
            config.write(configfile)
    return highscorefun

# Main logic of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validating a direction
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # Update snake position [x,y]
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    # Food spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        foodSpawn = True

    # Background
    playSurface.fill(white)     # sprobować dać to przed while

    # Draw Snake
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

    # Bound
    if snakePos[0] > 710 or snakePos[0] < 0:
        highscore = savehighscore(highscore)
        gameover()
        newGame = True

    if snakePos[1] > 450 or snakePos[1] < 0:
        highscore = savehighscore(highscore)
        gameover()
        newGame = True

    # Self hit
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            highscore = savehighscore(highscore)
            gameover()
            newGame = True

    # Creates new game
    if newGame:
        snakePos = [100, 50]
        snakeBody = [[100, 50], [90, 50], [80, 50]]
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        foodSpawn = True
        direction = 'RIGHT'
        changeto = direction
        score = 0
        newGame = False

    showscore()
    pygame.display.flip()
    fpsController.tick(level)
