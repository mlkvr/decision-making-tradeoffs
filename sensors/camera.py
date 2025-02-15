import carla
import numpy as np
import cv2
import os
from datetime import datetime
from global_data import last_camera_image 

image_save_directory = None  # Görüntülerin kaydedileceği dinamik klasör
image_counter = 0  # Her görüntüye farklı bir isim vermek için sayaç

def setup_save_directory():
    global image_save_directory
    # Simülasyon başlangıcında tarih/saat bilgisiyle bir klasör oluştur
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_save_directory = os.path.join("camera_outputs", f"simulation_{timestamp}")
    os.makedirs(image_save_directory, exist_ok=True)

def process_image(image):
    global last_camera_image
    # Convert the raw data to a numpy array.
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    # Convert BGRA to BGR
    # Update the shared variable. If using module-level, do:
    #    global_data.last_camera_image = array[:, :, :3]
    # If you imported it directly, reassigning might not update the module variable.
    # It's better to import the module and then update its attribute.
    import global_data
    global_data.last_camera_image = array[:, :, :3]
    
    cv2.imshow("Camera View", array[:, :, :3])
    cv2.waitKey(1)


def attach_camera(world, vehicle):
    global process_image, setup_save_directory

    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')

    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

    setup_save_directory()  # Create the folder for saving images.
    camera.listen(process_image)
    return camera

