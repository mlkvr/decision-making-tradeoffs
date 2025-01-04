import carla
import numpy as np
import cv2
import os
from datetime import datetime

# Kameradan gelen son görüntüyü saklamak için bir değişken
last_camera_image = None
image_save_directory = None  # Görüntülerin kaydedileceği dinamik klasör
image_counter = 0  # Her görüntüye farklı bir isim vermek için sayaç

def setup_save_directory():
    global image_save_directory
    # Simülasyon başlangıcında tarih/saat bilgisiyle bir klasör oluştur
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_save_directory = os.path.join("camera_outputs", f"simulation_{timestamp}")
    os.makedirs(image_save_directory, exist_ok=True)

def process_image(image):
    global last_camera_image, image_counter

    # Görüntü verilerini numpy array'e dönüştür
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    last_camera_image = array[:, :, :3]  # Son görüntüyü RGB formatında kaydet

    # OpenCV ile görüntüyü göster
    cv2.imshow('Camera View', last_camera_image)
    cv2.waitKey(1)

    # Görüntüyü dosyaya kaydet
    if image_save_directory is not None:
        file_name = os.path.join(image_save_directory, f"frame_{image_counter:06d}.png")
        cv2.imwrite(file_name, last_camera_image)
        image_counter += 1

def attach_camera(world, ego_vehicle):
    global process_image, setup_save_directory

    # Kamera blueprint'ini oluştur
    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')

    # Kamera özelliklerini ayarla
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')

    # Kamerayı yerleştirme noktası
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

    # Görüntüleri kaydetmek için klasör oluştur
    setup_save_directory()

    # Kameradan gelen verileri dinleme
    camera.listen(process_image)  # Kamerayı dinlemeye başla
    return camera
