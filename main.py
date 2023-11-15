# Importeer en initialiseer benodigde modulesimport pygame
import pygame, sys
import shelve
import random
from classes.button import Button
from classes.spaceship import Spaceship
from classes.gameobject import GameObject

pygame.init()

X, Y = 1200, 720

# Stel het scherm in en de titel
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Lunar Lander by Ruben and Mees")

# Stel de background in
background = pygame.image.load("assets/Space.jpg")

# Maak de benodigde variabelen aan
clock = pygame.time.Clock()
reset = None
score = 0
high_score = 0

# Aanmaken van spaceship
spaceship_img = pygame.image.load('assets/spaceshipPINK.png')
collision_img = None
spaceship_img = pygame.transform.scale(spaceship_img, (60, 60))

spaceship = Spaceship(image=spaceship_img, spaceshipX=random.randrange(50, X - 50),
                      spaceshipY=random.randrange(10, Y - 700),
                      speed=4, fuel=1000, gravity_x=.1, gravity_y=.05)

# Aanmaken van de satalieten en bom objecten
env_objects = []
dish1 = GameObject(150, 600, 0, 0, "dish_large")
dish2 = GameObject(550, 630, 0, 0, "dish")
dish3 = GameObject(650, 630, 0, 0, "dish")
env_objects.append(dish1)
env_objects.append(dish2)
env_objects.append(dish3)

# Het aanmaken van vijf bommen
for i in range(5):
    env_objects.append(GameObject(random.randrange(0 + 80, X - 80), random.randrange(200, Y - 230), 0, 0, "bomb"))

# Het aanmaken van de BombRocket
bombrocket = GameObject(10, random.randrange(200, Y - 230), 2, 0, "bombrocket")
env_objects.append(bombrocket)

# Maakt een target object
target = GameObject(350, 610, 0, 0, "target")

# Deze functie maakt een text object aan
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


# Toon alles op elke locatie op het scherm
def display(image, x, y):
    screen.blit(image, (int(x), int(y)))

def play():  # Play scherm
    while True:
        # Haalt de positie van de muis op
        play_mouse_pos = pygame.mouse.get_pos()

        # Toon de background images op het scherm (plattegrond)
        screen.fill((100, 100, 100))
        display(background, 0, -200)
        reset_button = Button(image=None, pos=(X / 2, Y / 2 - 80),
                              text_input="AGAIN", font=get_font(21), base_color="Red", hovering_color="Green")
        game_over_text = get_font(30).render("MISSION FAILED", True, "Red")


        # Beweeg en weergeef de environmental objects
        for anything in env_objects:
            anything.display(screen)
            if spaceship.collided_with(anything):
                if anything.name == 'bombrocket':
                    global collision_img
                    collision_img = True
                spaceship.image = None
                global reset
                reset = True
                display(pygame.image.load('assets/in_air_explosion_large.png'), spaceship.spaceshipX,
                        spaceship.spaceshipY)

        if collision_img == True:
            display(pygame.image.load('assets/in_air_explosion_large.png'), spaceship.spaceshipX,
                    spaceship.spaceshipY)


        # Plaats het spaceship op het scherm
        spaceship.update(screen)

        # Display de target
        target.display(screen)

        # Plaatsen van de score op het scherm
        global score
        global high_score

        score_text = pygame.font.Font("assets/font.ttf", 23).render("Landingen : " + str(score), True, "White")
        screen.blit(score_text, (40, 80))

        high_score_text = pygame.font.Font("assets/font.ttf", 23).render("Highscore : " + str(high_score), True, "White")
        screen.blit(high_score_text, (40, 120))

        # Kijkt of het spaceship geraakt is
        if (reset == True):
            if score > high_score:
                high_score = score

            score = 0
            # Het verwijderen van alle extra rocketsbombs
            for anything in env_objects:
                if anything.name == 'bombrocket':
                    env_objects.remove(anything)

            screen.blit(game_over_text, (X / 2 - 220, Y / 2 - 140))
            reset_button.update(screen)

            # Loopt door alle events en kijkt of er op enter gedrukt word
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_RETURN]:
                        env_objects.append(GameObject(10, random.randrange(200, Y - 230), 2, 0, "bombrocket"))
                        # Het resetten van alle properties
                        spaceship.spaceshipX = random.randrange(0 + 50, X - 50)
                        spaceship.spaceshipY = random.randrange(100, Y - 600)
                        spaceship.image = spaceship_img
                        reset = False
                        collision_img = None
                        spaceship.update(screen)

        if spaceship.spaceshipY >= 530:
            # Win als de speler het target aanraakt en niet te snel gaat
            if spaceship.collided_with(target) == 1:
                # Geeft alle bombs een andere locatie
                for bomb in env_objects:
                    if bomb.name == 'bomb':
                        bomb.x = random.randrange(0 + 80, X - 80)
                        bomb.y = random.randrange(200, Y - 230)
                        bombrocket.y = random.randrange(200, Y - 230)
                # Kijkt of de score voor winnen is behaald zo ja ga naar win screen
                if score > 30:
                    win_screen()

                # Hier word een extra punt gegeven voor het landen
                if score <= 30:
                    # Het toevoegen van de extra rocket bij elk nieuw level
                    extra_bomrocket = GameObject(10, random.randrange(160, Y - 230), random.randrange(1, 3), 0, "bombrocket")
                    env_objects.append(extra_bomrocket)
                    spaceship.fuel = 1000

                    spaceship.spaceshipX = random.randrange(0 + 50, X - 50)
                    spaceship.spaceshipY = random.randrange(100, Y - 600)
                    spaceship.update(screen)
                    score += 1

        for event in pygame.event.get():
            # Checkt of er op de quit button is geklikt zoja quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def options():  # Option scherm
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        # Weergeeft de tekst op Option scherm
        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            # Checkt of er op de quit button is geklikt zoja quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checkt of er op de back butten word geklikt zoja ga terug naar main menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkforinput(options_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():  # Main menu scherm
    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        # Weergeeft de tekst op Menu scherm
        menu_text = get_font(80).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            # Checkt of er op de quit button is geklikt zoja quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checkt of er op de play button is geklikt zoja play
                if play_button.checkforinput(menu_mouse_pos):
                    spaceship.image = spaceship_img
                    play()
                    # Checkt of er op de options button is geklikt zoja ga naar options
                if options_button.checkforinput(menu_mouse_pos):
                    options()
                if quit_button.checkforinput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def win_screen():
    screen.fill((0, 0, 0))

    # Het verwijderen van alle extra rocketsbombs
    global env_objects
    for anything in env_objects:
        if anything.name == 'bombrocket':
            env_objects.remove(anything)

    game_over_mouse_pos = pygame.mouse.get_pos()

    # Weergeeft de tekst op Menu scherm
    win_text = get_font(80).render("GREAT SUCCES!", True, "#b68f40")
    win_text_rect = win_text.get_rect(center=(640, 100))

    win_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                        text_input="BACK", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

    screen.blit(win_text, win_text_rect)

    win_button.changeColor(game_over_mouse_pos)
    win_button.update(screen)
    for event in pygame.event.get():
        # Checkt of er op de quit button is geklikt zoja quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Checkt of er op de play button is geklikt zoja play
            if win_button.checkforinput(game_over_mouse_pos):
                env_objects.append(GameObject(10, random.randrange(200, Y - 230), 2, 0, "bombrocket"))
                spaceship.spaceshipX = random.randrange(0 + 50, X - 50)
                spaceship.spaceshipY = random.randrange(100, Y - 600)
                spaceship.fuel = 1000
                spaceship.image = spaceship_img
                spaceship.update(screen)
                global score
                score = 0
                global reset
                reset = False
                main_menu()
                sys.exit()

    pygame.display.update()


main_menu()
clock.tick(60)
