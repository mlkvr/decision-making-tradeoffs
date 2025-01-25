import carla  # carla kütüphanesi dahil edildi
from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker, move_walker
from decision.decision_logic import process_decision
from sensors.camera import attach_camera
import cv2  # OpenCV pencerelerini kapatmak için

def main():
    global ego_vehicle, walker, walker_controller, camera

    try:
        # settings.py'deki setup_carla_client fonksiyonunu kullanarak bağlantı kurun
        client, world, blueprint_library = setup_carla_client()

        # Ego araç oluşturma işlemi
        ego_vehicle = spawn_ego_vehicle(world, blueprint_library)
        if ego_vehicle is None:
            print("Error: Ego vehicle could not be spawned!")
            return

        # Walker (yaya) oluşturma işlemi
        walker = spawn_walker(world, blueprint_library)
        if walker is None:
            print("Error: Walker could not be spawned!")
            return

        # Yaya kontrolcüsü ekle ve hareket ettir
        walker_controller_bp = blueprint_library.find('controller.ai.walker')
        walker_controller = world.try_spawn_actor(walker_controller_bp, carla.Transform(), attach_to=walker)
        if walker_controller is not None:
            walker_controller.start()
            move_walker(world, walker_controller)
        else:
            print("Error: Walker controller could not be spawned!")
            walker_controller = None

        # Kamerayı ego araca bağlama
        camera = attach_camera(world, ego_vehicle)
        if camera is None:
            print("Error: Camera could not be attached!")
            return
        
        # Simülasyon mantığı
        process_decision(ego_vehicle, walker)

        # Sonsuz döngü (kameradan görüntü almayı sürdürmek için)
        running = True  # Kontrol değişkeni
        while running:
            world.tick()  # Dünya zamanını ilerlet

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting...")
        running = False  # Döngüyü sonlandır

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        running = False  # Döngüyü sonlandır

    finally:
        # Temizlik
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
