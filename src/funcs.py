from math import sin, radians, cos
import pygame


def split(l, number_splits) -> list:
    nl = []
    for i in range(0, len(l), number_splits):
        nl.append(l[i:i + number_splits])

    return nl

def pie(scr,color,center,radius,start_angle,stop_angle):
    theta=start_angle
    while theta <= stop_angle:
        pygame.draw.line(scr,color,center, 
        (center[0]+radius*cos(radians(theta)),center[1]+radius*sin(radians(theta))),2)
        theta+=0.01

def pie_outline(scr,color,center,radius,start_angle,stop_angle):
    theta=start_angle
    while theta <= stop_angle:
        pygame.draw.line(scr,color, 
            (center[0]+radius*cos(radians(theta)),
            center[1]+radius*sin(radians(theta))),
            (center[0]+radius*cos(radians(theta)),
            center[1]+radius*sin(radians(theta))),2
        )
        theta+=0.01

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)
