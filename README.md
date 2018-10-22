# pyEngine

Small Unity inspired Engine for some little projects

### Game Object hierarchy overview

- GameObject
        This is a base game Object
    - InputObject
            This object takes input and processes that
        - Tank
    - ParticleObject
            This is a small lived object for particles and smaller objects
        - Projectile
        - ParticleEffects
    - RigidObjects
            Objects that rarely change, or do not need frequent update
        - Terrain
        - Background
- GameFunction
        These are used for independent functions from game objects.
    - mainGameFunction
    - some other stuff

---

- GameBehavior
        Coroutine to be executed with a GameObject to control it in 'parralel'


### Usage
By inheriting a class from GameFunction (`base.engine.GameFunction`) you can
create a Instance to add the function to the main engine loop. This allows
for some additional features, like cerating GameObjects as well as starting
other GameFunctions and stuff.

You can either use the `engine.managed.loop` to get a self managed infinite
loop, or you can manually call the update function

### Resolution considerations
##### 16x9:

| Name | Resolution  | Factors         |
|------|-------------|-----------------|
| QHD  | 2560 x 1440 | 320\*8 x 180\*8 |
| FHD  | 1920 x 1080 | 320\*6 x 180\*6 |
| HD+  | 1600 x 900  | 320\*5 x 180\*5 |
| WXGA | 1280 x 720  | 320\*4 x 180\*4 |
##### Constants
320\*6\*5\*2, 180\*6\*5\*2