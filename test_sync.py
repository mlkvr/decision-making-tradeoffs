import carla


def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    # Synchronous mode'u açıyoruz:
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05  # 20 tick per second
    world.apply_settings(settings)

    blueprint_library = world.get_blueprint_library()

    # Araç spawn et
    ego_bp = blueprint_library.filter("vehicle.*")[0]
    spawn_points = world.get_map().get_spawn_points()
    ego_vehicle = world.spawn_actor(ego_bp, spawn_points[0])

    # Araç hareketi için default kontrol komutu ver
    ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5))

    try:
        while True:
            user_input = input("Tick için Enter'a bas, çıkmak için 'q'+Enter: ")
            if user_input.lower() == 'q':
                break
            world.tick()  # Manuel tick atılıyor
            print("Tick atıldı. Araç hareket ediyor mu kontrol et.")

    finally:
        settings = world.get_settings()
        settings.synchronous_mode = False
        world.apply_settings(settings)
        ego_vehicle.destroy()
        print("Simülasyon bitti, araç temizlendi.")


if __name__ == "__main__":
    main()
