import carla

def spawn_parked_vehicles(world, blueprint_library):
    vehicle_bp = blueprint_library.filter('vehicle.*')[0]
    spawn_points = [
        carla.Transform(carla.Location(x=50, y=-3.5, z=0.0)),
        carla.Transform(carla.Location(x=55, y=-3.5, z=0.0))
    ]
    for spawn_point in spawn_points:
        world.try_spawn_actor(vehicle_bp, spawn_point)
