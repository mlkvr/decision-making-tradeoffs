import time
import carla
from sensors.camera import process_image,last_camera_image

def process_decision(ego_vehicle, walker):
    print("decision_logic.py successfuly called")
    global last_camera_image
    computation_time = 0.5
    start_time = time.time()
    
    # Varsayılan değer atanıyor
    pedestrian_detected = False

    while time.time() - start_time < computation_time:
        if last_camera_image is not None:
            pedestrian_detected = process_image(last_camera_image)
            if pedestrian_detected:
                break

    if pedestrian_detected:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
        print("Emergency braking applied!")
    else:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
        print("Continuing on path.")



