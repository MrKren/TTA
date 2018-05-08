from spritesheet import SpriteSheet


class Animation(object):

    def __init__(self, images, tilesize, length,  fps):
        self.images = []
        self.tilesize = tilesize
        self.fps = fps
        self.sprite_strip = SpriteSheet(images)
        self.index = 0
        self.count = 0
        for i in range(length):
            x = self.sprite_strip.get_image(i*tilesize, 0, tilesize, tilesize)
            self.images.append(x)
        self.export_image = self.images[self.index]

    def update(self):
        self.count += 1
        if (30/self.fps) % self.count == 0:
            self.export_image = self.images[self.index]
            self.index += 1
            if self.index > (len(self.images)-1):
                self.index = 0
        if self.count > 30:
            self.count = 0

        return self.export_image
