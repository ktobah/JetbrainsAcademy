class Sphere:
    PI = 3.1415

    def __init__(self, radius):
        self.radius = radius
        self.volume = 4 / 3 * self.PI * (radius ** 3)
