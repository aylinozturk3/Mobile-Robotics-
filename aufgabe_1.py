import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("..")
sys.path.append(".")

from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLController import PIController



def doTask(robot, mqtt, camera):

    print("Task 1: Waiting for green light signal...")
    
    green_threshold = 0.20
    is_green = False

    while not is_green:
        percentage = camera.get_green_percentage()

        if percentage > green_threshold:
            print(f"Green detected ({percentage:.2%})! Starting journey...")
            is_green = True
        else:
            time.sleep(0.1)
    
    line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
    velocity = 300

    left_color = None

    FMLRobot.drive(robot, 0.02)

    while left_color != "Red":

        left_color = robot.get_color_left()

        current_sensor_val = robot.BP.get_sensor(robot.right_sensor)
        u = line_controller.get_u(current_sensor_val)

        robot.BP.set_motor_dps(robot.left_motor, velocity + u)
        robot.BP.set_motor_dps(robot.right_motor, velocity - u)

        time.sleep(0.01)

    FMLRobot.stop(robot)
    FMLRobot.turn(robot, 90)

    print("Reached red marker. Task 1 complete.")

