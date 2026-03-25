import sys

sys.path.append("..")

sys.path.append(".")

from FMLRobot import FMLRobot

from FMLController import PIController

from FMLCamera import FMLCamera

from FMLMqtt import FMLMqtt

import time



def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    # --- PHASE 1: Scan the Initial Order QR ---
    time.sleep(1)

    FMLRobot.turn(robot, -45)


    print("Step 1: Scan the target QR code from the paper...")
    target_qr = None
    while target_qr is None:
        target_qr = camera.get_barcode()
        time.sleep(0.5)
    print(f"Target QR identified: {target_qr}")

    FMLRobot.turn(robot, -45)

# --- PHASE 2: Navigation and Blue Search Framework ---
    # Initialize the controller for black lane navigation
    # Adjust Kp and target_value based on your light sensor calibration
    
    print("Starting line following. Searching for Blue markers...")

    
    line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
    velocity = 300
    found_correct_container = False
    
    while not found_correct_container:
        # 1. Implementation of Follower Line (Right Sensor)
        # We read the right sensor to stay on the black line edge
        current_sensor_val = robot.BP.get_sensor(robot.right_sensor)
        u = line_controller.get_u(current_sensor_val)
        
        # Apply the simplified steering logic: velocity + u / velocity - u
        robot.BP.set_motor_dps(robot.left_motor, velocity + u)
        robot.BP.set_motor_dps(robot.right_motor, velocity - u)

        # 2. Framework for Blue Search (Left Sensor)
        # The robot checks for the blue station marker while driving
        if robot.get_color_left() == "Blue":
            robot.stop()
            print("Blue marker detected! Entering verification state...")
            # TODO: Implementation of the 90-degree turn
            FMLRobot.turn(robot, -90)
            time.sleep(5)
            # TODO: Implementation of QR comparison
            current_qr = None
            current_qr = camera.get_barcode()
            if current_qr == target_qr:
                FMLRobot.drop_fork(robot, 750)
                FMLRobot.drive(robot, 0.1)
                FMLRobot.lift_fork(robot, 750)
                FMLRobot.drive(robot, -0.1)
                FMLRobot.turn(robot, 90)
                found_correct_container = True
            
            else:
                FMLRobot.turn(robot, 90)
                FMLRobot.drive(robot, 0.05)
                current_qr = None
            # TODO: Implementation of the forklift pickup
            
            # For now, we use this as a place holder to show the framework works
            # If the correct QR is found and picked up, set:
            # found_correct_container = True 
            
            # If not found, turn back and nudge forward to clear the marker
            print("Placeholder: Returning to line search...")
            time.sleep(1) 
        
        # Small delay to prevent CPU overloading
        time.sleep(0.01)

    line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
    velocity = 300
    task_2_end = False

    while not task_2_end:

        current_sensor_val = robot.BP.get_sensor(robot.right_sensor)
        u = line_controller.get_u(current_sensor_val)
        
        robot.BP.set_motor_dps(robot.left_motor, velocity + u)
        robot.BP.set_motor_dps(robot.right_motor, velocity - u)

        if robot.get_color_left() == "Red":
            robot.stop()
            FMLRobot.turn(robot, 90)
            print("Task 2 Completed.")
            task_2_end = True


            