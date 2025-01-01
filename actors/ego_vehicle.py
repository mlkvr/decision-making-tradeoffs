import carla

def spawn_ego_vehicle(world, blueprint_library):
    """
    Ego aracı belirtilen dünya ve blueprint kütüphanesi kullanılarak spawn eder.
    """
    try:
        print("ego_vehicle.py successfuly called")
        vehicle_bp = blueprint_library.filter('vehicle.*')[0]  # İlk uygun araç blueprint'ini seç
        spawn_point = world.get_map().get_spawn_points()[0]  # İlk uygun spawn noktasını seç
        return world.spawn_actor(vehicle_bp, spawn_point)
    except IndexError:
        print("Error: No vehicle blueprints or spawn points available!")
        return None
    except Exception as e:
        print(f"Error while spawning ego vehicle: {e}")
        return None
