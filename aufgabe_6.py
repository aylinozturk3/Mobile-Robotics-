import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera


def doTask(robot):
    try:
        
        robot.follower_distance(velocity=300)
    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruldu.")
    

