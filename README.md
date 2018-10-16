# Tutorium 6

Wir werden ein super tolles Spiel programmieren!
> TODO

### Game Object hierarchy overview

- GameObject
> This is a base game Object

    - InputObject
    > This object takes input and processes that

        - Tank
    - ParticleObject
    > This is a small lived object for particles and smaller objects

        - Projectile
        - ParticleEffects
    - RigidObjects
    > Objects that rarely change, or do not need frequent update

        - Terrain
        - Background

- GameFunction
> These are used for independent functions from game objects.
> Will always be processed first (TODO)

    - mainGameFunction
    - some other stuff

---

- GameBehavior
> Coroutine to be executed with a GameObject to control it in 'parralel'


### Usage
By inheriting a class from GameFunction (`base.engine.GameFunction`) you can
create a Instance to add the function to the main engine loop. This allows
for some additional features, like cerating GameObjects as well as starting
other GameFunctions and stuff.

You can either use the `engine.managed.loop` to get a self managed infinite
loop, or you can manually call the update function

### Resolution considerations
Optimization resolutions
##### 16x9:
    - WXGA is included in QHD
    - QHD:   2560x1440, 320*8x180*8
    - FHD:   1920x1080, 320*6x180*6
    - HD+:   1600x900,  320*5x180*5
    - WXGA:  1280x720,  320*4x180*4
##### 4x3:
    - ????
##### Constants
320*6*5*2, 180*6*5*2