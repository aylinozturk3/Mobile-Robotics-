import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt

def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    print("--- Starting Task 5: Following the Worker ---")
    
    robot.turn(-45)
    robot.drive(0.05)
    
    time.sleep(3)
    
    # 1. Setup the controller for tracking the QR code
    # Note: Kp will likely be very different for camera pixels vs. floor sensors!
    # Start small (e.g., 0.5) and tune it on the track.
    qr_controller = PIController(kp=0.2, ki=0.0, target_value=0.0) 
    base_velocity = 150
    
    print("Looking for worker's QR code. Waiting for red marker to stop...")
    
    # 2. Call our new modular function!
    # It will follow the QR code until it drives over "Red"
    robot.follower_qr_until_color(base_velocity, qr_controller, camera, "Red")
    
    


