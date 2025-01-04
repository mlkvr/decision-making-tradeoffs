from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker
from decision.decision_logic import process_decision
from sensors.camera import attach_camera  # Kamera modülünü ekledik

def main():
    global ego_vehicle, walker, camera  # Kamera için global tanımlama yaptık

    try:
        # settings.py'deki setup_carla_client fonksiyonunu kullanarak bağlantı kurun
        client, world, blueprint_library = setup_carla_client()

        # Ego araç oluşturma işlemi ego_vehicle.py'daki fonksiyona devredildi
        ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
        if ego_vehicle is None:
            print("Error: Ego vehicle could not be spawned!")
            return

        # Walker (yaya) oluşturma işlemi
        walker = spawn_walker(world, blueprint_library)
        if walker is None:
            print("Error: Walker could not be spawned!")
            return

        # Kamerayı ego araca bağlama
        camera = attach_camera(world, ego_vehicle)
        if camera is None:
            print("Error: Camera could not be attached!")
            return

        # Simülasyon mantığı
        process_decision(ego_vehicle, walker)

        # Sonsuz döngü (kameradan görüntü almayı sürdürmek için)
        while True:
            pass

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Temizlik
        if ego_vehicle is not None:
            ego_vehicle.destroy()
        if walker is not None:
            walker.destroy()
        if camera is not None:
            camera.stop()  # Kamerayı durdur
            camera.destroy()
        # OpenCV pencerelerini kapat
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
