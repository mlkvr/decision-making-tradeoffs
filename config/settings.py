import carla

def setup_carla_client():
    print("settings.py successfuly called")
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    return client, world, blueprint_library
