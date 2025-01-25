import carla

def spawn_walker(world, blueprint_library):
    """
    Yaya (walker) belirtilen dünya ve blueprint kütüphanesi kullanılarak spawn eder.
    """
    try:
        print("walker.py successfully called")
        walker_bp = blueprint_library.filter('walker.pedestrian.*')[0]  # İlk uygun yaya blueprint'ini seç

        # Ego aracın spawn noktasını al
        ego_vehicle_spawn_point = world.get_map().get_spawn_points()[0]

        # Ego aracın spawn noktasından 100 metre ileride bir spawn noktası ayarla
        walker_spawn_point = carla.Transform(
            carla.Location(
                x=ego_vehicle_spawn_point.location.x + 85,  # 100 metre ileri
                y=ego_vehicle_spawn_point.location.y + 11,
                z=ego_vehicle_spawn_point.location.z
            ),
            carla.Rotation(pitch=0.0, yaw=270.0, roll=0.0)  # Rotasyonu 270 derece olarak ayarladık
        )

        # Spawn noktasını görselleştir
        world.debug.draw_string(
            walker_spawn_point.location,
            "Walker Spawn Point",
            draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0),  # Kırmızı renk
            life_time=5.0,  # 5 saniye boyunca görünür
            persistent_lines=True
        )

        walker = world.spawn_actor(walker_bp, walker_spawn_point)

        if walker is None:
            print("Error: Walker could not be spawned!")
        return walker
    except IndexError:
        print("Error: No walker blueprints available!")
        return None
    except Exception as e:
        print(f"Error while spawning walker: {e}")
        return None


def move_walker(world, walker_controller):
    """
    Yayanın hareket etmesini sağlar.
    Yaya, mevcut pozisyonundan Z ekseninde 10 metre yukarı hareket eder.
    """
    try:
        # Walker'ın mevcut pozisyonunu al
        walker_location = walker_controller.get_location()

        # Yeni hedef konumu belirle (Z ekseninde 10 metre yukarı)
        target_location = carla.Location(
            x=walker_location.x,
            y=walker_location.y - 40,
            z=walker_location.z
        )

        # Yaya kontrolcüsünü hedef konuma gönder
        walker_controller.go_to_location(target_location)

        # Hedef konumu görselleştir
        world.debug.draw_string(
            target_location,
            "Target Location",
            draw_shadow=False,
            color=carla.Color(r=0, g=255, b=0),  # Yeşil renk
            life_time=15.0,  # 5 saniye boyunca görünür
            persistent_lines=True
        )
        print("Walker is moving to the target location.")
    except Exception as e:
        print(f"Error while moving walker: {e}")

