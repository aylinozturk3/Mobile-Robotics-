import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time 
import aufgabe_1 
import aufgabe_2
import aufgabe_3 
import aufgabe_4 
import aufgabe_5 
import aufgabe_6 
import aufgabe_7 
import aufgabe_8 


camera = FMLCamera()
mqtt = FMLMqtt("mqttBroker","gruppe1/shape")
line_controller = PIController(0,0.00,0)


done = False
current_task_number = -1
target_shape =None
with FMLRobot() as robot:
    while not done:
        # reset current taks number
        current_task_number = 3
        
        while current_task_number == -1:
                # Call your previously implemented scanning feature
                qr_data = camera.get_barcode()
                
                if qr_data:
                    try:
                        # Convert the string data from the QR code to an integer
                        current_task_number = int(qr_data)
                        print(f"Task {current_task_number} detected!")
                    except ValueError:
                        # If the QR code contains text instead of a number, ignore it
                        print(f"Invalid Task QR: {qr_data}")
                
                
                # Small sleep to prevent CPU overheating
                time.sleep(0.5)
        
        if current_task_number == 1:
            aufgabe_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
            aufgabe_2.doTask(robot,mqtt,camera)
        if current_task_number == 3:
            aufgabe_3.doTask(robot,mqtt,camera)
        if current_task_number == 4:
            target_shape = aufgabe_4.doTask(robot, mqtt, camera)
        if current_task_number == 5:
            aufgabe_5.doTask(robot,mqtt,camera)
        if current_task_number == 6:
            aufgabe_6.doTask(robot)
        if current_task_number == 7:
            aufgabe_7.doTask(robot, camera, target_shape=target_shape)
        if current_task_number == 8:
            aufgabe_8.doTask(robot,mqtt,camera)
            done = True
        
