from spritesheet import SpriteSheet
import math


class Animation(object):
    """An object useful for animations with sprites"""

    def __init__(self, images, tilesize, length,  aps):
        self.images = []
        self.tilesize = tilesize
        self.aps = aps  # Animations loops per second
        self.sprite_strip = SpriteSheet(images)
        self.index = 0
        self.count = 0
        self.frame_loop = 30/self.aps  # How many cycles of animation fit in 1 second
        self.frame_tick = math.ceil(self.frame_loop/length)  # How many ticks need to be spent of one frame of animation
        self.end_count = self.frame_tick * length
        for i in range(length):
            x = self.sprite_strip.get_image(i*tilesize, 0, tilesize, tilesize)
            self.images.append(x)
        self.export_image = self.images[self.index]

    def update(self):
        self.count += 1
        if self.count % self.frame_tick == 0:
            self.export_image = self.images[self.index]
            self.index += 1
            if self.index > (len(self.images)-1):
                self.index = 0
        if self.count > self.end_count:
            self.count = 0

        return self.export_image
