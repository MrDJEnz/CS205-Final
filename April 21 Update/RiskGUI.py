from tkinter import *
import Map as loadmap

optionField = [] #used for text labels
playerColors = ['red','green','blue','yellow','purple','cian'] #used for color options

#method updates tkinter menu with color options... COLOR PICKER IS BUGGY
def playerSetup():
    numPlayers = int(userInput.get())
    for i in range(0,numPlayers): # creates text field for color selection
        optionField.append("Player " + str(i+1))

    #setup color form
    playerOptions = []
    for i, j in enumerate(optionField):
        colorLabel = Label(root, width = 15, text = optionField, anchor = 'w')
        entry = Entry(root)

        colorLabel.grid(row = i, column = 0)
        entry.grid(row = i, column = 1)

        playerColors = ['red','green','blue','yellow','purple','cian'] #used for color options
        tempVar = StringVar()
        menuDrop = OptionMenu(root, tempVar, *playerColors)
        menuDrop.grid(row = i, column = 2, sticky = "ew")
        playerOptions.append((j, entry, tempVar))

    root.bind('<Return>', (lambda event, playerOptions: menuFormat(playerOptions)))
    labelNumPlayers.grid_forget()
    buttonDone.grid_forget()
    buttonQuit.grid_forget()

    b2 = Button(root, text="Start",command=lambda Arg=playerColors: checkPlayerColors(Arg))
    b2.grid(row=20, column=0)
    buttonQuit.grid(row=20, column=1)

# method keeps users from preceeding with invalid number of players
def checkNumPlayers():
    numPlayers = int(userInput.get())

    if numPlayers < 2: #min number players is 2
        print("You need at least two players to play ..")
    elif numPlayers > 6:
        print("You can have at most six players ..")
    else:
        print("Setting up Risk for " + str(numPlayers) + " players.")
        playerSetup()

#BUGGY METHOD... starts game regardless of color option
def checkPlayerColors(colorList):
    playerNames = []
    playerColors = []
    try:  
        for i in colorList:
            playerNames.append(i[1])
            if i[1] == "":
                raise ValueError("One or more players have incorrect/missing colors")
            playerColors.append(i[2])

        colorsTaken = set() #creates set of used colors
        colorsAvailable = []
        for i in playerColors:
            if i not in colorsTaken:
                colorsTaken.add(i)
                colorsAvailable.append(i)

        if not len(colorsAvailable) == len(playerNames):
            raise ValueError("You need to pick a different color for each player")
    except ValueError as e:
        print (e.args)

    else:
        global root
        root.quit()
        print("Starting game ...")
        loadmap.start() #starts pygame ...

#Method to loop to update tinker options, sourced from: https://stackoverflow.com/questions/54295666/how-to-get-entry-from-first-text-box-in-form-and-use-as-button-text/54296123#54296123
def menuFormat(entries):
   for entry in entries:
      field = entry[0]
      text = entry[1].get()
      color=entry[2].get()
      print('%s: "%s" %s' % (field, text,color))

#buttonQuit use
def goodbye():
    root.quit()
    print("Goodbye!")
    exit()



if __name__ == "__main__":
    root = Tk()
    root.title("Risk Setup")

    labelNumPlayers = Label(root, text="Enter the number of players:")
    labelNumPlayers.grid(row=0, column=0, columnspan=2)
    userInput = Entry(root, bd = 1)
    userInput.grid(row=1, column=0,columnspan = 2)

    buttonDone = Button(root, text='Done',command = checkNumPlayers)
    buttonDone.grid(row=2, column=0)
                
    buttonQuit = Button(root, text='Quit', command = goodbye)
    buttonQuit.grid(row=2, column = 1)
    
    root.mainloop()

