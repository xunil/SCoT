from Tkinter import *
from ConfigParser import *

        
class ConfigDlg(Frame):
    def __init__(self, master=None, configFileName='SCoT.ini'):
        self.cfg = ConfigParser()
        self.cfg.read(configFileName)
        self.playerInfo = []
        for i in range(16):
            self.playerInfo.append({})
        for sectionName in self.cfg.sections():
            if (sectionName != 'SCoT'):
                playerNo = int(sectionName[6:])
                self.playerInfo[playerNo] =    {'selfFlag': int(self.cfg.get(sectionName, 'selfFlag')),
                                'playerName': self.cfg.get(sectionName, 'playerName'),
                                'PRT': self.cfg.get(sectionName, 'PRT'),
                                'memberFlag': self.cfg.get(sectionName, 'memberFlag')}
        self.createWidgets(topLevel=master)

    def createWidgets(self, topLevel=None):
        self.topLevel = Tk()
        self.topFrame = Frame(self.topLevel)
        self.topFrame.pack(side=TOP, fill=X)
        
        Label(self.topFrame, text='Game Name').grid(column=0, row=0)
        self.gameName = Entry(self.topFrame, width=40)
        self.gameName.grid(column=1, row=0, columnspan=3)

        Label(self.topFrame, text='Number of Players').grid(column=0, row=1)
        self.numPlayers = Entry(self.topFrame, width=3)
        self.numPlayers.grid(column=1, row=1, columnspan=3)


        Label(self.topFrame, text='Me').grid(column=0, row=2)
        Label(self.topFrame, text='Player Name').grid(column=1, row=2)
        Label(self.topFrame, text='PRT').grid(column=2, row=2)
        Label(self.topFrame, text='Member?').grid(column=3, row=2)

        self.thisIsMe = None
        self.whoAmI = []
        self.playerName = []
        self.PRT = []
        self.coalitionMember = []
        self.cmVar = []
        for i in range(1,16):
            self.whoAmI.append(Radiobutton (self.topFrame, value=i, 
                variable=self.thisIsMe))
            self.whoAmI[i-1].grid(column=0, row=2+i)
            self.playerName.append(Entry (self.topFrame, width=30))
            self.playerName[i-1].grid(column=1, row=2+i)
            self.PRT.append(Entry (self.topFrame, width=4))
            self.PRT[i-1].grid(column=2, row=2+i)
            self.cmVar.append(0)
            self.coalitionMember.append(Checkbutton (self.topFrame, 
                variable=self.cmVar[i-1]))
            self.coalitionMember[i-1].grid(column=3, row=2+i)

        for i in range(16):
            if self.playerInfo[i] != {}:
                print "Setting player name to %s" % (self.playerInfo[i]['playerName'])
                self.playerName[i].config(text=self.playerInfo[i]['playerName'])
        
        self.okBtn = Button(self.topFrame, text='OK', command=self.topLevel.destroy)
        self.okBtn.grid(row=19, column=0, columnspan=2, sticky=E+W)

        self.cancelBtn = Button(self.topFrame, text='Cancel', command=self.topLevel.destroy)
        self.cancelBtn.grid(row=19, column=2, columnspan=2, sticky=E+W)

        self.topLevel.grab_set()
        self.topLevel.focus_set()
        self.topLevel.wait_window()

if __name__ == '__main__':
    bloatis = ConfigDlg()
