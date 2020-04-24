from MainMenu import Menu
import constants as c
import pygame

def run():
    # We will start with the main menu to start the proj.
    freshStart = True  # for initializing map animation
    running = True
    MENUSTAT = True
    game = False
    screen = pygame.display.set_mode((c.windowLength, c.windowWidth))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Risk (GAME WINDOW)")
    background1 = pygame.image.load(c.imagePath + c.menuBackgroundImage)

    newMenu = Menu(MENUSTAT, screen, clock, background1)

    Menu.startMenu(newMenu)

if __name__ == "__main__":
    run()