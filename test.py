if __name__ == "__main__":
    from game_objects.tank import Tank
    from engine.base import engine
    tank = Tank(2)
    engine.update()
else:
    raise
