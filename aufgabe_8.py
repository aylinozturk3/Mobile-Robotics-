import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import math
import numpy as np
import time

def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    # --- Settings ---
    FMLRobot.turn(robot, 50)
    target_distance_m = 1.47    # Total distance to travel
    safe_distance_cm = 20       # Stop if object is closer than 20cm
    velocity = 550             # Driving speed (degrees per second)
    
    # --- Kinematics Calculation ---
    # distance = (degrees / 360) * circumference / gear_ratio
    # Solve for degrees: degrees = (distance * 360 * gear_ratio) / circumference
    target_degrees = (target_distance_m * 360 * robot.gear_ratio) / robot.wheel_circumference
    
    # Initialize starting encoder value
    start_encoder = robot.BP.get_motor_encoder(robot.left_motor)
    traveled_degrees = 0
    
    print(f"Task 8: Starting. Target: {target_distance_m}m ({int(target_degrees)} deg)")

    try:
        while traveled_degrees < target_degrees:
            # 1. Update distance traveled
            current_encoder = robot.BP.get_motor_encoder(robot.left_motor)
            traveled_degrees = abs(current_encoder - start_encoder)
            
            # 2. Check for Obstructions
            # Uses get_distance_front() from your FMLRobot class
            dist_front = robot.get_distance_front()
            
            # 3. Movement Logic
            if 0 < dist_front < safe_distance_cm:
                # Obstacle detected: STOP and wait
                robot.stop()
                print(f"Obstacle at {dist_front}cm. Pausing...", end="\r")
            else:
                # Path clear: DRIVE
                robot.BP.set_motor_dps(robot.left_motor, velocity)
                robot.BP.set_motor_dps(robot.right_motor, velocity)
            
            # Update internal odometry during movement
            robot.update_position()
            time.sleep(0.05)

        # Final Stop
        robot.stop()
        print("\nTask 8: Goal Reached.")

    except Exception as e:
        print(f"\nTask 8 failed: {e}")
        robot.stop()

