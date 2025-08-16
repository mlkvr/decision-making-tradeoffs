import carla
import global_data
import numpy as np

SPEED_LIMIT = 50.0
MIN_BRAKING_DISTANCE = 10.0
BRAKING_DISTANCE_FACTOR = 0.6

def calculate_dynamic_braking_distance(speed_kmh):
    return max(MIN_BRAKING_DISTANCE, speed_kmh * BRAKING_DISTANCE_FACTOR)

def get_pedestrian_distance_from_lidar(lidar_points):
    if len(lidar_points) == 0:
        return float('inf')

    points = lidar_points[:, :3]
    forward_points = points[(points[:, 0] > 0)]

    if len(forward_points) == 0:
        return float('inf')

    distances = np.linalg.norm(forward_points, axis=1)
    min_distance = np.min(distances)

    return min_distance

def process_decision(ego_vehicle, lidar_data_points):
    velocity = ego_vehicle.get_velocity()
    current_speed = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
    dynamic_braking_distance = calculate_dynamic_braking_distance(current_speed)

    pedestrian_distance = get_pedestrian_distance_from_lidar(lidar_data_points)

    print(f"Araç Hızı: {current_speed:.2f} km/h, Fren Mesafesi: {dynamic_braking_distance:.2f} m")
    print(f"LIDAR ile ölçülen gerçek yaya mesafesi: {pedestrian_distance:.2f} m")

    if pedestrian_distance < dynamic_braking_distance:
        print(f"Tehlike! Yayaya mesafe {pedestrian_distance:.2f} m. Fren yapılıyor.")
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
    elif current_speed > SPEED_LIMIT:
        print("Hız limiti aşıldı, hız düşürülüyor!")
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.3))
    else:
        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
