#!/usr/bin/python3
import math
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.texture import Texture
from py3d.geometry.sphere import SphereGeometry
from py3d.material.texture import TextureMaterial
from py3d.extras.movement_rig import MovementRig
from py3d.extras.planet import Planet
from py3d.material.lambert import LambertMaterial
from py3d.light.ambient import AmbientLight
from py3d.light.point import PointLight

class SistemaSolar(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer(clear_color=[0, 0, 0])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1920/1080)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([300, 100, 50])
        self.rig.look_at([0, 0, 0])
        sky_geometry = SphereGeometry(radius=500)
        sky_material = TextureMaterial(texture=Texture(file_name="./py3d/images_8k/8k_stars.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        #factor de rotacion y traslacion
        self.rotation_factor = 1000
        self.translation_factor = 5000

        #diccionario que almacena el angulo que debe rotar cada planeta por cada frame, siendo 144 fps
        self.rotation = {
            "sun" : [self.calculate_rotation(period=27), 0, 0],
            "mercury" : [self.calculate_rotation(period=58), 0, 0],
            "venus" : [self.calculate_rotation(period=243),0,0],
            "earth" : [self.calculate_rotation(1), 0, 0],
            "mars" : [self.calculate_rotation(1.04), 0, 0],
            "jupyter" : [self.calculate_rotation(0.414), 0, 0],
            "saturn" : [self.calculate_rotation(0.426), 0, 0],
            "uranus" : [self.calculate_rotation(0.717), 0, 0],
            "neptune" : [self.calculate_rotation(0.671), 0, 0]
        }

        #diccionario que almacena los dias que tarda cada planeta en completar una orbita alrededor del Sol
        self.period = {
            "sun" : 1,
            "mercury" : 88,
            "venus" : 225,
            "earth" : 365,
            "mars" : 687,
            "jupyter" : 4332,
            "saturn" : 10759,
            "uranus" : 30685,
            "neptune" : 60266
        }

        self.AU_factor = 3

        #diccionario que almacena la distancia entre cada planeta y el Sol, en unidades astronomicas
        self.AU = {
            "sun" : 0 * self.AU_factor,
            "mercury" : 0.39 * self.AU_factor,
            "venus" : 0.72 * self.AU_factor,
            "earth" : 1 * self.AU_factor,
            "mars" : 1.52 * self.AU_factor,
            "jupyter" : (5.20 * self.AU_factor) * 1,
            "saturn" : (9.57 * self.AU_factor) * 1,
            "uranus" : (19.20 * self.AU_factor) * 1,
            "neptune" : (30.06 * self.AU_factor) * 1
        }

        numero_luces = 2

        self.sun = Planet(
            material=TextureMaterial(
                    texture=Texture("./py3d/images_8k/8k_sun.jpg")
                )
            )
        
        self.mercury = Planet(
            material=LambertMaterial(
                    texture=Texture("./py3d/images_8k/8k_mercury.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.venus = Planet(
            material=LambertMaterial(
                    texture=Texture("./py3d/images_8k/4k_venus_atmosphere.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.earth = Planet(
            material=LambertMaterial(
                    texture=Texture("./py3d/images_8k/8k_earth_daymap.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.mars = Planet(
            material=LambertMaterial(
                    texture=Texture("./py3d/images_8k/8k_mars.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.jupyter = Planet(
            material=LambertMaterial(
                    texture=Texture("./py3d/images_8k/8k_jupiter.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.saturn = Planet(
            material=LambertMaterial(
                texture=Texture("./py3d/images_8k/8k_saturn.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.uranus = Planet(
            material=LambertMaterial(
                texture=Texture("./py3d/images_8k/2k_uranus.jpg"), number_of_light_sources=numero_luces
                )
            )
        
        self.neptune = Planet(
            material=LambertMaterial(
                texture=Texture("./py3d/images_8k/2k_neptune.jpg"), number_of_light_sources=numero_luces
                )
            )

        ambient_light = AmbientLight(color=[1, 1, 1])
        self.scene.add(ambient_light)

        self.point_light_1 = PointLight(color=[1, 1, 1], position=[0, 0, 0], attenuation=[0.002, 0.002, 0.002])
        self.scene.add(self.point_light_1)

        self.sun.set_position( [0, 0, 0] )
        self.sun.scale(2)
        self.scene.add(self.sun)

        self.mercury.scale(0.3)
        self.scene.add(self.mercury)

        self.venus.scale(0.5)
        self.scene.add(self.venus)

        self.earth.scale(1)
        self.scene.add(self.earth)

        self.mars.scale(0.9)
        self.scene.add(self.mars)

        self.jupyter.scale(3)
        self.scene.add(self.jupyter)

        self.saturn.scale(2.5)
        self.scene.add(self.saturn)

        self.uranus.scale(2)
        self.scene.add(self.uranus)

        self.neptune.scale(2.2)
        self.scene.add(self.neptune)

    #calcula el angulo de rotacion de cada planeta en funcion del periodo
    def calculate_rotation(self, period) -> float:
        seconds = period * 24 * 60 * 60
        degrees_per_second = 360 / seconds
        degrees_per_frame = degrees_per_second / 144
        return degrees_per_frame
    
    #calcula la posicion de un planeta en funcion del tiempo actual y su distancia del sol en unidad astronomica
    def calculate_planet_orbit(self, current_time, factor, period, AU):
        angular_velocity = ((2 * math.pi) / period) * factor

        x = AU * self.AU_factor * math.cos(angular_velocity * current_time) 
        y = AU * self.AU_factor *  math.sin(angular_velocity * current_time) 

        return [x, 0, y]

    def update(self):
        #se establece el angulo de rotacion de cada planeta, consultando el diccionario que almacena dicho angulo de rotacion
        self.sun.rotate_y(self.rotation.get("sun")[0] * self.rotation_factor)
        self.mercury.rotate_y(self.rotation.get("mercury")[0] * self.rotation_factor)

        #venus rota en sentido contrario
        self.venus.rotate_y(-self.rotation.get("venus")[0] * self.rotation_factor )
            
        self.earth.rotate_y(self.rotation.get("earth")[0] * self.rotation_factor)
        self.mars.rotate_y(self.rotation.get("mars")[0] * self.rotation_factor)
        self.jupyter.rotate_y(self.rotation.get("jupyter")[0] * self.rotation_factor)
        self.saturn.rotate_y(self.rotation.get("saturn")[0] * self.rotation_factor)

        #urano rota de 'costado'
        self.uranus.rotate_x(self.rotation.get("uranus")[0] * self.rotation_factor)
        self.neptune.rotate_y(self.rotation.get("neptune")[0] * self.rotation_factor)

        #durante cada actualizacion, se calcula la nueva posicion de los planetas pasandole a la funcion calculate_planet_orbit:
        #   - el tiempo actual
        #   - el factor de traslacion
        #   - el numero de dias que tarda un planeta en orbitar el Sol
        #   - la distancia del planeta al Sol en UA

        self.mercury.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time,
                factor=self.translation_factor,
                period=self.period.get("mercury"),
                AU=self.AU.get("mercury")
                ) 
            )
        
        self.venus.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time,
                factor=self.translation_factor,
                period=self.period.get("venus"),
                AU=self.AU.get("venus")
                ) 
            )
        
        self.earth.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time,
                factor=self.translation_factor,
                period=self.period.get("earth"),
                AU=self.AU.get("earth")
                ) 
            )
        
        self.mars.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time, 
                factor=self.translation_factor, 
                period=self.period.get("mars"), 
                AU=self.AU.get("mars")
                ) 
            )
        
        self.jupyter.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time, 
                factor=self.translation_factor, 
                period=self.period.get("jupyter"), 
                AU=self.AU.get("jupyter")
                ) 
            )
        
        self.saturn.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time, 
                factor=self.translation_factor, 
                period=self.period.get("saturn"), 
                AU=self.AU.get("saturn")
                ) 
            )
        
        self.uranus.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time, 
                factor=self.translation_factor, 
                period=self.period.get("uranus"), 
                AU=self.AU.get("uranus")
                ) 
            )
        
        self.neptune.set_position( 
            self.calculate_planet_orbit(
                current_time=self._time, 
                factor=self.translation_factor, 
                period=self.period.get("neptune"), 
                AU=self.AU.get("neptune")
                ) 
            )

        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
SistemaSolar(screen_size=[1920, 1080]).run()
