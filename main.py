import carla
import cv2
from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker, compute_jaywalk_waypoints
from decision.decision_logic import process_decision
from sensors.camera import attach_camera

def main():
    global ego_vehicle, walker, walker_controller, camera

    try:
        # Set up CARLA client, world, and blueprint library
        client, world, blueprint_library = setup_carla_client()

        # Spawn the ego vehicle
        ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
        if ego_vehicle is None:
            print("Error: Ego vehicle could not be spawned!")
            return

        # Spawn the pedestrian (walker)
        walker = spawn_walker(world, blueprint_library)
        if walker is None:
            print("Error: Walker could not be spawned!")
            return

        # Optionally, start the walker controller briefly for natural animations, then disable it.
        walker_controller_bp = blueprint_library.find('controller.ai.walker')
        walker_controller = world.try_spawn_actor(walker_controller_bp, carla.Transform(), attach_to=walker)
        if walker_controller is not None:
            walker_controller.start()
            # Let it run briefly to play natural animations
            for _ in range(10):
                world.tick()
            walker_controller.stop()
            walker_controller.destroy()
            walker_controller = None
            print("Walker controller disabled before forcing path.")

        # Compute a series of waypoints for jaywalking.
        start_location = walker.get_location()
        waypoints = compute_jaywalk_waypoints(start_location, num_waypoints=10, step_distance=1.0, lateral_offset=10.0)

        # Attach a camera to the ego vehicle
        camera = attach_camera(world, ego_vehicle)
        if camera is None:
            print("Error: Camera could not be attached!")
            return

        # Simulation loop: update both the walker and the car concurrently.
        current_waypoint_index = 0
        tick_counter = 0
        tick_delay = 1  # update the walker position every tick_delay ticks
        running = True

        while running:
            world.tick()
            tick_counter += 1

            # If there are still waypoints left for the walker, update its position gradually.
            if current_waypoint_index < len(waypoints) and tick_counter % tick_delay == 0:
                # Force the walker to the next waypoint using set_transform (updates both location and rotation)
                new_transform = carla.Transform(
                    location=waypoints[current_waypoint_index],
                    rotation=walker.get_transform().rotation
                )
                walker.set_transform(new_transform)
                print(f"Walker forced to waypoint {current_waypoint_index+1}: {waypoints[current_waypoint_index]}")
                current_waypoint_index += 1

            # Process decision logic concurrently (using sensor data)
            process_decision(ego_vehicle)

            # Check for exit condition (press 'q' in the OpenCV window)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting simulation via 'q'.")
                running = False

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Clean up actors and resources.
        if ego_vehicle is not None:
            ego_vehicle.destroy()
            print("ego_vehicle destroyed")
        if walker is not None:
            walker.destroy()
            print("walker destroyed")
        if camera is not None:
            camera.stop()
            camera.destroy()
            print("camera destroyed")
        print("Actors cleaned up. Simulation ended.")

if __name__ == '__main__':
    main()
