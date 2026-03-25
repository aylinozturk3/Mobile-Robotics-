import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt

AVAILABLE_FORMS = ["Circle", "Rectangle", "Triangle", "Ellipse"]

BROKER_ADDRESS = "mqttBroker"
TOPIC = "gruppe1" 
PORT = 1884


def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    print("--- Starting Task 4 ---")
    
    # 1. Setup the line following controller
    line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
    velocity = 300
    
    print("Navigating... looking for the blue marker.")

    # FIX 1: Initialize the variable before the loop checks it!
    
    robot.follower_line_until_color(velocity, line_controller, "Blue")
    
    print("Blue marker detected! Robot stopped.")
    
    
    mqtt_client = FMLMqtt(BROKER_ADDRESS, broker_port=PORT, topic="gruppe1/shape")
    
    if mqtt_client.connect():
        
        mqtt_client.publish("Arrival message published. Waiting for worker")
        print("Arrival message published. Waiting for worker...")     
        message_arrived = False
        while (not message_arrived):    # 5. Wait for the Packaging Shape
            # The read_message() method will block execution here until a message is received
            received_shape = mqtt_client.read_message()
    
            # Clean up the string just in case there are trailing spaces
            received_shape = received_shape.strip()
    
            # 6. Validate the received shape against available forms (Optional but good practice)
            if received_shape not in AVAILABLE_FORMS:
                print(f"Warning: '{received_shape}' is not in the standard available forms list.")
            elif received_shape in AVAILABLE_FORMS:
                print(f"Message received! Packaging shape is: {received_shape}")
                message_arrived = True
                
        robot.follower_line_until_color(velocity, line_controller, "Red")
                
        print("--- Task 4 Complete ---")
    else:
        print ("No mqqt connection")
    # Return the shape so it can be passed to Task 7 later!
    return received_shape

    
    