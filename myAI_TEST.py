'''
This is a mini game for Cozmo. Start Cozmo with a view of the 3 cubes. When it says 'My favourite color is green' you
can tap a cube and see it goes to revert it to green. Like an useless machine.
'''

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose

import time, random, sys

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')

id_cube = 0
# Define an annotator using the annotator decorator
@cozmo.annotate.annotator
def clock(image, scale, annotator=None, world=None, **kw):
    d = ImageDraw.Draw(image)
    bounds = (0, 0, image.width, image.height)
    text = cozmo.annotate.ImageText(time.strftime("%H:%m:%S"),
            position=cozmo.annotate.TOP_LEFT)
    text.render(d, bounds)

# Define another decorator as a subclass of Annotator
class Battery(cozmo.annotate.Annotator):
    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)
        batt = self.world.robot.battery_voltage #3.3-3.6 3.7-3.9 4.0-4.2
        if batt >= 4.0:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='green')
        elif batt <= 3.6:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='red')
        else:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='orange')
        text.render(d, bounds)

def tap_handler(evt, obj=None, tap_count=None, **kwargs):
    cube_tapped = evt.obj
    cube_tapped.set_lights(cozmo.lights.Light(on_color=cozmo.lights.Color(
        rgb=(round(random.random() * 255), round(random.random() * 100), round(random.random() * 255)))))
    # print(cube, tap_count)
    print("Tapped: ", cube_tapped.object_id)
    global id_cube
    id_cube = cube_tapped.object_id

def faceAppeared(evt, face=None, **kwargs):
    print("face appeared", face.name)

def actionCompleted(evt, **kwargs):
    print("actionCompleted")

def actionStarted(evt, **kwargs):
    print("actionStarted")

def animationCompleted(evt, **kwargs):
    print("animationCompleted")

def animationsLoaded(evt, **kwargs):
    print("animationsLoaded")

def behaviorStarted(evt, behavior_type_name=None, **kwargs):
    print("behaviorStarted", behavior_type_name)

def behaviorStopped(evt, **kwargs):
    print("behaviorStopped")

def newRawCameraImage(evt, **kwargs):
    print("newRawCameraImage")

def robotFound(evt, **kwargs):
    print("robotFound")

def erasedEnrolledFace(evt, **kwargs):
    print("erasedEnrolledFace")

def faceDisappeared(evt, **kwargs):
    print("faceDisappeared")

def faceIdChanged(evt, **kwargs):
    print("faceIdChanged")

def faceObserved(evt, **kwargs):
    None
    #print("faceObserved")

def faceRenamed(evt, **kwargs):
    print("faceRenamed")

def objectAppeared(evt, **kwargs):
    print("objectAppeared")

def objectAvailable(evt, obj=None, **kwargs):
    print("objectAvailable")

def connectChanged(evt, **kwargs):
    print("connectChanged")

def objectDisappeared(evt, **kwargs):
    print("objectDisappeared")

def objectMoving(evt, **kwargs):
    print("objectMoving")

def movingStarted(evt, **kwargs):
    print("movingStarted")

def movingStopped(evt, **kwargs):
    print("movingStopped")

def objectObserved(evt, **kwargs):
    None
    #SPAM print("objectObserved")

def petAppeared(evt, **kwargs):
    print("petAppeared")

def petDisappeared(evt, **kwargs):
    print("petDisappeared")

def petObserved(evt, **kwargs):
    print("petObserved")

def robotReady(evt, **kwargs):
    print("robotReady")

def newCameraImage(evt, **kwargs):
    print("newCameraImage")


def cozmo_program(robot: cozmo.robot.Robot):
    robot.world.image_annotator.add_static_text('text', 'Coz-Cam', position=cozmo.annotate.TOP_RIGHT)
    robot.world.image_annotator.add_annotator('clock', clock)
    robot.world.image_annotator.add_annotator('battery', Battery)
    print("--------------------------")
    print("Battery (below 3.5V is low)")
    print(robot.world.robot.battery_voltage)
    print("--------------------------")

    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, tap_handler)
    robot.world.add_event_handler(cozmo.faces.EvtFaceAppeared, faceAppeared)
    robot.world.add_event_handler(cozmo.action.EvtActionCompleted, actionCompleted)
    robot.world.add_event_handler(cozmo.action.EvtActionStarted, actionStarted)
    robot.world.add_event_handler(cozmo.anim.EvtAnimationCompleted, animationCompleted)
    robot.world.add_event_handler(cozmo.anim.EvtAnimationsLoaded, animationsLoaded)
    robot.world.add_event_handler(cozmo.behavior.EvtBehaviorStarted, behaviorStarted)
    robot.world.add_event_handler(cozmo.behavior.EvtBehaviorStopped, behaviorStopped)
    #SPAM robot.world.add_event_handler(cozmo.camera.EvtNewRawCameraImage, newRawCameraImage)
    robot.world.add_event_handler(cozmo.conn.EvtRobotFound, robotFound)
    robot.world.add_event_handler(cozmo.faces.EvtErasedEnrolledFace, erasedEnrolledFace)
    robot.world.add_event_handler(cozmo.faces.EvtFaceDisappeared, faceDisappeared)
    robot.world.add_event_handler(cozmo.faces.EvtFaceIdChanged, faceIdChanged)
    robot.world.add_event_handler(cozmo.faces.EvtFaceObserved, faceObserved)
    robot.world.add_event_handler(cozmo.faces.EvtFaceRenamed, faceRenamed)
    robot.world.add_event_handler(cozmo.objects.EvtObjectAppeared, objectAppeared)
    robot.world.add_event_handler(cozmo.objects.EvtObjectAvailable, objectAvailable)
    robot.world.add_event_handler(cozmo.objects.EvtObjectConnectChanged, connectChanged)
    robot.world.add_event_handler(cozmo.objects.EvtObjectDisappeared, objectDisappeared)
    robot.world.add_event_handler(cozmo.objects.EvtObjectMoving, objectMoving)
    robot.world.add_event_handler(cozmo.objects.EvtObjectMovingStarted, movingStarted)
    robot.world.add_event_handler(cozmo.objects.EvtObjectMovingStopped, movingStopped)
    robot.world.add_event_handler(cozmo.objects.EvtObjectObserved, objectObserved)
    robot.world.add_event_handler(cozmo.pets.EvtPetAppeared, petAppeared)
    robot.world.add_event_handler(cozmo.pets.EvtPetDisappeared, petDisappeared)
    robot.world.add_event_handler(cozmo.pets.EvtPetObserved, petObserved)
    robot.world.add_event_handler(cozmo.robot.EvtRobotReady, robotReady)
    #SPAM robot.world.add_event_handler(cozmo.world.EvtNewCameraImage, newCameraImage)

    #robot.say_text("A I loading...", use_cozmo_voice=False).wait_for_completed()
    #Initialization
    if robot.is_on_charger:
        robot.drive_off_charger_contacts().wait_for_completed()
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()

    robot.start_freeplay_behaviors()
    while True:
        time.sleep(1)
        #Run mini games
        run = random.randint(0,100)
        if run  == 1:
            useless(robot)


def useless(robot):
    robot.stop_freeplay_behaviors()
    print("StartMiniGame X")
    new_color = cozmo.lights.Color(rgb=(0, 255, 0))
    green = cozmo.lights.Light(on_color=new_color)

    cubes = [robot.world.light_cubes.get(cozmo.objects.LightCube1Id),
             robot.world.light_cubes.get(cozmo.objects.LightCube2Id),
             robot.world.light_cubes.get(cozmo.objects.LightCube3Id)]
    for cube in cubes:
        cube.set_lights(green)
    robot.say_text("Where are my cubes?").wait_for_completed()
    look = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cube_vision = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube,
                                                             timeout=30,
                                                             include_existing=True)
    look.stop()
    print("Cubes found")
    robot.say_text("My favourite color is green!").wait_for_completed()
    global id_cube
    while True:
        time.sleep(1)
        if id_cube:
            robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
            print("vado verso il cubo", id_cube)
            for mycube in cube_vision:
                if mycube.object_id == id_cube:
                    robot.go_to_object(mycube, distance_mm(60)).wait_for_completed()
                    robot.play_anim(name="ID_pokedB").wait_for_completed()
                    mycube.set_lights(green)
            id_cube = None
            if random.random() > 0.7:
                print("Stop minigame")
                robot.say_text("I don't want to play anymore").wait_for_completed()
                break
    robot.start_freeplay_behaviors()

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
