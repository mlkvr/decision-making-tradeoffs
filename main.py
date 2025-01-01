from config.settings import setup_carla_client
from actors.ego_vehicle import spawn_ego_vehicle
from actors.walker import spawn_walker
from decision.decision_logic import process_decision

def main():
    global ego_vehicle, walker

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

        # Simülasyon mantığı
        process_decision(ego_vehicle, walker)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Temizlik
        if ego_vehicle is not None:
            ego_vehicle.destroy()
        if walker is not None:
            walker.destroy()

if __name__ == '__main__':
    main()
