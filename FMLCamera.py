# from picamera2 import Picamera2
# import numpy as np
# import cv2
# import pyzbar.pyzbar as pyzbar
# import time

# class FMLCamera:

#     def __init__(self):
#         self.resolution = (800,400) # rows x columns
#         self._pi_camera = Picamera2()
#         self._pi_camera.framerate = 10
#         self._pi_camera.resolution=self.resolution
#         self._pi_camera.start()
#         # make shure camera is up and awake
#         time.sleep(2)

    
#     # Destructor (gets called once the object is destroyed)
#     def __del__(self):
#         # Frees ressources connected to the camera
#         self._pi_camera.close() 
    
#     # Return a array as a image just a in 06-perception
#     def get_image_array(self):
#         frame = self._pi_camera.capture_array("main")
#         frame_bgr = frame[..., ::-1]
#         return frame_bgr

#     # saves a image to disk - probably usefull for the shape recognition.
#     def save_to_disk(self, path_to_image):
#         self._pi_camera.capture(path_to_image)


#     # the following function only provide hints on what could be done using the FMLCamera class. 
#     # Feel free to implement things differently. 

#     # return the parsed barcode thats directly in front of the roboter (takes image -> processes it -> return the result)
#     def get_qr_data(self):
#         import cv2
#         from pyzbar import pyzbar

#         # 1. Capture the image
#         image = self.get_image_array()
        
#         # 2. Pre-process to fix blur/tint issues
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Thresholding: pixels darker than 100 become black, others white
#         _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
#         # 3. Decode
#         decoded_objects = pyzbar.decode(thresh)
        
#         for obj in decoded_objects:
#             # Return the string data if a QR code is found
#             if obj.type == 'QRCODE':
#                 return obj.data.decode('utf-8')
                
#         return None

#     def is_green(self):
#         image = self.get_image_array()
#         if image is None:
#             return False

#         # Debug: Ne gördüğünü kaydetmeye devam et
#         cv2.imwrite("camera_debug.jpg", image)

#         hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#         # IŞIK İÇİN EN AGRESİF ARALIK:
#         # H: 30-100 (Yeşil tonları)
#         # S: 2-255 (Işık o kadar parlaktır ki neredeyse beyaz görünür, 2 yaparak bunu yakalıyoruz)
#         # V: 150-255 (Sadece çok parlak olan şeylere bak, karanlık yeşilleri görmezden gel)
#         lower_green = np.array([30, 2, 150]) 
#         upper_green = np.array([100, 255, 255])
        
#         mask = cv2.inRange(hsv, lower_green, upper_green)

#         # Görüntüyü dikey olarak 3'e böl (Sol, Orta, Sağ)
#         height, width = mask.shape
#         third = width // 3
        
#         left_zone = mask[:, :third]
#         mid_zone = mask[:, third:2*third]
#         right_zone = mask[:, 2*third:]

#         # Her bölgedeki pikseli say
#         p_left = cv2.countNonZero(left_zone)
#         p_mid = cv2.countNonZero(mid_zone)
#         p_right = cv2.countNonZero(right_zone)

#         total_pixels = p_left + p_mid + p_right
        
#         if total_pixels > 10: # 10 piksel bile yeterli
#             print(f"IŞIK YAKALANDI! Sol: {p_left}, Orta: {p_mid}, Sağ: {p_right}")
#             return True
            
#         return False

#     """
#     def is_green(self):
#         image = self.get_image_array()
#         if image is None:
#             print("KRİTİK HATA: Kamera görüntü yakalayamıyor!")
#             return False

#         # Robotun ne gördüğünü dosyaya kaydet (Sol menüden kontrol et)
#         # Eğer bu resim tamamen siyahsa kamera donmuştur.
#         cv2.imwrite("camera_test.jpg", image) 

#         hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
#         # Işık çok parlaksa beyaza döner, bu yüzden doygunluğu (S) 5'e kadar indirdik.
#         lower_green = np.array([30, 5, 50]) 
#         upper_green = np.array([100, 255, 255])
#         mask = cv2.inRange(hsv, lower_green, upper_green)
        
#         green_pixels = cv2.countNonZero(mask)
#         print(f"DEBUG -> Yesil Piksel Sayisi: {green_pixels}")

#         return green_pixels > 20 
#     """


#     def get_green_percentage(self):
#         image = self.get_image_array()
        
#         # Kanalları ayır (RGB)
#         red_ch = image[:,:,0]
#         green_ch = image[:,:,1]
#         blue_ch = image[:,:,2]

#         avg_red = np.mean(red_ch)
#         avg_green = np.mean(green_ch)
#         avg_blue = np.mean(blue_ch)

#         # Mantık: Yeşil hem belli bir parlaklıkta olmalı 
#         # hem de diğer renklerden en az 20 birim daha fazla olmalı.
#         if avg_green > 60 and avg_green > (avg_red + 20) and avg_green > (avg_blue + 20):
#             return 100  # Yeşil var kabul et
        
#         return 0 # Yeşil yok



#     # returns a list of shapes recognized in the picture. The image is provided via a path saved to harddisk (mainly because image resultion is higher this way)
#     # (load picture -> process it -> generate list of shapes -> return them)
#     def get_shapes_on_image(self,path_to_image):
#         pass

#     # Return the offset of the centerpoint of the barcode relative to the center of the camera view. 
#     # But here its really open to you what you want to control with the P-PI Controller. 
#     # Remind yourself that you can get the position of a barcode also from the Scanner() lib.
#     def get_qr_position(self):
#         pass

#     def get_aruco_offset(self, target_id=None):
#         import cv2.aruco as aruco
#         image = self.get_image_array()
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
#         parameters = aruco.DetectorParameters_create()

#         corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

#         if ids is None:
#             return 0
        
        
#         for i, marker_id in enumerate(ids):

#         # doğru markerı seç
#             if target_id is None or marker_id[0] == target_id:

#                 c = corners[i][0]

#                 # marker center
#                 center_x = (c[0][0] + c[2][0]) / 2

#                 # image center
#                 image_center_x = image.shape[1] / 2

#                 offset = center_x - image_center_x

#                 print("Detected ArUco:", marker_id[0])
#                 print("Offset:", offset)

#                 return offset

      
#             ## Calculate the offset between the camera center and the Aruco center in the x axis
#             ## Return the offset calculated
#             ## If the offset is positive it means that the Aruco is to the right of the robot
#             ## If the offset is negative it means that the Aruco is to the left
#     def is_green_detected(self):
#         # Kameradan anlık kareyi al
#         image = self.get_image_array()
#         # Renk algılama için HSV formatına çevir
#         hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
#         # Yeşil renk aralığı (H: 35-85 arası yeşildir)
#         lower_green = np.array([35, 50, 50])
#         upper_green = np.array([85, 255, 255])
        
#         # Görüntüde sadece yeşil olan yerleri beyaz yap
#         mask = cv2.inRange(hsv, lower_green, upper_green)
        
#         # Belirli bir piksel sayısının (örn: 500) üzerinde yeşil varsa 'True' dön
#         if cv2.countNonZero(mask) > 500:
#             return True
#         return False
    

from picamera2 import Picamera2
# from picamera.array import PiRGBArray
import numpy as np
import cv2
# import zbar
import pyzbar.pyzbar as pyzbar
import time

class FMLCamera:

    def __init__(self):
        self.resolution = (800,400) # rows x columns
        self._pi_camera = Picamera2()
        self._pi_camera.framerate = 30
        self._pi_camera.resolution=self.resolution
        config = self._pi_camera.create_still_configuration(main={"size": self.resolution})
        self._pi_camera.configure(config)
        self._pi_camera.start()
        # make shure camera is up and awake
        time.sleep(1)

    
    # Destructor (gets called once the object is destroyed)
    def __del__(self):
        # Frees ressources connected to the camera
        self._pi_camera.close() 
    

    def get_image_array(self):
        frame = self._pi_camera.capture_array("main")
        frame_bgr = frame[..., ::-1]
        return frame_bgr

    def save_to_disk(self, path_to_image):
        self._pi_camera.capture_file(path_to_image)


    # to be implemented during challenge using knowledge from 06
    def get_barcode(self):
        image_taken = self.get_image_array()
        image_in_gray = cv2.cvtColor(image_taken, cv2.COLOR_BGR2GRAY)
        # scanner = zbar.Scanner()
        results = pyzbar.decode(image_in_gray)
        if len(results) == 0:
            return None
        else:
            # return first element
            return results[0].data.decode("utf-8")
               
    # to be implemented during challenge using knowledge from 06
    def get_green_percentage(self):
        image_taken = self.get_image_array()
        # convert to hsv image
        hsv_image = cv2.cvtColor(image_taken,cv2.COLOR_BGR2HSV)
        # mask the image with bools if pixel counts as green
        greens = np.logical_and(hsv_image[:,:,0] > 45, hsv_image[:,:,0] < 60)
        #count them
        number_of_greens = np.count_nonzero(greens)
        
        return number_of_greens / (self.resolution[0]*self.resolution[1])

    # to be implemented during challenge using knowledge from 06
    def get_shapes_on_image(self,path_to_image):
        img = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
        #create picture is just white and black based on predefined threshold (here: 80)
        unknown_threshold, threshold = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
        contours, unknown_contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Initially no shapes in image
        shapes_in_image = []

        for countour in contours:
        # form is determined using the number of corners of the form
            edges = cv2.approxPolyDP(countour, 0.01 * cv2.arcLength(countour, True), True)
            
            if len(edges) == 3:
                shapes_in_image.append("Triangle")

            elif len(edges) == 4:
                shapes_in_image.append('Rectangle')

            elif len(edges) == 5:
                shapes_in_image.append('Pentagon')

            elif 6 < len(edges) < 15:
                shapes_in_image.append('Ellipse')

            else:
                shapes_in_image.append('Circle')
        
        return shapes_in_image

    def get_qr_position(self):
        image_taken = self.get_image_array()
        #results contains one element per detected barcode
        image_in_gray = cv2.cvtColor(image_taken, cv2.COLOR_BGR2GRAY)
        results = pyzbar.decode(image_in_gray)
        # results = scanner.scan(image_in_gray)
        if not results:
            return "No Barcode"
    
        # ans = results[0].rect
        x, y, w, h = results[0].rect
        x_center = x + w / 2
        offset = x_center - (self.resolution[0] / 2)
        return offset
    
    def get_qr_position_task5(self):
        import pyzbar.pyzbar as pyzbar
        
        image = self.get_image_array()
        barcodes = pyzbar.decode(image)
        
        if not barcodes:
            return None # No QR code seen
            
        # Get the first barcode detected
        barcode = barcodes[0]
        
        # Extract the bounding box dimensions
        (x, y, w, h) = barcode.rect
        
        # Calculate where the center of the QR code is
        qr_center_x = x + (w / 2.0)
        
        # Center of the camera resolution (800 / 2 = 400)
        image_center_x = self.resolution[0] / 2.0
        
        # Calculate offset (positive means right, negative means left)
        offset = qr_center_x - image_center_x
        
        # Return the numerical pixel offset!
        return offset
    
    def get_shape(self):
        """
        Capture current frame and detect shapes in it.
        Return the first detected shape, or None if no shapes.
        """
        image = self.get_image_array()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            edges = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            if len(edges) == 3:
                return "Triangle"
            elif len(edges) == 4:
                return "Rectangle"
            elif len(edges) == 5:
                return "Pentagon"
            elif 6 < len(edges) < 15:
                return "Circle"
        return None

    def get_aruco_offset(self, target_id=None):
        import cv2.aruco as aruco
        image = self.get_image_array()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
        parameters = aruco.DetectorParameters_create()

        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is None:
            return 0

        for i, marker_id in enumerate(ids.flatten()):
            if target_id is None or marker_id == target_id:
                # corners[i] has shape (1, 4, 2), calculate center x
                marker_corners = corners[i][0]
                center_x = np.mean(marker_corners[:, 0])
                image_center_x = self.resolution[0] / 2
                offset = center_x - image_center_x
                print(f"ArUco ID {marker_id} detected, offset: {offset:.1f}px")
                return offset

        # target marker not found
        return 0
    
    def wait_for_shape(self, target_shape, display=False):
        print(f"Waiting for shape: {target_shape}")

        while True:
            # 1. Get image using self (Fixing the missing camera parameter issue)
            image = self.get_image_array()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply slightly stronger blur to smooth jagged edges (5,5) -> (7,7)
            gray = cv2.GaussianBlur(gray, (7, 7), 0) 

            # 2. Threshold (OTSU)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 3. Contours - RETR_EXTERNAL prevents reading internal noise as separate shapes
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Ignore small noise and prevent the entire camera frame from being read as a rectangle
                if area < 1500 or area > 100000: 
                    continue

                # 4. INCREASED EPSILON: 0.04 makes approximation less sensitive to edge noise
                epsilon = 0.04 * cv2.arcLength(contour, True)
                edges = cv2.approxPolyDP(contour, epsilon, True)

                shape = None
                
                # 5. Shape Detection
                if len(edges) == 3:
                    shape = "Triangle"
                elif len(edges) == 4:
                    shape = "Rectangle"
                elif len(edges) == 5:
                    shape = "Pentagon"
                elif len(edges) > 5:
                    shape = "Circle"

                # 6. Return if target found
                if shape == target_shape:
                    print(f"Detected target shape: {shape}")
                    if display:
                        cv2.imshow("Shape Found", image)
                        cv2.waitKey(1000)
                        cv2.destroyAllWindows()
                    return shape
                    
            # Prevent CPU overloading during the while True loop
            time.sleep(0.05)

    def get_stable_shape(self, duration=2.5):
        import collections
        import time
        import cv2
        
        found_shapes = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            image = self.get_image_array()
            # 1. Gri tonlama ve Blur
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            
            # 2. THRESH_BINARY_INV Çok Kritik! 
            # Beyaz kağıdı siyah, içindeki siyah şekli beyaz yapar. 
            # Böylece RETR_EXTERNAL doğrudan içteki şekle odaklanır.
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # 3. ALAN SINIRLAMASI (En önemli kısım)
                # Eğer alan çok büyükse (örn > 90000), bu muhtemelen kamera çerçevesidir.
                # Eğer çok küçükse (örn < 3000), bu gürültüdür.
                if area < 3000 or area > 85000:
                    continue
                
                # 4. Köşe Hassasiyeti (Epsilon)
                # %4.5 (0.045) değeri dikdörtgen kenarlarındaki pürüzleri siler.
                epsilon = 0.045 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                num_edges = len(approx)
                
                if num_edges == 3:
                    found_shapes.append("Triangle")
                elif num_edges == 4:
                    found_shapes.append("Rectangle")
                elif num_edges > 5:
                    found_shapes.append("Circle")
            
            time.sleep(0.02)
        
        if not found_shapes:
            return None

        # Oylama sonucu en çok tekrar eden şekli döndür
        decision = collections.Counter(found_shapes).most_common(1)[0][0]
        return decision