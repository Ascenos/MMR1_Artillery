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