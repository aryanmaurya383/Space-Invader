import pygame
import cv2
import os
import HandTracker as ht

WIN_WIDTH = 900
WIN_HEIGHT = 700
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bg.jpg")))
SPACESHIP_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "spaceship.png")))
ENEMY_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "enemies.png")))
BULLET_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "bullet.png")))

SPACESHIP_POS = [450, 550]
BULLET_POS = [SPACESHIP_POS[0] + 65, 510]

clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)


class Enemies():
    def __init__(self, id, x, y):
        self.countdown = 0
        self.id = id
        self.y = y
        self.x = x

    def update_countdown(self):
        self.countdown += 1
        if self.countdown > 60:
            self.countdown = 0
        self.y += 10


class Spaceship():
    def __init__(self):
        pass


class Bullet():
    def __init__(self, x, y):
        self.ENEMY_IMG = ENEMY_IMG
        self.IMG = BULLET_IMG
        self.x = x
        self.y = y

    def move(self, bullet_y):
        bullet_y -= 10
        return bullet_y

    def collision(self, enemy):
        enemy_mask = pygame.mask.from_surface(self.ENEMY_IMG)
        bullet_mask = pygame.mask.from_surface(self.IMG)
        bullet_offset = (self.x - enemy.x, self.y - round(enemy.y))

        bullet_collision_point = enemy_mask.overlap(bullet_mask, bullet_offset)

        if bullet_collision_point:
            return True

        return False


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 100)  # to open the pygame window at top left corner
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    game_over = False
    detector = ht.HandDetectionModule()
    time_passed = 0
    ENEMIES_POSITION = [Enemies(0, 50, -20), Enemies(1, 250, -20), Enemies(2, 450, -20), Enemies(3, 650, -20),
                        Enemies(4, 50, 90), Enemies(5, 250, 90), Enemies(6, 450, 90), Enemies(7, 650, 90)]
    bullets = []

    while game_over == False:
        clock.tick(30)
        time_passed += 1
        win.blit(BG_IMG, (0, 0))

        success, img = cap.read()
        img = detector.findHands(img)

        landmark_list = detector.findPosition(img, )
        if len(landmark_list) != 0:
            SPACESHIP_POS[0] = 1.2 * landmark_list[8][1] - 100
            BULLET_POS[0] = SPACESHIP_POS[0] + 65

        if (time_passed == 30):
            bullets.append(Bullet(BULLET_POS[0], BULLET_POS[1]))
        if (time_passed == 60):
            bullets.append(Bullet(BULLET_POS[0], BULLET_POS[1]))
        if (time_passed == 90):
            bullets.append(Bullet(BULLET_POS[0], BULLET_POS[1]))
            time_passed = 0

        for ep in ENEMIES_POSITION:
            win.blit(ENEMY_IMG, (ep.x, ep.y))
            if (ep.y == SPACESHIP_POS[1]):
                print("GAME OVER")
                pygame.display.quit()
                quit()
                game_over = True

        win.blit(SPACESHIP_IMG, SPACESHIP_POS)

        for bullet in bullets:
            if (bullet.y < 0):
                bullets.remove(bullet)
            bullet.y -= 10

            win.blit(BULLET_IMG, (bullet.x, bullet.y))

            for ep in ENEMIES_POSITION:
                if bullet.collision(ep):
                    ENEMIES_POSITION.remove(ep)
                    bullets.remove(bullet)

        for en in ENEMIES_POSITION:
            en.y += 0.5

        if len(ENEMIES_POSITION) == 0:
            print("YOU WIN !!")
            pygame.display.quit()
            quit()
            game_over = True

        pygame.display.update()
        cv2.imshow("Image", img)
        cv2.waitKey(1)


main()
