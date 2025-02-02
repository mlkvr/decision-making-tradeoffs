import carla
import math

global isWalked

def spawn_walker(world, blueprint_library):
    """
    Spawns a walker at a location relative to the ego vehicle spawn point.
    The walker is spawned 100 meters ahead with a fixed orientation.
    """
    try:
        print("walker.py successfully called")
        # Choose a pedestrian blueprint (select one at random)
        walker_bp = blueprint_library.filter('walker.pedestrian.*')[0]
        
        # Get a spawn point from the map (for example, the first one)
        ego_vehicle_spawn_point = world.get_map().get_spawn_points()[0]
        
        # Set the walker spawn point 100 meters ahead of the ego vehicle,
        # with a fixed rotation (here 270° so that it faces perpendicular to the road)
        walker_spawn_point = carla.Transform(
            carla.Location(
                x=ego_vehicle_spawn_point.location.x + 86,  # 100 meters ahead
                y=ego_vehicle_spawn_point.location.y + 10,
                z=ego_vehicle_spawn_point.location.z
            ),
            carla.Rotation(pitch=0.0, yaw=270.0, roll=0.0)
        )
        
        # Optionally, visualize the spawn location for debugging
        world.debug.draw_string(
            walker_spawn_point.location,
            "Walker Spawn Point",
            draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0),
            life_time=5.0,
            persistent_lines=True
        )
        
        walker = world.try_spawn_actor(walker_bp, walker_spawn_point)
        if walker is None:
            print("Error: Walker could not be spawned!")
        else:
            print("Walker spawned successfully.")
        return walker
    except Exception as e:
        print(f"Error while spawning walker: {e}")
        return None


def compute_jaywalk_waypoints(start_location, num_waypoints=5, step_distance=2.0, lateral_offset=10.0):
    """
    Computes a list of waypoints for a jaywalking pedestrian.
    In this example, the walker will be forced to cross laterally (across the road)
    from its start_location. You can adjust the values to simulate a realistic crossing.
    
    Parameters:
      start_location: carla.Location object representing the start position.
      num_waypoints: number of waypoints to generate.
      step_distance: forward movement (along the original heading) per waypoint.
      lateral_offset: total lateral displacement (across the road) at the final waypoint.
      
    This function generates waypoints that gradually move the walker from its
    original sidewalk toward a point crossing the street.
    """
    waypoints = []
    # Calculate the incremental lateral offset per waypoint.
    lateral_step = lateral_offset / num_waypoints
    for i in range(1, num_waypoints + 1):
        # For this example, assume that crossing means increasing the y-coordinate.
        # (Adjust the axis based on your map orientation.)
        wp = carla.Location(
            x = start_location.x,      # gradual forward movement
            y = start_location.y - i * lateral_step,         # gradual lateral offset
            z = start_location.z
        )
        waypoints.append(wp)
    return waypoints


def force_jaywalk_path(world, walker, waypoints, tick_delay=10):
    """
    Forces the walker to follow a series of waypoints (simulating a jaywalk)
    by teleporting it along the path. A delay in ticks is introduced between steps.
    
    Parameters:
      world: the CARLA world object.
      walker: the pedestrian actor.
      waypoints: list of carla.Location objects representing the desired path.
      tick_delay: number of simulation ticks to wait between updates.
    """
    try:
        for idx, wp in enumerate(waypoints):
            # Force the walker’s position to the current waypoint.
            new_transform = carla.Transform(location=wp, rotation=walker.get_transform().rotation)
            walker.set_transform(new_transform)
            print(f"Walker forced to waypoint {idx+1}: {wp}")
            # Wait for a number of ticks to allow animations to play.
            for _ in range(tick_delay):
                world.tick()
            # Optionally, visualize the waypoint.
            world.debug.draw_string(
                wp,
                f"WP {idx+1}",
                draw_shadow=False,
                color=carla.Color(r=0, g=255, b=0),
                life_time=2.0,
                persistent_lines=False
            )
        print("Walker forced jaywalking path completed.")
    except Exception as e:
        print(f"Error in force_jaywalk_path: {e}")
