from direct.interval.LerpInterval import LerpScaleInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import Vec4, Vec3
from direct.gui.DirectGui import DirectFrame, DirectLabel
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownIntervals

class StatsMeter(DirectFrame):

    def __init__(self, avdna, hp, maxHp):
        DirectFrame.__init__(self, relief=None, sortOrder=50)
        self.initialiseoptions(StatsMeter)
        self.container = DirectFrame(parent=self, relief=None)
        self.style = avdna
        self.av = None
        self.moneyvalue = hp
        self.__obscured = 0
        self.load()
        return

    def obscure(self, obscured):
        self.__obscured = obscured
        if self.__obscured:
            self.hide()

    def isObscured(self):
        return self.__obscured

    def load(self):
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        self.container['image'] = jarGui
        self.resetFrameSize()
        self.moneyLabel = DirectLabel(parent=self.container, relief=None, pos=(0, 0, -0.1), text='120', text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_scale=0.18, text_font=ToontownGlobals.getSignFont())
        jarGui.removeNode()
        return

    def destroy(self):
        if self.av:
            self.ignore(self.av.uniqueName('moneyChange'))
        del self.style
        del self.av
        del self.moneyvalue
        del self.beanJar
        del self.moneyLabel
        DirectFrame.destroy(self)

    def adjustText(self, other):
        if self.moneyLabel['text'] != str(base.localAvatar.getMoney()):
            self.moneyLabel['text'] = str(base.localAvatar.getMoney())
            Sequence(LerpScaleInterval(self, .3, Vec3(0.43, 0.43, 0.43), Vec3(0.46, 0.46, 0.46),
                                       blendType='easeInOut')).start()


    def start(self):
        if self.av:
            self.moneyvalue = self.av.hp
        if not self.__obscured:
            self.show()
            self.adjustText(3)
        if self.av:
            self.accept(self.av.uniqueName('moneyChange'), self.adjustText)

    def stop(self):
        self.hide()
        if self.av:
            self.ignore(self.av.uniqueName('moneyChange'))

    def setAvatar(self, av):
        if self.av:
            self.ignore(self.av.uniqueName('moneyChange'))
        self.av = av
