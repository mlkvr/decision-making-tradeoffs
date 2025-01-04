import carla
import numpy as np
import cv2

# Kameradan gelen son görüntüyü saklamak için bir değişken
last_camera_image = None

def process_image(image):
    global last_camera_image
    # Görüntü verilerini numpy array'e dönüştür
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    last_camera_image = array[:, :, :3]  # Son görüntüyü RGB formatında kaydet
    cv2.imshow('Camera View', last_camera_image)
    cv2.waitKey(1)

def attach_camera(world, ego_vehicle):
    global process_image  # Callback fonksiyonunu global olarak tanımla

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

    # Kameradan gelen verileri dinleme
    camera.listen(process_image)  # Kamerayı dinlemeye başla
    return camera
