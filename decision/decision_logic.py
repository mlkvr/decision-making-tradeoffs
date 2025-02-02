import time
import carla
import cv2
from .pedestrian_detector import detect_pedestrians, pedestrian_in_path
import global_data  # Import the module itself

def process_decision(ego_vehicle):
    # No need for a local "global last_camera_image" declaration anymore.
    computation_time = 1.0  # seconds
    start_time = time.time()
    
    pedestrian_detected = False

    while time.time() - start_time < computation_time:
        # Access the shared variable via the module.
        if global_data.last_camera_image is not None:
            detections = detect_pedestrians(global_data.last_camera_image, conf_threshold=0.3)
            print(f"Detections: {detections}")
            image_width = global_data.last_camera_image.shape[1]
            if pedestrian_in_path(detections, image_width, central_fraction=1.0):
                pedestrian_detected = True
                break
        else:
            print("No frame available yet.")
        time.sleep(0.1)  # Give a brief delay

    if pedestrian_detected:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
        print("Emergency braking applied!")
    else:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
        print("Continuing on path.")
