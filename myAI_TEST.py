'''
Cozmo AI addons
'''

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose

import time, random, sys

from uselessMachine import useless, tap_handler

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')

interaction = 0


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
        batt = self.world.robot.battery_voltage  # 3.3-3.6 3.7-3.9 4.0-4.2
        if batt >= 4.0:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='green')
        elif batt <= 3.6:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='red')
        else:
            text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='orange')
        text.render(d, bounds)


def object_tapped(evt, obj=None, tap_count=None, **kwargs):
    if interaction == 1:
        tap_handler(evt, obj=None, **kwargs)


def cozmo_program(robot: cozmo.robot.Robot):
    robot.world.image_annotator.add_static_text('text', 'Coz-Cam', position=cozmo.annotate.TOP_RIGHT)
    robot.world.image_annotator.add_annotator('clock', clock)
    robot.world.image_annotator.add_annotator('battery', Battery)
    print("--------------------------")
    print("Battery (below 3.5V is low)")
    print(robot.world.robot.battery_voltage)
    print("--------------------------")

    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, object_tapped)
    # Initialization
    if robot.is_on_charger:
        robot.drive_off_charger_contacts().wait_for_completed()
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()

    robot.start_freeplay_behaviors()

    while True:
        time.sleep(1)
        # Run mini games
        run = random.randint(0,100)
        global interaction
        if run == 1:
            interaction = 1
            useless(robot)
        interaction = 0


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
