import carla
from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker, compute_jaywalk_waypoints, force_jaywalk_path
from decision.decision_logic import process_decision
from sensors.camera import attach_camera
import cv2

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

        # Optionally, you can spawn and start the walker controller to get natural animations.
        # However, if the navigation mesh prevents the walker from going out of bounds,
        # the controller may override your destination. In this approach, we use it briefly
        # for animation, then force the path manually.
        walker_controller_bp = blueprint_library.find('controller.ai.walker')
        walker_controller = world.try_spawn_actor(walker_controller_bp, carla.Transform(), attach_to=walker)
        if walker_controller is not None:
            walker_controller.start()
        else:
            print("Warning: Walker controller could not be spawned!")
            walker_controller = None

        # Compute a series of waypoints for jaywalking.
        # Use the walker's current location as the starting point.
        start_location = walker.get_location()
        waypoints = compute_jaywalk_waypoints(start_location, num_waypoints=15, step_distance=1.0, lateral_offset=10.0)

        if walker_controller is not None:
            walker_controller.stop()
            walker_controller.destroy()
            walker_controller = None
            print("Walker controller disabled before forcing path.")

       
        # Optionally, attach a camera to the ego vehicle.
        camera = attach_camera(world, ego_vehicle)
        if camera is None:
            print("Error: Camera could not be attached!")
            return

        # Process decision logic, etc.
        process_decision(ego_vehicle, walker)

         # Force the walker along the computed jaywalking path.
        force_jaywalk_path(world, walker, waypoints, tick_delay=10)

        # Run the simulation loop; here we wait until the user presses 'q' to exit.
        running = True
        while running:
            world.tick()
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
        if walker_controller is not None:
            walker_controller.stop()
            walker_controller.destroy()
            print("walker_controller destroyed")
        if camera is not None:
            camera.stop()
            camera.destroy()
            print("camera destroyed")
        print("Actors cleaned up. Simulation ended.")

if __name__ == '__main__':
    main()
