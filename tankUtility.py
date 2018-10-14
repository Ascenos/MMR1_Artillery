class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)
        return self.x / other.x + self.y / other.y

    def __len__(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        self.x /= len(self)


class BasicParticle:
    def __init__(self, positionX, positionY, width, height, speedX = 0, speedY = 0):
        self.position = Vector2(positionX, positionY)
        self.size = Vector2(width, height)
        self.speed = Vector2(speedX, speedY)

    def update(self):
        self.move()

    def move(self):
        self.position += self.speed


class DecayingParticle(BasicParticle):
    def __init__(self, counter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = counter
        self.decayed = False

    def update(self):
        self.move()
        self.decay()

    def decay():
        self.counter -= 1
        if self.counter == 0:
            self.decayed = True

class GravityParticle(DecayingParticle):
    gravity = 0
    def __init__(self, *args, acceleration = None, **kwargs):
        if acceleration == None:
            self.acceleration = gravity

    def setGravity(value):
        gravity = value
    


class Tank:

    def __init__(self, positionX, positionY ,speedX, color, sizeFactor = 3):
        """ Die Tank Klasse besteht aus zwei Partikeln, einem für den Körper und einem
            für den Lauf.
        """

        self.sizeFactor = sizeFactor                # bestimmt die Skalierung des Panzers
        self.bodyWidth = 13 * self.sizeFactor       # sollte ungerade bleiben
        self.bodyHeight = 6 * self.sizeFactor       # sollte gerade bleiben
        self.rifleThickness = 1 * self.sizeFactor   # sollte ungerade bleiben
        self.rifleLength = 12 * self.sizeFactor     # sollte gerade bleiben
        self.body = BasicParticle(positionX, positionY, self.bodyWidth, self.bodyHeight, 0, 0, color)

        self.rifle = BasicParticle(positionX + ((((self.bodyWidth/self.rifleThickness)/2)-0.5) * self.rifleThickness)
                                # Hier wird mühselig der Lauf horizontal auf die Mitte des Panzers positioniert
                                , positionY-self.rifleLength+ (self.bodyHeight/2)
                                # Hier wird mühselig der Lauf vertikal auf die Mitte des Panzers positioniert
                                , self.rifleThickness, self.rifleLength, 0, 0, color)
        self.speedX = speedX                        # Fahrgeschwindigkeit des Panzers
        self.rotateSpeed = 4                        # Rotationsgeschwindigkeit des Lauf
        self.movingLeft = False
        self.movingRight = False
        self.movingRifleLeft = False
        self.movingRifleRight = False
        self.rifleDegree = 90                       # Neigung des Laufs

    def move(self):
        """ Die move Funktion überprüft erst ob das Bewegen des Panzers oder seines Laufs
            möglich ist und führt dann die Bewegung oder Rotation aus. Die Struktur ist wichtig,
            da die move Funktion in der Main Game Loop ständig aufgerufen wird. Durch das Drücken
            der Pfeiltasten verstellen sich dann die boolschen Variablen für die Bewegung und der Panzer
            bewegt sich. Durch diese Methode bewegt sich der Panzer sehr flüssig auf dem Bild. Eine
            Veränderung seiner Position durch Addition an seine momentane Position beim Drücken der Tasten
            ohne das move in der Main Game Loop hat sich als Ruckelig erwiesen.
        """
        if self.movingLeft == True and self.movingRight == False:  # Bewegung nach links
            self.body.position.x -= self.speedX
            self.rifle.position.x -= self.speedX
        elif self.movingLeft == False and self.movingRight == True:  # Bewegung nach rechhts
            self.body.position.x += self.speedX
            self.rifle.position.x += self.speedX

        if self.movingRifleLeft == True and self.movingRifleRight == False and self.rifleDegree > 0:
            self.rifleDegree -= self.rotateSpeed                    # Rotation gegen den Uhrzeigersinn
        elif self.movingRifleLeft == False and self.movingRifleRight == True and self.rifleDegree < 180:
            self.rifleDegree += self.rotateSpeed                    # Rotation mit dem Uhrzeigersinn
