        
class GameFunctions:
    def __init__(self):
        self.curX = 1000
        self.curY = 0
        self.inputText = ""

    def ask(self,inputArg):
        import tkinter as tk
        from tkinter import Button
        from tkinter import Label
        from tkinter import Entry

        def get_text():
            self.text = playerEntry.get()
            inputFrame.destroy()   

        inputFrame = tk.Tk()

        inputFrame.title("Input")
        Label(inputFrame, text=inputArg).grid(row=0)

        playerEntry = Entry(inputFrame)
        playerEntry.grid(row=0, column=1)

        Button(inputFrame, text="Quit", command=inputFrame.quit).grid(row=2, column=0, sticky='w', pady=4)
        Button(inputFrame, text="Enter", command=get_text).grid(row=2, column=1, sticky='w', pady=4)

        inputFrame.mainloop()

        return self.text
    
    def initGame(self, frame, canvas):

        playerNum = int(self.ask("How many players?"))

        players = []
        colors = ["red2", "yellow", "blue2", "lime green", "gray2", "saddle brown"]
        inputColors = {
            "red": colors[0],
            "yellow": colors[1],
            "blue": colors[2],
            "green": colors[3],
            "black": colors[4],
            "brown":colors[5]
        }
        takenColors = []

        for i in range(playerNum):
            playerName = self.ask("What's your name?")
            text = "Hello " + playerName + ". What color?\n"
            for name,real in inputColors.items():
                if not name in takenColors:
                    text += "\t" + name + "\n"
            color = self.ask(text)
            takenColors += [color]
            playerColor = inputColors[color]
            players += [(playerName, playerColor)]

        print(players)
        totalArmies = 35 - (playerNum-3)*5

        from PygameGraphics import GraphicsMain
        import os, time
        import Territories
        CountryInfo = Territories.CountryInfo()
        print(totalArmies)
        for j in range(totalArmies):
            for k in players:
                print(k[0] + " pick a country: ")
                while True:
                    time.sleep(0.5)
                    if os.path.exists("CurrentClickedCountry.txt"):
                        file = open("CurrentClickedCountry.txt", "r")
                        country = file.read().strip("\n")
                        print(k[0] + " picks " + country)
                        file.close()
                        os.remove("CurrentClickedCountry.txt")
                        CountryInfo.ChangeCountryColor(country, k[1])
                        CountryInfo.ChangeCountryArmyCount(country, 1)
                        break
                    else:
                        continue          
        
        print("Game inited")

    def printOnScreen(self, canvas, text):
        canvas.delete("printText")
        canvas.create_text(self.curX,
                           self.curY,
                           anchor="nw",
                           fill="ghost white",
                           font="Times",
                           text=text,
                           tag="printText")
