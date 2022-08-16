# See Tech with Tim if dont understand any part of this
import pygame
import neat
import time
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

# doubling the scale ie size of img and then loading the imgs in a list
BIRD_IMGS = [pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))

BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird():
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # rotation to tilt the bird to move up or down
    ROT_VEL = 20  # rotaion per frame
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0  # how much we moved since last jump
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * (self.tick_count) + 1.5 * (self.tick_count) ** 2

        # setting max velocity to 16
        if d >= 16:
            d = 16
        # adds a smoother transition to jump
        if d < 0:
            d -= 2

        # updating the height
        self.y = self.y + d

        # if we are moving up or above the jumping point tilt the bird accordingly
        if d < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:  # becasue when we go up we dont want to all the way up so capping it with MAX_ROTATION
                self.tilt = self.MAX_ROTATION
            else:  # tilt down
                if self.tilt > -90:  # because when we go down we want to tilt all the way down
                    self.tilt -= self.ROT_VEL

    def draw(self, win):  # win==the window on which we are drawing
        self.img_count += 1  # no of times we have shown an image

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < 2 * self.ANIMATION_TIME:
            self.img = self.IMGS[1]
        elif self.img_count < 3 * self.ANIMATION_TIME:
            self.img = self.IMGS[2]
        elif self.img_count < 4 * self.ANIMATION_TIME:
            self.img = self.IMGS[1]
        elif self.img_count == 4 * self.ANIMATION_TIME + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if (self.tilt <= -80):
            # if the bird is falling it wont flap the wings so we will be showing a single image
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # to rotate the img about the axis of the bird
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)

        # draws the rotated img on the window
        win.blit(rotated_img, new_rect.topleft)

    # to get the collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe():
    GAP = 200
    VEL = 5

    def __init__(self, x):  # y will be determined randomly
        self.x = x
        self.height = 0

        # to determine where the top f the pipe would be drawn
        self.top = 0
        self.bottom = 0
        # to upside down the image for top pipes
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        # sets the height where the upper pipe image is to be drawn
        # so that its bottom is at the desired location
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # checks if the pixels in the mask of pipe and bird are far or are same and thus collided
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # gives the collision point of bird and pipe
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if bottom_point or top_point:
            return True  # ie if anyone is present the collision is true

        return False


class Base():
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # looping the first image after the second image if it goes completely out of the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    # draw the bg_img at 0,0 on the window
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    # each generation is called genomes
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)  # the bottom of our screen
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()  # to set frame rate manually
    score = 0

    run = True

    while run:
        clock.tick(30)  # max frame rate =30
        for event in pygame.event.get():  # checks if any event like mouse or kepyboard press happens
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            # updating the fitness so the bird try to move forward instead of dropping down or flying so high
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []  # removed pipes
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)
        for bird in birds:
            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    # prints the config values in terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
