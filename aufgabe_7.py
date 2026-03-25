import sys
import time
import os

# Kütüphane yollarını ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("..")
sys.path.append(".")

from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt



def doTask(robot, camera, target_shape="Circle"):
    
    velocity=200
    found_correct_station = False
   

    print(f"Görev Başladı: {target_shape} aranıyor...")
    
   
    # --- FAZ 1: DOĞRU İSTASYONU BULANA KADAR ARA ---
    while not found_correct_station:
        line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
        # Şerit Takibi
        current_sensor_val = robot.BP.get_sensor(robot.right_sensor)
        u = line_controller.get_u(current_sensor_val)
        robot.BP.set_motor_dps(robot.left_motor, velocity + u)
        robot.BP.set_motor_dps(robot.right_motor, velocity - u)
        
        # Mavi Marker Kontrolü
        if robot.get_color_left() == "Blue":
            time.sleep(1)
            robot.stop()
            print("Mavi marker bulundu, kontrol ediliyor...")
            
            # Hizalanma ve Fotoğraf Çekme
            robot.turn(-90)
            time.sleep(1) # Titreşimin geçmesi için bekle

            detected = camera.get_stable_shape(duration=3.0)
            print(f"Analiz sonucu: {detected}")
            
        

            # Eğer listenin içinde hedef şeklimiz varsa
            if detected==target_shape:
                print(f" {target_shape} istasyonuna paket bırakılıyor.")
                # Paket bırakma manevrası
                
                robot.lift_fork(750)
                time.sleep(1)
                
                robot.drop_fork(750)
                
                robot.turn(90)
                found_correct_station = True 

            else:
                print("look next")
                robot.turn(90)
                # Aynı markerı bir daha algılamamak için biraz ileri git
                
                FMLRobot.drive(robot, 0.05)
            
                detected=None

            

        time.sleep(0.1)

    # --- FAZ 2: HİÇBİR ŞEYE BAKMADAN KIRMIZIYA GİT ---
    print("İstasyon bulundu. Şimdi sadece kırmızı bitiş çizgisi bekleniyor...")

    line_controller = PIController(kp = 4, ki = 0, target_value = 30.0)
    not_Red=False
    while not not_Red:
        # Şerit takibine devam
        current_sensor_val = robot.BP.get_sensor(robot.right_sensor)
        u = line_controller.get_u(current_sensor_val)
        robot.BP.set_motor_dps(robot.left_motor, velocity + u)
        robot.BP.set_motor_dps(robot.right_motor, velocity - u)

        # Sadece Kırmızı Kontrolü (Maviler artık görmezden geliniyor)
        if robot.get_color_left() == "Red" :
            robot.stop()
            not_Red=True
            
            

