#!/usr/bin/python
from Tkinter import *
from string import *

from ConfigDlg import *
"""
This is the Stars! Coalition Tool (SCoT), version 0.1 alpha.

Code for drawing a star: mapCanvas.create_rectangle (100, 100, 103, 103, fill='white')
    Of course, fill= can be set to a color appropriate to the player.

Stars' <gamename>.pla file contains a tab-seperated list of planets explored by the
    player.  This information can be uploaded to the SCoT server by the SCoT
    client.  When the SCoT client draws the map, it will automatically draw in
    the planets which have been explored/colonized by each player.

Stars' <gamename>.map file contains a complete list of every planet in the universe,
    complete with X/Y coords.

Not sure how to accomplish zooming yet, but that can wait.

Stars' X and Y coordinates are different from Tkinter-Canvas' coordinates.  The
    X coordinates work fine, but the Y coordinates need to be inverted.  Therefore,
    if a star is at X:1500,Y:500, it is in fact at X:1500,Y:1500.  Formula:
    Y = (2000 - (Y - 1000)).

Add 'intel' file.

-Read the entire map, to build a generified list of planets
-Read the planets file, to add in owner info
-Later, possibly add reading in fleet info.
"""

class Player:
    def __init__(self, playerId=-1, playerName='', playerColor=''):
        self.id = playerId
        self.name = playerName
        self.color = playerColor;

class gamePlayers:
    def __init__(self):
        self.players = []
        self._playerNames = [ 'Kinnakku', 'Zylar', 'Alpacan', 'Micronaut', 'Zodor', 'Ozarkian',
                  'Thylon', 'Murtlean', 'Rhadsu', '', 'Mooninite', 'Rasta-Roach', '' ]
        self._colors = [ '#f6f239', '#ff0000', '#ffffff', '#0000ff', '#ffff00', '#ff00ff', 
                 '#00ffff', '#7b0000', '#007d00', '#00007b', '#7b7d7b', '#39ca62', 
                 '#ff7d20' ]

        for i in range(0, len(self._playerNames)):
            self.players.append(Player(i+1, self._playerNames[i], self._colors[i]))

    def findPlayer(self, playerName):
        found = 0
        i = 0
        while found != 1 and i < 13:
            if self.players[i].name == playerName:
                found = 1
            else:
                i = i + 1
        if found:
            return i
        else:
            return -1
                


class Planet:
    def __init__(self, xCoord=-1, yCoord=-1, planetName='', 
            playerId=-1, populationVal=0, pctValue=0.01, numMines=0, 
            numFactories=0, pctDefense=0.00, ktIronium=0, ktBoranium=0, 
            ktGermanium=0, numResources=0):
        self.x        = xCoord
        self.y         = yCoord
        self.name    = planetName
        self.owner    = playerId
        self.population    = populationVal
        self.value    = pctValue
        self.mines    = numMines
        self.factories    = numFactories
        self.defense    = pctDefense
        self.ironium    = ktIronium
        self.boranium    = ktBoranium
        self.germanium    = ktGermanium
        self.resources    = numResources

    
    def config(self, xCoord=None, yCoord=None, planetName=None, 
            playerId=None, populationVal=None, pctValue=None, numMines=None, 
            numFactories=None, pctDefense=None, ktIronium=None, ktBoranium=None, 
            ktGermanium=None, numResources=None):
        if xCoord != None:
            self.x = xCoord
        if yCoord != None:
            self.y = yCoord
        if planetName != None:
            self.name = planetName
        if playerId != None:
            self.owner = playerId
        if populationVal != None:
            self.population = populationVal
        if pctValue != None:
            self.value = pctValue
        if numMines != None:
            self.mines = numMines
        if numFactories != None:
            self.factories = numFactories
        if pctDefense != None:
            self.defense = pctDefense
        if ktIronium != None:
            self.ironium = ktIronium
        if ktBoranium != None:
            self.boranium = ktBoranium
        if ktGermanium != None:
            self.germanium = ktGermanium
        if numResources != None:
            self.resources = numResources


    def getAttribute(self, attrName=None):
        if attrName != None:
                # 'Report Age',    # XXX
            if attrName == 'xCoord':
                return self.x
            if attrName == 'yCoord':
                return self.y
            if attrName == 'planetName' or attrName == 'Planet Name':
                return self.name
            if attrName == 'playerId' or attrName == 'Owner':
                return self.owner
            if attrName == 'populationVal' or attrName == 'Population':
                return self.population
            if attrName == 'pctValue' or attrName == 'Value':
                return self.value
            if attrName == 'numMines' or attrName == 'Mines':
                return self.mines 
            if attrName == 'numFactories' or attrName == 'Factories':
                return self.factories
            if attrName == 'pctDefense' or attrName == 'Def %':
                return self.defense
            if attrName == 'ktIronium' or attrName == 'Surface Ironium':
                return self.ironium
            if attrName == 'ktBoranium' or attrName == 'Surface Boranium':
                return self.boranium
            if attrName == 'ktGermanium' or attrName == 'Surface Germanium':
                return self.germanium
            if attrName == 'numResources' or attrName == 'Resources':
                return self.resources
        return None
                


class SCoT(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.topLevel = master
        self.planets = []
        self.zoomLevels = [ 0.25, 0.38, 0.50, 0.75, 1.00, 1.25, 1.50, 2.0, 4.0 ]
        self.currentZoom = 4 # 100% or 1.00
        self.displayLabels = [ 
            'Planet Name',
            'Owner',
            'Starbase Type',
            'Report Age',
            'Population',
            'Value',
            'Resources',
            'Mines',
            'Factories',
            'Def %',
            'Surface Ironium',
            'Surface Boranium',
            'Surface Germanium'
        ]

        # Add these labels later: 
        # Surface Germanium  
        # Ironium Mining Rate 
        # Boranium Mining Rate 
        # Germanium Mining Rate 
        # Ironium Mineral Concentration
        # Boranium Mineral Concentration  
        # Germanium Mineral Concentration 
        # Resources

        self.bleeIndex = 1
        self.gamePlayers = gamePlayers()
        self.grid()
        self.createWidgets()
        self.readMap()
        self.readPlanets()
        self.zoomFactor = 1.0
        self.drawMap()

    def fetchFiles(self):
        self.ftpConnection = FTP(self.ftpHost, self.ftpUser, self.ftpPass)
        self.ftpConnection.login()
        self.ftpConnection.cwd(self.ftpDir)

        for i in range(1,16):
            self.fp = open("KIA2002.p%d" % (i), "w")
            self.ftpConnection.retrbinary("RETR KIA2002.p%d" % (i), self.fp.write)
            self.fp.close()

    def putFiles(self):
        try:
            self.ftpConnection = FTP(self.ftpHost, self.ftpUser, self.ftpPass)
            self.ftpConnection.login()
            self.ftpConnection.cwd(self.ftpDir)
            self.fp.open("KIA2002.pla", 'r')
            self.ftpConnection.storbinary("STOR KIA2002.p%d" % (self.playerNum), fp)
            self.ftpConnection.quit()
        except:
            pass
            
        
        

    def zoomCanvas(self):
        if self.currentZoom + 1 >= len(self.zoomLevels):
            self.currentZoom = 0
        else:
            self.currentZoom = self.currentZoom + 1
        self.zoomTo(self.zoomLevels[self.currentZoom])

    def zoomTo(self, newZoomFactor=1.00):
        self.zoomFactor = newZoomFactor
        self.statusBar.config(text="Zoom: " + str(int(self.zoomFactor * 100)) + "%")
        self.mapCanvas.config(scrollregion=(0,0,(2000*newZoomFactor)+10,(2000*newZoomFactor)+10))
            
        self.drawMap()
        self.mapCanvas.xview_moveto(0.0)
        self.mapCanvas.yview_moveto(0.0)

    def clearCanvas(self):
        self.mapCanvas.delete('ALLPLANETS')

    def createWidgets(self):
        self.pack(expand=YES, fill=BOTH)

        # Menu bar creation
        self.menuBar = Menu(self)
        self.topLevel.config(menu=self.menuBar)
        self.fileMenu = Menu(self.menuBar)
        self.fileMenu.add_command(label='Delete Texas', command=self.deleteTexas, underline=1)
        self.fileMenu.add_command(label='Exit', command=self.quit, underline=1)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu, underline=0)
        
        self.viewMenu = Menu(self.menuBar)
        self.zoomMenu = Menu(self.viewMenu)
        self.zoomMenu.add_command(label='25%', command=(lambda s=self, z=0.25: s.zoomTo(z)))
        self.zoomMenu.add_command(label='38%', command=(lambda s=self, z=0.38: s.zoomTo(z)))
        self.zoomMenu.add_command(label='50%', command=(lambda s=self, z=0.50: s.zoomTo(z)))
        self.zoomMenu.add_command(label='75%', command=(lambda s=self, z=0.75: s.zoomTo(z)))
        self.zoomMenu.add_command(label='100%', command=(lambda s=self, z=1.00: s.zoomTo(z)))
        self.zoomMenu.add_command(label='125%', command=(lambda s=self, z=1.25: s.zoomTo(z)))
        self.zoomMenu.add_command(label='150%', command=(lambda s=self, z=1.50: s.zoomTo(z)))
        self.zoomMenu.add_command(label='200%', command=(lambda s=self, z=2.00: s.zoomTo(z)))
        self.zoomMenu.add_command(label='400%', command=(lambda s=self, z=4.00: s.zoomTo(z)))
        self.viewMenu.add_cascade(label='Zoom...', menu=self.zoomMenu, underline=0)
        self.menuBar.add_cascade(label='View', menu=self.viewMenu, underline=0)

        # Screen layout
        self.displayPane = Frame()

        # Set up frames
        #self.scannerPane = Frame(self.displayPane)
        #self.scrollPane = Frame(self.displayPane)
        #self.statusPane = Frame(self.displayPane)

        # Create scroll bars
        self.xScrollBar = Scrollbar(self.displayPane)
        self.yScrollBar = Scrollbar(self.displayPane)

        # Create and configure map canvas
        self.mapCanvas = Canvas (self.displayPane, bg='black', height=600, width=800,
                        scrollregion=(0,0,2010,2010),
                        xscrollcommand=self.xScrollBar.set,
                        yscrollcommand=self.yScrollBar.set)
        self.mapCanvas.bind('<ButtonPress-1>', self.onClick)


        self.yScrollBar.config(command=self.mapCanvas.yview, orient=VERTICAL)
        self.xScrollBar.config(command=self.mapCanvas.xview, orient=HORIZONTAL)

        self.statusBar = Label(self.displayPane, text="X:0, Y:0", relief=SUNKEN)
        self.displayCanvas = Canvas (self.displayPane, height=600, width=300)

        # Grid packing layouts:     
        # xScrollBar: row=1, column=0, rowspan=1, columnspan=1, sticky=E+W
        # statusBar: row=2, column=0, rowspan=1, columnspan=3, sticky=E+W
        # displayCanvas: row=0, column=2, rowspan=2, columnspan=1, sticky=N+E
        # yScrollBar: row=0, column=1, rowspan=1, columnspan=1, sticky=N+S
        # mapCanvas: row=0, column=0, rowspan=1, columnspan=1, sticky=N+E
        self.xScrollBar.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=E+W)
        self.statusBar.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=E+W)
        self.displayCanvas.grid(row=0, column=2, rowspan=2, columnspan=1, sticky=N+E)
        self.yScrollBar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=N+S)
        self.mapCanvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=N+E)

        self.displayPane.pack(side=TOP, expand=YES, fill=BOTH)


    def readMap(self):
        self.mapFile = open('KIA2002.map', 'r')
        self.x = []
        self.y = []
        self.names = []
        linecount = 1
        for line in self.mapFile.readlines():
            if line[0] == '#':
                pass
            else:
                #def __init__(self, xCoord=-1, yCoord=-1, planetName='', 
                #        playerId=-1, populationVal=0, pctValue=0.01, numMines=0, 
                #        numFactories=0, pctDefense=0.00, ktIronium=0, ktBoranium=0, 
                #        ktGermanium=0):

                bits = split(line, "\t")
                newPlanet = Planet(    xCoord=(int(bits[1]) - 1000), 
                            yCoord=(int(bits[2]) - 1000), 
                            planetName=bits[3][:-2],
                        )
                self.planets.append(newPlanet)
            linecount = linecount + 1

    def findPlanet(self, planetName, retObject=None):
        found = 0
        for i in range(0, len(self.planets)):
            #print "comparing '%s' with '%s'" % (planetName, self.planets[i].name)
            if self.planets[i].name == planetName:
                found = 1
                if retObject:
                    return self.planets[i]
                else:
                    return i
        if not found:
            return None

    def readPlanets(self, planetFileName=None):
        if planetFileName == None:
            recursionFlag = 0
            self.planetFile = open('KIA2002.pla', 'r')
        else:
            recursionFlag = 1
            try:
                self.planetFile = open('%s' % (planetFileName), 'r')
            except IOError:
                pass
            except:
                pass
        self.planetFile.readline()        # Discard first line
        for line in self.planetFile.readlines():
            line = rstrip(line)
            line = replace(line, "\t", ':')
            line = replace(line, '::', ':0:')
            line = replace(line, '::', ':')
            bits = split(line, ':')
            if len(bits[1]) > 0:
                thisPlayerId = self.gamePlayers.findPlayer(bits[1])
                if thisPlayerId > -1:
                    # set the owner of the planet in question
                    planetId = self.findPlanet(bits[0])
                    if planetId > -1:
                        if len(bits) < 19:
                            for i in range(0,(20 - len(bits))):
                                bits.append('0')
                        # print bits
                        if bits[5][-1:] == '%':
                            bits[5] = bits[5][:-1]
                        self.planets[planetId].config(playerId=thisPlayerId,
                            populationVal=int(bits[4]),
                            pctValue=int(bits[5]),
                            numMines=int(bits[7]),
                            numFactories=int(bits[8]),
                            ktIronium=int(bits[10]),    
                            ktBoranium=int(bits[11]),    
                            ktGermanium=int(bits[12]),
                            numResources=int(bits[19])
                        )

                        #self.planets[planetId].config(pctDefense=int(float(bits[9][:-1])))
        if not recursionFlag:
            for i in range(1,16):
                self.readPlanets(planetFileName='KIA2002.p%d' % (i))


    def drawMap(self, allLabels=FALSE):
        self.clearCanvas()
        for thisPlanet in self.planets:
            self.xCoord = thisPlanet.x
            self.yCoord = thisPlanet.y
            self.yCoord = (2000 - self.yCoord)

            self.xCoord = int(self.xCoord * self.zoomFactor)
            self.yCoord = int(self.yCoord * self.zoomFactor)
            if thisPlanet.owner > -1:
                #print "Found planet w/nonzero owner: %s! (Owner: %d)" % (thisPlanet.name, thisPlanet.owner)
                fillColor = self.gamePlayers.players[thisPlanet.owner].color

                dotId = self.mapCanvas.create_oval (self.xCoord, self.yCoord, self.xCoord+9, self.yCoord+9, fill=fillColor, outline=fillColor)
                nameId = self.mapCanvas.create_text (self.xCoord, self.yCoord+20, text=thisPlanet.name, fill=fillColor)
                self.mapCanvas.addtag_withtag (thisPlanet.name, dotId)
                self.mapCanvas.addtag_withtag (thisPlanet.name, nameId)
            else:
                fillColor = 'darkgray'
                dotId = self.mapCanvas.create_rectangle (self.xCoord, self.yCoord, self.xCoord+2, self.yCoord+2, fill=fillColor, outline=fillColor)
                self.mapCanvas.addtag_withtag (thisPlanet.name, dotId)
                if allLabels:
                    nameId = self.mapCanvas.create_text (self.xCoord, self.yCoord+20, text=thisPlanet.name, fill=fillColor)
                    self.mapCanvas.addtag_withtag (thisPlanet.name, nameId)
        self.allPlanetsTag = self.mapCanvas.addtag_all('ALLPLANETS')

    def deleteTexas(self):
        self.foo = ConfigDlg(self.topLevel)

    def onClick(self, event):
        self.displayCanvas.delete('DISPLAY')
        id = self.mapCanvas.find_closest(self.mapCanvas.canvasx(event.x), self.mapCanvas.canvasy(event.y), halo=5)
        tag = self.mapCanvas.gettags (id)
        planetName = tag[0]
        self.statusBar.config(text=planetName)

        for label in self.displayLabels:
            thisPlanet = self.findPlanet(planetName, retObject=1)
            keyId = self.displayCanvas.create_text(15, 15 * self.bleeIndex, text=label, fill='black', anchor=NW)
            if label == 'Owner':
                ownerName = self.gamePlayers.players[int(thisPlanet.getAttribute(label))].name
                valId = self.displayCanvas.create_text(150, 15 * self.bleeIndex, text=ownerName, fill='black', anchor=NW)
            else:
                valId = self.displayCanvas.create_text(150, 15 * self.bleeIndex, text=thisPlanet.getAttribute(label), fill='black', anchor=NW)
            #self.displayCanvas.addtag_withtag('DISPLAY', keyId)    
            #self.displayCanvas.addtag_withtag('DISPLAY', valId)    
            self.displayCanvas.addtag_all('DISPLAY')
            self.bleeIndex = self.bleeIndex + 1

        self.bleeIndex = 1


topLevel = Tk()
app = SCoT(topLevel)
app.master.title("Stars! Coalition Tool")
app.mainloop()
