import random

from direct.showbase.PythonUtil import lerp
from panda3d.core import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.DistributedObject import DistributedObject
from direct.actor import Actor
from . import FishingTargetGlobals
import math
from toontown.effects import Ripples

class DistributedFishingTarget(DistributedNode):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingTarget')
    radius = 2.5

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self)
        self.pond: DistributedObject | None = None
        self.centerPoint: tuple[float, float, float] = (0.0, 0.0, 0.0)
        self.maxRadius: float = 1.0
        self.track: Sequence = None
        self.track2: Sequence = None

    def generate(self):
        self.assign(render.attachNewNode('DistributedFishingTarget'))
        shadow = loader.loadModel('phase_3/models/props/fishshadow')
        shadow.setPos(0, 0, -0.04)
        shadow.setScale(0.35, 0.35, 0.35)
        shadow.setColorScale(1, 1, 1, 0.75)
        shadow.reparentTo(self)
        self.bubbles = Ripples.Ripples(self)
        self.bubbles.renderParent = shadow
        self.bubbles.renderParent.setDepthWrite(0)
        self.bubbles.setScale(0.4)
        self.bubbles.setPos(1, 0, 0)
        self.bubbles.setColorScale(1, 1, 1, 0.88)
        self.bubbles.play()
        DistributedNode.generate(self)

    def disable(self):
        if self.track:
            self.track.finish()
            self.track2.finish()
            self.track = None
            self.track2 = None
        self.bubbles.destroy()
        del self.bubbles
        self.pond.removeTarget(self)
        self.pond = None
        DistributedNode.disable(self)

    def delete(self):
        del self.pond
        DistributedNode.delete(self)

    def setPondDoId(self, pondDoId: int):
        self.pond = base.cr.doId2do[pondDoId]
        self.pond.addTarget(self)
        self.centerPoint = FishingTargetGlobals.getTargetCenter(self.pond.getArea())
        self.maxRadius = FishingTargetGlobals.getTargetRadius(self.pond.getArea())

    def getDestPos(self, angle: float, radius: float) -> tuple[float, float, float]:
        x = radius * math.cos(angle) + self.centerPoint[0]
        y = radius * math.sin(angle) + self.centerPoint[1]
        z = self.centerPoint[2]
        return (x, y, z)

    def setState(self, angle: float, radius: float, time: float, timeStamp: int):
        ts = globalClockDelta.localElapsedTime(timeStamp)
        prevpos = self.getPos()
        pos = self.getDestPos(angle, radius)
        destangle = math.atan2((pos[1] - prevpos[1]),
                               (pos[0] - prevpos[0]))
        self.bubbles.setH(360/math.tau * (destangle))
        if self.track and self.track.isPlaying():
            self.track.finish()
            self.track2.finish()
        self.track = Sequence(LerpPosHprScaleInterval(self, (0.3 + lerp(0.05, 0.1, time)), Point3(*prevpos), (360/math.tau * (destangle), 0.0, 0.0), (1.0 - lerp(0.05, 0.075, time), 1.1, 1.0), blendType='easeInOut'),
                              Func(self.bubbles.play, 1.0 + (0.025 * time)),
                              LerpPosHprScaleInterval(self, time - ts - 0.6, Point3(*pos), (360/math.tau * (destangle), 0.0, 0.0), (1.0, 1.0, 1.0), blendType='easeOut'))
        self.track2 = Sequence(LerpScaleInterval(self.bubbles, 0.5, lerp(0.005, 0.07, time), 0.01, blendType='easeOut'),
                               Func(self.bubbles.setHpr, 0, 0, 0))
        self.track.start()
        self.track2.start()

    def getRadius(self) -> float:
        return self.radius
