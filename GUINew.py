from Tkinter import *
from tkFileDialog import askopenfilename
from eventBasedAnimationClass import EventBasedAnimationClass
import string

#Select Background and Foreground songs

class MusicMasher(EventBasedAnimationClass):

    def __init__(self):
        width = height = 600
        super(MusicMasher, self).__init__(width, height)

    def initAnimation(self):
        SongSelectPage = SongSelect(self.root, self.canvas)
        self.pages = [SongSelectPage]
        self.page = self.pages[0]

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.page.redrawAllTitlePage() 

class SongSelect(EventBasedAnimationClass):

    def __init__(self, root = None, canvas = None):
        self.foregroundNames = []
        self.backgroundNames = [] 
        width = height = 600
        super(SongSelect, self).__init__(width,height, root, canvas)
        if root != None:
            self.initAnimation()

    def initAnimation(self):
        self.title = ('''Music Masher''')
        self.root.title(self.title)
        self.initAnimationButton1()
        self.initAnimationButton2()
        self.initAnimationButton3()
        self.errorList = []
        self.background = PhotoImage(file="DJC.gif")

    @staticmethod
    def isAudioType(name):
        if name.endswith(".mp3") or name.endswith(".mp4") or name.endswith(".wav") or name.endswith(".m4a"): return True
        return False 

    def initAnimationButton1(self):
        self.buttonFrame = Frame(self.root)
        def callback():
            name = askopenfilename()
            if SongSelect.isAudioType(name) == False:
                self.errorList += [[name,5]]
                return
            self.foregroundNames += [name]
            #just add filename to list of songs
        errmsg = 'Error!'
        b1 = Button(text='Choose Foreground File',
                    command=callback)
        xLoc, yLoc = self.width/8, self.height*3/4
        b1.place(x=xLoc,y=yLoc)


    def initAnimationButton2(self):
        def callback():
            name = askopenfilename()
            if name != "" and SongSelect.isAudioType(name) == False:
                self.errorList += [[name,5]]
                return
            self.backgroundNames += [name]
        errmsg = "Error!"
        b2 = Button(text='Choose Background Files', command=callback)
        xLoc, yLoc = self.width*5/8, self.height*3/4
        b2.place(x=xLoc,y=yLoc)

    def initAnimationButton3(self):
        def playMusic():
            return 42
        errmsg = "Error!"
        b3 = Button(text='Mash Music', command=playMusic, fg = 'blue')
        xLoc, yLoc = self.width*5/12, self.height*7/8
        b3.place(x=xLoc,y=yLoc)

    def onTimerFired(self):
        
        for i in xrange(len(self.errorList)):    
            self.errorList[i][1] -= 1
        
        self.errorList = [elem for elem in self.errorList if elem[1]>0]     

    def redrawAllTitlePage(self):
        canvas = self.canvas
        canvas.delete(ALL)
        self.onTimerFired()
        margin = 40
        step = 15
        shift = 50
        canvas.create_image(self.width/2, self.height/2, image = self.background)
        canvas.create_text(self.width/2,margin,
                                text = "Music Masher",fill="white",
                                font="Helvetica 26 bold",
                                anchor = CENTER)
        canvas.create_text(self.width/2,self.height/2-shift,
                                text="Songs",
                                font="Helvetica 20 bold",
                                fill='white',anchor=CENTER)

        for i in xrange(len(self.errorList)):
            name = self.errorList[i][0]
            name = name[len(name)-name[::-1].find('/')-1+1:]
            textt = "Invalid File Type: " + name 
            canvas.create_text(self.width/2,
                                    self.height/4+step*i,text=textt,
                                    fill='red',
                                    anchor=CENTER)

        for i in xrange(len(self.foregroundNames)):
            name = self.foregroundNames[i]
            textt = name[len(name)-name[::-1].find('/')-1+1:]
            canvas.create_text(self.width/4,
                                    self.height/2+step*i,text=textt,
                                    fill='white',
                                    anchor=CENTER)

        for i in xrange(len(self.backgroundNames)):
            name = self.backgroundNames[i]
            textt = name[len(name)-name[::-1].find('/')-1+1:]
            canvas.create_text(self.width*3/4,
                                    self.height/2+step*i,text=textt,
                                    fill='white',
                                    anchor=CENTER)
                                
    def redrawAll(self):
        self.redrawAllTitlePage()



#passing and setting variable functions
    def passVar(self): return None
    def setVar(self,var): pass

MusicMasher().run()
#SongSelect().run()
