import cozmo
from cozmo.util import distance_mm, speed_mmps
import random, time

id_cube = 0

def tap_handler(evt, obj=None, tap_count=None, **kwargs):
    cube_tapped = evt.obj
    cube_tapped.set_lights(cozmo.lights.Light(on_color=cozmo.lights.Color(
        rgb=(round(random.random() * 255), round(random.random() * 100), round(random.random() * 255)))))
    # print(cube, tap_count)
    print("Tapped: ", cube_tapped.object_id)
    global id_cube
    id_cube = cube_tapped.object_id

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