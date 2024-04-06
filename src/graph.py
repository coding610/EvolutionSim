import pygame


class LineGraph:
    def __init__(self, origo_pos: tuple, axis_dims: tuple, max_value: float, n_steps: tuple) -> None:
        self.pos = origo_pos
        self.axis_dims = axis_dims
        self.max_value = max_value
        self.n_steps = n_steps

        self.points = []
        self.nudge_size = 3
        self.step_sizex = self.axis_dims[0] / float(self.n_steps[0])
        self.step_sizey = self.axis_dims[1] / float(self.n_steps[1])

    def add_point(self, coord):
        self.points.append(coord)

    def update(self, window):
        pygame.draw.line(window, (0, 0, 0), self.pos, (self.pos[0] + self.axis_dims[0], self.pos[1]))
        pygame.draw.line(window, (0, 0, 0), self.pos, (self.pos[0], self.pos[1] - self.axis_dims[1]))

        for steps in range(1, self.n_steps[0] + 1):
            p1x = (self.pos[0] + steps*self.step_sizex, self.pos[1] + self.nudge_size)
            p2x = (self.pos[0] + steps*self.step_sizex, self.pos[1] - self.nudge_size)
            pygame.draw.line(window, (0, 0, 0), p1x, p2x)
        for steps in range(1, self.n_steps[1] + 1):
            p1y = (self.pos[0] + self.nudge_size, self.pos[1] - steps*self.step_sizey)
            p2y = (self.pos[0] - self.nudge_size, self.pos[1] - steps*self.step_sizey)
            pygame.draw.line(window, (0, 0, 0), p1y, p2y)

        for p in self.points:
            pygame.draw.circle(window, (0, 0, 0), (self.pos[0] + self.step_sizex * p[0], self.pos[1] - self.axis_dims[1] * p[1]), 3)

        if len(self.points) > 0:
            pygame.draw.line(window, (30, 30, 30), self.pos, (self.pos[0] + self.step_sizex * self.points[0][0], self.pos[1] - self.axis_dims[1] * self.points[0][1]))
        for i in range(len(self.points) - 1):
            p1 = (self.pos[0] + self.step_sizex * self.points[i][0], self.pos[1] - self.axis_dims[1] * self.points[i][1])
            p2 = (self.pos[0] + self.step_sizex * self.points[i+1][0], self.pos[1] - self.axis_dims[1] * self.points[i+1][1])
            pygame.draw.line(window, (30, 30, 30), p1, p2, 1)


        return window
