# platformer/anim.py
import pygame


class AnimSprite(pygame.sprite.Sprite):
    def __init__(self, anims: dict[str, list[pygame.Surface]], pos, fps=10):
        super().__init__()
        self.anims = anims
        self.current = "idle"
        self.frames = self.anims[self.current]
        self.fps = fps
        self.timer = 0.0
        self.index = 0
        self.flip = False
        # target display size for frames (keep consistent)
        self.size = (50, 50)
        # rotation in degrees
        self.rotation = 0.0
        frame0: pygame.surface.Surface = self.frames[0]
        new_frame = pygame.transform.scale(frame0, self.size)
        self.image = new_frame
        self.rect = self.image.get_rect(topleft=pos)

    def set(self, name):

        if name != self.current:
            #print(f"Call set with name = {name}")
            self.current = name
            self.frames = self.anims[self.current]
            self.index = 0
            self.timer = 0.0
            # make sure the first frame is scaled and flipped to match current state
            frame: pygame.surface.Surface = self.frames[0]
            new_frame = pygame.transform.scale(frame, self.size)
            self.image = pygame.transform.flip(new_frame, True, False) if self.flip else new_frame
            # preserve position
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
  
    def update(self, dt, flip=False, rotation=0.0):
        self.flip = flip
        self.rotation = rotation
        self.timer += dt

        if self.timer >= 1.0 / self.fps:
            self.timer = 0.0
            self.index = (self.index + 1) % len(self.frames)
            #print(f"call update with self.index = {self.index}")
            frame : pygame.surface.Surface = self.frames[self.index]
            new_size = (50,50)
            new_frame = pygame.transform.scale(frame, new_size)
            # flip horizontally only (x=True, y=False)
            flipped_frame = pygame.transform.flip(new_frame, True, False) if self.flip else new_frame
            # apply rotation
            self.image = pygame.transform.rotate(flipped_frame, self.rotation)
            # preserve top-left after replacing the image
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            #print(self.flip)
