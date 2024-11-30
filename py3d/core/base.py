import pygame
import os
import subprocess

from py3d.core.input import Input
from py3d.core.utils import Utils
from OpenGL.GL import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE


class Base:
    def __init__(self, screen_size=(512, 512)):
        # Initialize all pygame modules
        pygame.init()
        # Indicate rendering details
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        # Initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # Use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # Create and display the window
        self._screen = pygame.display.set_mode(screen_size, display_flags)
        # Set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        # Determine if main loop is active
        self._running = True
        # Manage time-related data and operations
        self._clock = pygame.time.Clock()
        # Manage user input
        self._input = Input()
        # number of seconds application has been running
        self._time = 0

        self.frame_count = 0
        # Print the system information
        Utils.print_system_info()

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def input(self):
        return self._input

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def initialize(self):
        """ Implement by extending class """
        pass

    def update(self):
        """ Implement by extending class """
        pass

    def run(self):
        # Startup #
        self.initialize()
        # main loop #
        while self._running:
            # process input #
            self._input.update()
            if self._input.quit:
                self._running = False
            # seconds since iteration of run loop
            self._delta_time = self._clock.get_time() / 1000
            # Increment time application has been running
            self._time += self._delta_time
            # Update #
            self.update()

            # Render #
            # Display image on screen
            pygame.display.flip()

            self.frame_count += 1

            #guarda los pixeles de la ventana
            pixeles = glReadPixels(0, 0, 1920, 1080, GL_RGBA, GL_UNSIGNED_BYTE)

            #convierte dichos pixeles en una imagen
            imagen = pygame.image.frombuffer(pixeles, (1920, 1080), "RGBA")

            #invierte la imagen    
            imagen = pygame.transform.flip(imagen, False, True)

            #guarda la imagen actual en la carpeta frames, y enumera los frames guardados
            pygame.image.save(imagen, f"./frames/frame_{self.frame_count}.jpg")

            # Pause if necessary to achieve 60 FPS
            self._clock.tick(144)
        # Shutdown #

        pygame.quit()

        #al cerrar la ventana de pygame, se ejecuta un comando con subproccess el cual
        #ejecuta la generacion de un video con las imagenes o frames guardados en la carpeta frames
        #y guarda el resultado en la carpeta video

        print("Generando video!")

        subprocess.run([
            "ffmpeg",
            "-r",
            "144",
            "-f",
            "image2",
            #"-s",
            #"1920x1080",
            "-i",
            f"{os.getcwd()}/frames/frame_%d.jpg",
            "-vcodec",
            "libx264",
            "-crf",
            "0",
            f"{os.getcwd()}/video/video.mp4"
        ])
