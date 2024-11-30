from py3d.light.light import Light


class DirectionalLight(Light):
    def __init__(self, color=(1, 1, 1), direction=(0, -1, 0), position=(0,0,0)):
        super().__init__(Light.DIRECTIONAL)
        self._color = color
        self.set_direction(direction)
        self.set_position(position)
