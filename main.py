#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import noise
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

class Program(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):
        button1 = QPushButton("&Obraz1", self)
        button2 = QPushButton("&Obraz2", self)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(button1)
        buttonsLayout.addWidget(button2)
        button1.clicked.connect(self.generateFirstImage)
        button2.clicked.connect(self.generateSecondImage)
        self.setLayout(buttonsLayout)
        self.resize(400, 400)
        self.setWindowTitle("Image Generation")
        self.show()

    def generateFirstImage(self):
            def rgb_norm(world):
                world_min = np.min(world)
                world_max = np.max(world)
                norm = lambda x: (x - world_min / (world_max - world_min)) * 255
                return np.vectorize(norm)

            def prep_world(world):
                norm = rgb_norm(world)
                world = norm(world)
                return world

            shape = (1024, 1024)
            scale = 100
            octaves = 6
            persistence = 0.5
            lacunarity = 2.0
            seed = np.random.randint(0, 100)
            #seed = 126

            world = np.zeros(shape)
            for i in range(shape[0]):
                for j in range(shape[1]):
                    world[i][j] = noise.pnoise2(i / scale,
                                                j / scale,
                                                octaves=octaves,
                                                persistence=persistence,
                                                lacunarity=lacunarity,
                                                repeatx=1024,
                                                repeaty=1024,
                                                base=seed)

            Image.fromarray(prep_world(world)).show()


    def generateSecondImage(self):
       def rgb_norm(world):
           world_min = np.min(world)
           world_max = np.max(world)
           norm = lambda x: (x - world_min / (world_max - world_min)) * 255
           return np.vectorize(norm)

       def prep_world(world):
           norm = rgb_norm(world)
           world = norm(world)
           return world

       shape = (1024, 1024)
       scale = 50
       octaves = 6
       persistence = 0.5
       lacunarity = 2.0
       seed = np.random.randint(0, 100)
       world = np.zeros(shape)
       for i in range(shape[0]):
           for j in range(shape[1]):
               world[i][j] = noise.pnoise2(i / scale,
                                           j / scale,
                                           octaves=octaves,
                                           persistence=persistence,
                                           lacunarity=lacunarity,
                                           repeatx=1024,
                                           repeaty=1024,
                                           base=seed)

       blue = [65, 105, 225]
       green = [34, 139, 34]
       beach = [238, 214, 175]
       snow = [255, 250, 250]
       mountain = [139, 137, 137]

       def add_color(world):
           color_world = np.zeros(world.shape + (3,))
           for i in range(shape[0]):
               for j in range(shape[1]):
                   if world[i][j] < -0.05:
                       color_world[i][j] = blue
                   elif world[i][j] < 0:
                       color_world[i][j] = beach
                   elif world[i][j] < .20:
                       color_world[i][j] = green
                   elif world[i][j] < 0.35:
                       color_world[i][j] = mountain
                   elif world[i][j] < 1.0:
                       color_world[i][j] = snow

           return color_world

       color_world = add_color(world).astype(np.uint8)
       Image.fromarray(color_world,'RGB').show()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Program()
    sys.exit(app.exec_())