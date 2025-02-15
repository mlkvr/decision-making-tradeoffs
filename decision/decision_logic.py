import time
import carla
import cv2
from .pedestrian_detector import detect_pedestrians, pedestrian_in_path
import global_data

def estimate_distance(bbox_width, actual_width=0.6, focal_length=400):
    if bbox_width == 0:
        return float('inf')
    return (actual_width * focal_length) / bbox_width

def process_decision(ego_vehicle):
    computation_time = 1.0  # seconds
    start_time = time.time()
    
    pedestrian_detected = False
    braking_distance_threshold = 15.0  # Only brake if pedestrian is closer than 15 m
    
    while time.time() - start_time < computation_time:
        if global_data.last_camera_image is not None:
            detections = detect_pedestrians(global_data.last_camera_image, conf_threshold=0.3)
            image_width = global_data.last_camera_image.shape[1]
            # Instead of simply checking if a pedestrian is in path,
            # check the estimated distance for each detection.
            for det in detections:
                x, y, w, h = det["bbox"]
                est_distance = estimate_distance(w)
                print(f"Estimated distance: {est_distance:.2f} m (bbox width: {w})")
                # You can also check if the detection is in the central region if desired:
                if est_distance < braking_distance_threshold:
                    pedestrian_detected = True
                    break
            if pedestrian_detected:
                break
        else:
            print("No frame available yet.")
        time.sleep(0.1)

    if pedestrian_detected:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
        print("Emergency braking applied!")
    else:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
        print("Continuing on path.")
