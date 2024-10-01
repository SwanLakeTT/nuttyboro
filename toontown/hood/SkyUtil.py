from panda3d.core import *
from toontown.toonbase.ToontownGlobals import *
from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal
notify = DirectNotifyGlobal.directNotify.newCategory('SkyUtil')

def cloudSkyTrack(task):
    task.h += globalClock.getDt() * 0.25
    if task.cloud1.isEmpty() or task.cloud2.isEmpty():
        notify.warning("Couln't find clouds!")
        return Task.done
    task.cloud1.setH(task.h * 1.2)
    task.cloud2.setH(-task.h * 1.0)
    return Task.cont


def startCloudSky(hood, parent = camera, effects = CompassEffect.PRot | CompassEffect.PZ):
    hood.sky.reparentTo(parent)
    hood.sky.setDepthTest(0)
    hood.sky.setDepthWrite(0)
    hood.sky.setBin('background', 100)
    hood.sky.find('**/Sky').reparentTo(hood.sky, -1)
    hood.sky.reparentTo(parent)
    hood.sky.setZ(44.0)
    hood.sky.setHpr(0.0, 0.0, 0.0)
    ce = CompassEffect.make(NodePath(), effects)
    hood.sky.node().setEffect(ce)
    skyTrackTask = Task(hood.skyTrack)
    skyTrackTask.h = 0
    skyTrackTask.cloud1 = hood.sky.find('**/cloud1')
    skyTrackTask.cloud2 = hood.sky.find('**/cloud2')
    skyTrackTask.sky = hood.sky.find('**/Sky')
    skysun = loader.loadModel('phase_4/models/props/sun.bam')
    if skysun:
        skysun.reparentTo(hood.sky)
        skysun.setDepthWrite(0)
        skysun.setY(200)
        skysun.setZ(55)
        skysun.setScale(1.3)
        skysun.setBillboardPointEye()
    skyhills = loader.loadModel('phase_13/models/parties/partyGrounds')
    if skyhills:
        skyhills.reparentTo(hood.sky)
        hills = hood.sky.find('**/hill_flat')
        colls = hood.sky.find('**/floor_collision')
        if hills:
            hills.setZ(-60)
            hills.setScale(1.7, 1.7, 1.75)
            hills.setBin('background', 110)
            skyhills.hide()
            hills.show_through()
        if colls:
            colls.stash()


    skyTrackTask.sky.setScale(1.1, 1.1, 1.5)
    skyTrackTask.cloud2.setScale(0.75, 0.75, 0.8)
    skyTrackTask.cloud1.setScale(1.1, 1.1, 1.1)
    skyTrackTask.sky.setZ(-40.0)
    if not skyTrackTask.cloud1.isEmpty() and not skyTrackTask.cloud2.isEmpty():
        taskMgr.add(skyTrackTask, 'skyTrack')
    else:
        notify.warning("Couln't find clouds!")
