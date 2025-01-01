import carla

def spawn_walker(world, blueprint_library):
    """
    Yaya (walker) belirtilen dünya ve blueprint kütüphanesi kullanılarak spawn eder.
    """
    try:
        print("walker.py successfuly called")
        walker_bp = blueprint_library.filter('walker.pedestrian.*')[0]  # İlk uygun yaya blueprint'ini seç
        walker_spawn_point = carla.Transform(carla.Location(x=2.0, y=3.0, z=1.0))
        return world.spawn_actor(walker_bp, walker_spawn_point)
    except IndexError:
        print("Error: No walker blueprints available!")
        return None
    except Exception as e:
        print(f"Error while spawning walker: {e}")
        return None


def move_walker(walker_controller):
    walker_controller.go_to_location(carla.Location(x=40, y=-3.5, z=0.0))
