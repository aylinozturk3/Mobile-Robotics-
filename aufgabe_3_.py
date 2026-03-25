from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import dijkstra
import time

graph = {"a": {"b": 2, "d": 5, "f": 6},
          "b": {"c": 3, "e": 2},
          "c": {"g": 8, "e": 1},
          "d": {"e": 1, "h": 10},
          "e": {"g": 10, "h": 10},
          "f": {"d": 2, "i": 4},
          "g": {"j": 8},
          "h": {"j": 6, "k": 6},
          "i": {"h": 7, "l": 4},
          "j": {"n": 5, "k": 7},
          "k": {"i": 7, "n": 9},
          "l": {"m": 9},
          "m": {"k": 1},
          "n": {"o": 1},
          "o": {},
}

color_dict = {'a': "Blue", 'b': "Red", 'c': "Blue", 'd': "Blue", 'e': "Red",
                  'f': "Yellow", 'g': "Blue", 'h': "Yellow", 'i': "Red", 'j': "Red",
                  'k': "Blue", 'l': "Blue", 'm': "Red", 'n': "Yellow", 'o': "Red"}


def doTask(robot : FMLRobot, mqtt : FMLMqtt, camera : FMLCamera):

    robot.turn(-90)
    robot.drive(0.02)

    line_controller = PIController(kp = 3, ki= 0, target_value = 30)

    dist_set = 0.2
    dist_after_color = 0.1
    target_point = "k"
    exit_color = "Red"
    start_point = "a"

    robot.follower_line_redStop(velocity = 300, controller = line_controller)
    robot.drive(dist_set)

    current_point = start_point
    print("Startpoint: ", current_point)

    path = dijkstra.dijkstra(graph, current_point, target_point)
    print("Path: ", path)

    for next_point in path[1:]:
        next_color  = color_dict[next_point]
        print("Next point: ", next_point, "Next color: ", next_color)

        robot.color_search(next_color)

        robot.drive(dist_after_color)
        robot.follower_line_redStop(velocity = 300, controller = line_controller)
        robot.drive(dist_set)

        current_point = next_point
        print("Curent point: ", current_point)

    robot.green_search()
    time.sleep(1)

    robot.drive(0.1)
    robot.drop_fork(750)
    robot.drive(-0.1)
    robot.lift_fork(750)

    print("Target point ", target_point, " reached, now going to n")
    exit_point = "n"
    path_ex = dijkstra.dijkstra(graph, current_point, exit_point)
    print("Path exit: ", path_ex)


    for next_point in path_ex[1:]:
        next_color = color_dict[next_point]
        print("Next point ", next_point,"Next color: ", next_color)

        robot.color_search(next_color)

        robot.drive(dist_after_color)
        robot.follower_line_redStop(velocity = 300, controller = line_controller)
        robot.drive(dist_set)

        current_point = next_point

        print("Current point: ", current_point)

    robot.color_search(exit_color)
    robot.drive(0.2)
    print("Exit reached, task 3 completed")

