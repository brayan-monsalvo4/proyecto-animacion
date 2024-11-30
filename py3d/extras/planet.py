from py3d.core_ext.mesh import Mesh
from py3d.geometry.sphere import SphereGeometry

class Planet(Mesh):
    def __init__(self, material):
        super().__init__(geometry=SphereGeometry(), material=material)
