from MainMenu import Menu
import constants as c
import pygame


# Since we were behind we used a wikipedia page with all the map images,
# and https://github.com/Whysmerhill/Risk/tree/a23b17826e84d992bf5434b99724d7aafaae5443 as a reference point.
# Most of the code is handwritten with logic for the playerTurn borrowed from this github.
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
    numPlayers = 2
    numAI = 0
    if numPlayers + numAI >= 2:
        print("OK running")
        newMenu = Menu(MENUSTAT, screen, clock, background1)

        Menu.startMenu(newMenu,numPlayers, numAI)
    else:
        print("Rerun not enough players")

if __name__ == "__main__":
    run()
