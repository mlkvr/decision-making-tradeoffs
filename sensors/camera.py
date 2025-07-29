import global_data
import carla
import numpy as np

def attach_camera(world, ego_vehicle):
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera_bp.set_attribute("image_size_x", "640")
    camera_bp.set_attribute("image_size_y", "480")
    camera_bp.set_attribute("fov", "90")

    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

    def save_image(image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((image.height, image.width, 4))[:, :, :3]  # BGR
        global_data.last_camera_image = array
        global_data.last_image_timestamp = image.timestamp

    camera.listen(lambda image: save_image(image))
    return camera
