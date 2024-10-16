import pygame
import sys
import math
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Circle Movement with Collision")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
circle_radius = 20
circle_pos = pygame.Vector2(100, 100)
circle_speed = 1


square_size = 100
square_rect = pygame.Rect((width - square_size) // 2, (height - square_size) // 2, square_size, square_size)
top_left = (square_rect.x, square_rect.y)
top_right = (square_rect.x + square_rect.width, square_rect.y)
bottom_left = (square_rect.x, square_rect.y + square_rect.height)
bottom_right = (square_rect.x + square_rect.width, square_rect.y + square_rect.height)
def calculate_rotated_corners(rect, angle):
    cx, cy = rect.center
    angle_rad = math.radians(angle)
    rotated_top_left = (
        -(cx-top_left[0]) * math.cos(angle_rad) - (cy-top_left[1]) * math.sin(angle_rad)+cx,
        -(cy-top_left[1]) * math.cos(angle_rad) + (cx-top_left[0]) * math.sin(angle_rad)+cy
    )

    rotated_top_right = (
        -(cx-top_right[0]) * math.cos(angle_rad) - (cy-top_right[1]) * math.sin(angle_rad)+cx,
        -(cy-top_right[1]) * math.cos(angle_rad) + (cx-top_right[0]) * math.sin(angle_rad)+cy
    )

    rotated_bottom_left = (
        -(cx-bottom_left[0]) * math.cos(angle_rad) - (cy-bottom_left[1]) * math.sin(angle_rad)+cx,
        -(cy-bottom_left[1]) * math.cos(angle_rad) + (cx-bottom_left[0]) * math.sin(angle_rad)+cy
    )

    rotated_bottom_right = (
        -(cx-bottom_right[0]) * math.cos(angle_rad) - (cy-bottom_right[1]) * math.sin(angle_rad)+cx,
        -(cy-bottom_right[1]) * math.cos(angle_rad) + (cx-bottom_right[0]) * math.sin(angle_rad)+cy
    )
    print(square_rect.center)
    print(top_left,top_right,bottom_left,bottom_right)
    print(rotated_top_left,rotated_top_right,rotated_bottom_left,rotated_bottom_right)
    return [rotated_top_left, rotated_top_right, rotated_bottom_left, rotated_bottom_right]
angel=123%360
def check_in_circle(point,a,b,r):
    distance=(point[0]-a)*(point[0]-a)+(point[1]-b)*(point[1]-b)
    print(point[0],point[1],a,b)
    print(distance,r*r)
    return r*r-distance>=0
def check_collision(tank, bullet):
    r = 20
    x, y = tank.center
    alpha = float(angel)
    a, b = bullet.center
    w, h = 100,100
    check_x, check_y = a - x, b - y
    new_x = float(check_x * math.cos(math.radians(alpha)) - check_y * math.sin(math.radians(alpha)))
    new_y = float(check_y * math.cos(math.radians(alpha)) + check_x * math.sin(math.radians(alpha)))
    if max(-w / 2, new_x - r) <= min(w / 2, new_x + r) and max(-h / 2, new_y - r) <= min(h / 2, new_y + r):
         if -w/2<=new_x<=w/2 or -h/2<=new_y<=h/2:
             return True
         else:
             for corner in tmp:
                 if check_in_circle(corner, a,b, r):
                     return True
             return False

    else:
        return False
def draw_rotated_rect(surface, color, rect, angle):
    rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 0))  # Fill with transparent color
    pygame.draw.rect(rect_surface, color, (0, 0, rect.width, rect.height))
    rotated_surface = pygame.transform.rotate(rect_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=rect.center)
    surface.blit(rotated_surface, rotated_rect.topleft)
tmp = calculate_rotated_corners(square_rect, angel)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    new_pos = circle_pos.copy()  # Copy current position
    if keys[pygame.K_LEFT]:
        new_pos.x -= circle_speed
    if keys[pygame.K_RIGHT]:
        new_pos.x += circle_speed
    if keys[pygame.K_UP]:
        new_pos.y -= circle_speed
    if keys[pygame.K_DOWN]:
        new_pos.y += circle_speed
    circle_rect = pygame.Rect(new_pos.x - circle_radius, new_pos.y - circle_radius, circle_radius * 2, circle_radius * 2)
    if not check_collision(square_rect,circle_rect):
        circle_pos = new_pos
        #print("HELLO\n")
    screen.fill(WHITE)
    draw_rotated_rect(screen, RED, square_rect, angel)
    pygame.draw.circle(screen, BLUE, (int(circle_pos.x), int(circle_pos.y)), circle_radius)
    pygame.display.flip()
    pygame.time.Clock().tick(60)