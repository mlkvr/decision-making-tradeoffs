import carla
import numpy as np

last_camera_image = None

def attach_camera(world, blueprint_library, ego_vehicle):
    global last_camera_image
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

    def callback(image):
        global last_camera_image
        last_camera_image = image

    camera.listen(callback)
    return camera

def process_image(image):
    # Görüntüyü numpy formatına çevir
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))  # RGBA formatında

    # Yaya tespiti için basit bir renk filtresi
    pedestrian_color_range = [(100, 0, 0), (255, 50, 50)]  # Örnek renk aralığı
    mask = (array[:, :, 0] > pedestrian_color_range[0][0]) & \
           (array[:, :, 0] < pedestrian_color_range[1][0]) & \
           (array[:, :, 1] > pedestrian_color_range[0][1]) & \
           (array[:, :, 1] < pedestrian_color_range[1][1])

    # Tespit edilen yaya varsa, lokasyonunu döndür
    if mask.any():
        print("Pedestrian detected!")
        return True
    return False

