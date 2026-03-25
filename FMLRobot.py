import brickpi3
import time
import math
import numpy as np
from FMLController import PController
from FMLController import PIController

class FMLRobot:
    def _init_motors(self):
        self.left_motor = self.BP.PORT_D
        self.right_motor = self.BP.PORT_A
        self.fork_motor = self.BP.PORT_B
        self.BP.set_motor_limits(self.left_motor, dps = 300)
        self.BP.set_motor_limits(self.right_motor, dps = 300)
        self.BP.set_motor_limits(self.fork_motor, dps = 400)

    def _init_sensors(self): 
        self.left_sensor = self.BP.PORT_4
        self.right_sensor = self.BP.PORT_3
        self.front_sensor = self.BP.PORT_1
        self.side_sensor = self.BP.PORT_2
        self.BP.set_sensor_type(self.front_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.side_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.right_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_REFLECTED)
        #self.BP.set_sensor_type(self.BP.PORT_3, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)
        self.BP.set_sensor_type(self.left_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)

    def _init_constants(self):
        self.colors = { 0:"None", 1:"Black", 2:"Blue", 3:"Green", 4:"Yellow", 5:"Red", 6:"White", 7:"Brown" } 

    # To be implemented in 01 - Kinematik
    def _init_kinematik(self):
        self.wheel_radius = 0.07/2
        self.wheel_distance = 0.132
        self.wheel_circumference = 2*math.pi*self.wheel_radius
        self.gear_ratio = 24/8# teeth_wheel/teeth_motor
        # global position of the robot within the coordinate system [x,y,phi]
        self.position = [0.0, 0.0, 0.0]
        # last encoder values are saved in the object (read out the encoder when starting the robot)
        self.encoder_left = self.BP.get_motor_encoder(self.left_motor)
        self.encoder_right= self.BP.get_motor_encoder(self.right_motor)

# Constructor (gets called on object creation -> FMLRobot())
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self._init_motors()
        self._init_sensors()
        self._init_constants()
        time.sleep(4.0)
        self._init_kinematik()

# context manager entry point
    def __enter__(self):
        return self

# context manager exit point --> gets called on exit of with block
    def __exit__(self, exc_type, exc_value, traceback):
# Stop the motors and reset the sensors etc
        self.BP.reset_all() 

    def get_distance_from_encoder(self):
        # Read out current encoder values
        new_encoder_left = self.BP.get_motor_encoder(self.left_motor)
        new_encoder_right = self.BP.get_motor_encoder(self.right_motor)
        # Compute the difference in degrees
        encdelta_left = new_encoder_left - self.encoder_left
        encdelta_right = new_encoder_right - self.encoder_right 
        # Calculate driven distance in meters for each wheel
        # Formula: (delta_degrees / 360) * circumference / gear_ratio
        dis_left = (encdelta_left / 360.0) * self.wheel_circumference / self.gear_ratio
        dis_right = (encdelta_right / 360.0) * self.wheel_circumference / self.gear_ratio
        # Update the stored encoder values for the next call
        self.encoder_left = new_encoder_left
        self.encoder_right = new_encoder_right
        return (dis_left, dis_right)
 
# odometrie
    def update_position(self):
        delta_s_left, delta_s_right = self.get_distance_from_encoder() 
        # Calculate average distance and change in angle (phi)
        delta_s = (delta_s_left + delta_s_right) / 2.0
        delta_phi = (delta_s_right - delta_s_left) / self.wheel_distance

        # Current orientation (phi) from the last step
        current_phi = self.position[2]

        # Calculate change in X and Y based on current orientation
        delta_x = delta_s * math.cos(current_phi)
        delta_y = delta_s * math.sin(current_phi)

        # Update the global position [x, y, phi]
        self.position[0] += delta_x # Update X
        self.position[1] += delta_y  # Update Y
        self.position[2] += delta_phi # Update phi    
        
    def stop(self):
        self.BP.set_motor_dps(self.left_motor, 0)
        self.BP.set_motor_dps(self.right_motor, 0)

# To be implemented in 1.1
    def turn(self,degree):
        # needed motor rotation to achieve movement 
        deg_right = (degree*math.pi*self.gear_ratio*self.wheel_distance*1.13)/self.wheel_circumference
        deg_left = -deg_right
        #turning
        self.BP.set_motor_position_relative(self.left_motor, deg_left)
        self.BP.set_motor_position_relative(self.right_motor, deg_right)

        # give motors some time to spin
        time.sleep(0.5)
        # read motor veloctiy until zero --> robot stands -> we can return from the function
        while self.BP.get_motor_status(self.left_motor)[3] != 0:
          time.sleep(0.02)

        self.update_position()

 
    def drive(self, distance):
        # needed motor rotation to achieve movement
        delta_angle = ((distance)*self.gear_ratio*360)/self.wheel_circumference
        # add angle to current motor position
        self.BP.set_motor_position_relative(self.left_motor, delta_angle)
        self.BP.set_motor_position_relative(self.right_motor, delta_angle)

        # give motors some time to spin
        time.sleep(0.5)
        # read motor veloctiy until zero --> robot stands -> we can return from the function
        while self.BP.get_motor_status(self.left_motor)[3] != 0:
           time.sleep(0.02)
 
        self.update_position()

   # To be implemented in 2.1
    def get_distance_front(self):
        try:
           # read sensor 
            distance = self.BP.get_sensor(self.front_sensor)
        except brickpi3.SensorError as error:
           # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")

        return distance

    # To be implemented in 2.1
    def get_color_left(self):
        try:
            color_index = self.BP.get_sensor(self.left_sensor)

           # Sözlükte bu index varsa rengi dön, yoksa "None" dön
            return self.colors.get(color_index, "None")
           #color = None #TODO Read in sensor
           # If brickpy sensor throws error set default value
        except brickpi3.SensorError as error:
            color = None # Default Value and print error
            print(f"Error during get_color_left(): {error}")

        return self.colors[color]

# To be implemented in 2.1    
    def get_color_right(self):
        try:
            color_index = self.BP.get_sensor(self.right_sensor)
 
# Sözlükte bu index varsa rengi dön, yoksa "None" dön
            return self.colors.get(color_index, "None")
#color = None #TODO Read in sensor
        except brickpi3.SensorError as error:
            color = None 
            print(f"Error during get_color_right(): {error}")

        return self.colors[color]


 ## Actor stuff

 # To be implemented in 2.3g
    def lift_fork(self,degree): # range 0-950
        self.move_fork(degree)


# To be implemented in 2.3
    def drop_fork(self,degree):
        self.move_fork(-degree)

# to be implemented in 2.3
    def move_fork(self,degree):
        # TODO Move fork motor
        # wait on the motor and check if it finished moving
        self.BP.set_motor_position_relative(self.fork_motor, degree)
        time.sleep(0.4)
        # read motor veloctiy until zero --> fork lift at position
        while self.BP.get_motor_status(self.fork_motor)[3] != 0:
           time.sleep(0.02)

    ## Higher level functions

## Followers:
    def follower_line(self, velocity=150):
       
        controller = PIController(kp=6, ki=0.2, target_value=20)

        while True:
            current_sensor_value = self.BP.get_sensor(self.right_sensor)
            u = controller.get_u(current_sensor_value)
           
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

            
            time.sleep(0.001)
            
            
    def follower_line_until_color(self, velocity, controller, target_color):
        """
        Sigue la línea negra usando el sensor derecho hasta que el 
        sensor izquierdo detecte el color especificado.
        """
        while True:
            # 1. Condición de parada: revisar el sensor izquierdo
            if self.get_color_left() == target_color:
                time.sleep(2)
                self.stop() # Detener los motores inmediatamente
                break       # Salir del bucle

            # 2. Leer el valor del sensor de línea (derecho)
            try:
                current_sensor_value = self.BP.get_sensor(self.right_sensor)
            except Exception as e:
                time.sleep(0.01)
                continue # Si hay un error de lectura, saltar este ciclo

            # 3. Calcular la corrección de dirección con el controlador PI
            u = controller.get_u(current_sensor_value)
 
            # 4. Limitar 'u' para no exceder los 500 DPS del motor
            if velocity + abs(u) > 500:
                if u >= 0:
                   u = 500 - velocity
                else:
                   u = velocity - 500

            # 5. Aplicar la velocidad a los motores
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

            time.sleep(0.01)


    def follower_distance(self, velocity):
        
        while True:
            time.sleep(0.1)
            dist_front = self.get_distance_front()
            print(dist_front)

            
           
            if dist_front <= 15:
                print("Obstacle detected")
                
                self.bypass_obstacle(velocity=120)
            else:
                controller = PIController(kp=4, ki=0.2, target_value=30.0)

                
            current_sensor_value = self.BP.get_sensor(self.right_sensor)
            u = controller.get_u(current_sensor_value)
           
            # Limit u
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500

            # Motorları u >= 0 ve < 0 mantığıyla çalıştır
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

            
            time.sleep(0.01)

    def bypass_obstacle(self, velocity=120):
       

        self.turn(90)
        self.BP.set_motor_dps(self.right_motor, 150)
        self.BP.set_motor_dps(self.left_motor, 150)
        time.sleep(1)
        
        working=True
        while working:
            
            controller = PIController(kp=5,ki=0.01, target_value=25.0)
            side_dist = self.get_distance_right()
            print(side_dist)
            
            if side_dist >= 200:
                u = 0
            else:
                u = controller.get_u(side_dist)


            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500
            
            

            if u >= 0:
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity - abs(u))
            
            else:
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
            
            black_or = self.BP.get_sensor(self.right_sensor)
            if self.is_black(black_or):
                print("Line detected, switching to line follower")
                self.stop()
                time.sleep(0.2)
                
                # Çizgiyi bulduktan sonra Kırmızı görene kadar takip etme mantığı:
                line_controller = PIController(kp=6, ki=0.2, target_value=30)
                while self.get_color_left() != "Red":
                    

        
                    current_sensor_value_1 = self.BP.get_sensor(self.right_sensor)
                    u_line = line_controller.get_u(current_sensor_value_1)
                    if u_line >= 0:
                        self.BP.set_motor_dps(self.right_motor, velocity - abs(u_line))
                        self.BP.set_motor_dps(self.left_motor, velocity + abs(u_line))
                    else:
                        self.BP.set_motor_dps(self.right_motor, velocity + abs(u_line))
                        self.BP.set_motor_dps(self.left_motor, velocity - abs(u_line))
                    time.sleep(0.01)
                
                if self.get_color_left()=="Red":
                    self.stop()
                    print("Red marker reached. Task finished.")
                    working=False
                    break # Bypass ve takip bitti


                
   

            time.sleep(0.01)
    
   # read and display the current voltages
    def print_battery_status(self):
        print("Battery voltage: %6.3f  9v voltage: %6.3f  5v voltage: %6.3f  3.3v voltage: %6.3f" % (self.BP.get_voltage_battery(), self.BP.get_voltage_9v(), self.BP.get_voltage_5v(), self.BP.get_voltage_3v3())) 

    def navigate_to_aruco_simple(self, camera, target_id=None, target_distance_cm=10, velocity=250, map_object=None):
        from FMLController import PController
        controller = PController(kp=1.5, target_value=0)
        last_save_time = time.time()
        snapshot_id=0
 
        while True:
            offset = camera.get_aruco_offset(target_id=target_id)
            front_distance = self.get_distance_front()

            # If the front_distance is less than 10 cm stop
            if(front_distance<10):
                self.stop()
                return 
        
            u = controller.get_u(offset)
            # Limit u to 500
            if velocity + abs(u) > 500:
                if u >= 0:
                   u = 500 - velocity
                else:
                   u = velocity - 500
             # Run motors
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor,velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor,velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity - abs(u))

            self.update_position()

            current_time = time.time()
            if current_time - last_save_time > 1:
                map_object.robot_position = (self.position[0] * 10, self.position[1] * 10)
                filename = f"map.png"
                map_object.save_map(filename)
                print(f"Saved {filename}")
                snapshot_id += 1
                last_save_time = current_time

            time.sleep(0.01)

        self.stop()

    def get_distance_right(self):
        distance = self.BP.get_sensor(self.side_sensor)

        return distance
    def is_black(self, sensor_value):
        BLACK_THRESHOLD=10
        return sensor_value <= BLACK_THRESHOLD


    def follower_qr_until_color(self, base_velocity, controller, camera, target_color):
        """
        Steers the robot to keep a QR code centered UNTIL a color sensor 
        detects target_color. Uses ultrasonic sensor to maintain safe distance.
        """
        not_red=True 
        
        while not_red:
            # 1. Stop Condition: Floor color
            if self.get_color_left() == target_color:
                self.stop()
                not_red=False
                return print("Red marker detected! Final position reached. --- Task 5 Complete ---")
                
            # 2. Get the visual offset using your NEW function name!
            offset = camera.get_qr_position_task5() 
            
            # 3. Handle lost QR code
            if offset is None:
                self.stop() 
                time.sleep(0.05)
                continue
                
            # 4. Calculate steering correction
            u = controller.get_u(offset)
            
            # 5. SAFETY CHECK: Check distance to worker using ultrasonic sensor
            dist_front = self.get_distance_front()
            
            # If worker is closer than 30cm (and sensor isn't glitching with -1)
            if dist_front != -1 and dist_front < 15:
                current_velocity = 0 # Stop moving forward!
            else:
                current_velocity = base_velocity # Keep moving forward
            
            # Limit the correction
            if current_velocity + abs(u) > 500:
                if u >= 0:
                   u = 500 - current_velocity
                else:
                   u = current_velocity - 500
                   
            # 6. Apply speeds (forward velocity + steering)
            if u >= 0:
                self.BP.set_motor_dps(self.left_motor, current_velocity + abs(u))
                self.BP.set_motor_dps(self.right_motor, current_velocity - abs(u))
            else:
                self.BP.set_motor_dps(self.left_motor, current_velocity - abs(u))
                self.BP.set_motor_dps(self.right_motor, current_velocity + abs(u))
                
            time.sleep(5)