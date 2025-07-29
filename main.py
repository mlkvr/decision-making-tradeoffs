import carla
import global_data
from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker, compute_jaywalk_waypoints
from sensors.camera import attach_camera
from utils.deepseek_integration import run_deepseek_decision

def main():
    global ego_vehicle, walker, walker_controller, camera

    client, world, blueprint_library = setup_carla_client()

    # Senkron moda geç
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
    if ego_vehicle is None:
        print("Error: Ego vehicle could not be spawned!")
        return

    walker = spawn_walker(world, blueprint_library)
    if walker is None:
        print("Error: Walker could not be spawned!")
        return

    walker_controller_bp = blueprint_library.find('controller.ai.walker')
    walker_controller = world.try_spawn_actor(walker_controller_bp, carla.Transform(), attach_to=walker)
    if walker_controller:
        walker_controller.start()
        for _ in range(10): world.tick()
        walker_controller.stop()
        walker_controller.destroy()
        walker_controller = None
        print("Walker controller disabled before forcing path.")

    waypoints = compute_jaywalk_waypoints(walker.get_location(), num_waypoints=10, step_distance=1.0, lateral_offset=10.0)
    camera = attach_camera(world, ego_vehicle)
    if camera is None:
        print("Error: Camera could not be attached!")
        return

    current_waypoint_index = 0
    tick_counter = 0
    tick_delay = 1
    running = True

    print("\n--- Manuel tick mode aktif! Devam etmek için Enter, çıkmak için q+Enter ---")
    try:
        while running:
            user_input = input("Devam etmek için Enter'a bas, çıkmak için q+Enter: ")
            if user_input.lower() == 'q':
                print("Exiting simulation via 'q'.")
                running = False
                break

            # Karar mantığı
            description = "A pedestrian is crossing in front of the car."
            print("LLava description:", description)

            decision = run_deepseek_decision(description)
            if decision == "brake":
                ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
                print("Emergency braking applied!")
            elif decision == "accelerate":
                ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
                print("Accelerating...")
            else:
                ego_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))
                print("Continuing on path.")

            world.tick()
            tick_counter += 1

            if current_waypoint_index < len(waypoints) and tick_counter % tick_delay == 0:
                new_transform = carla.Transform(location=waypoints[current_waypoint_index], rotation=walker.get_transform().rotation)
                walker.set_transform(new_transform)
                print(f"Walker forced to waypoint {current_waypoint_index+1}: {waypoints[current_waypoint_index]}")
                current_waypoint_index += 1

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting...")
    finally:
        settings = world.get_settings()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        if ego_vehicle: ego_vehicle.destroy(); print("ego_vehicle destroyed")
        if walker: walker.destroy(); print("walker destroyed")
        if camera: camera.stop(); camera.destroy(); print("camera destroyed")
        print("Actors cleaned up. Simulation ended.")

if __name__ == '__main__':
    main()
