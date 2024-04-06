from funcs import *
from graph import *
import pygame
import random
import math
from nn import *


class Core:
    def __init__(self) -> None:
        # Pygame
        self.dims = (1400, 900)
        self.window = pygame.display.set_mode(self.dims)
        self.background_clr = (230, 230, 230)
        self.title_font = pygame.font.SysFont("Arial", 48, True)
        self.font = pygame.font.SysFont("Arial", 15)

        # Diagnostics
        self.test_fimg = self.title_font.render("Diagnostics", True, (0, 0, 0))
        self.survival_graph = LineGraph((self.dims[0] - 550, 650), (500, 300), 1, (300, 10))

        # Grid
        self.gridsize = 100
        self.griddims = (700, 700)
        self.cellsize = self.griddims[0] / self.gridsize
        self.topleft = 50
        self.gridboard = []
        for i in range(self.gridsize):
            self.gridboard.append([])
            for _ in range(self.gridsize):
                self.gridboard[i].append(0)

        # Organisms
        self.number_organisms = 300
        self.organisms = []
        for i in range(self.number_organisms):
            self.organisms.append(Organism(self))
            self.gridboard = self.organisms[i].game.gridboard

        # Simluation
        self.tickspeed = 60 # Steps per second
        self.generation_time = 150 # Steps total
        self.mutation_constant = 0.02
        self.kill = False
        self.generations = 0
        self.fps = 0.0
        self.survival_rate = 0
        self.survival_rate_history = []

    def new_generation(self):
        self.generations += 1
        self.gridboard = []
        for i in range(self.gridsize):
            self.gridboard.append([])
            for _ in range(self.gridsize):
                self.gridboard[i].append(0)

        surviving_organisms = self.survive(self.organisms)
        self.survival_rate_history.append(self.survival_rate)
        self.survival_graph.add_point((self.generations, self.survival_rate))

        new_organisms = []
        for i in range(self.number_organisms):
            o1 = surviving_organisms[random.randint(0, len(surviving_organisms) - 1)] 
            o2 = surviving_organisms[random.randint(0, len(surviving_organisms) - 1)]
            new_organisms.append(self.pair(o1, o2))

        self.organisms = new_organisms

    def pair(self, o1, o2):
        new_weights = []
        for i in range(len(o1.brain.genome[0])):
            if random.randint(0, 1) == 0: new_weights.append(o1.brain.genome[0][i])
            else: new_weights.append(o2.brain.genome[0][i])

            if random.randint(0, 100) < self.mutation_constant * 100:
                del new_weights[-1]
                new_weights.append(np.float64(0.1 * random.uniform(-1, 1)))

        new_biases = []
        for i in range(len(o1.brain.genome[1])):
            if random.randint(0, 1) == 0: new_biases.append(o1.brain.genome[1][i])
            else: new_biases.append(o2.brain.genome[1][i])

            if random.randint(0, 100) < self.mutation_constant * 100:
                del new_biases[-1]
                new_biases.append(np.float64(0.1 * random.uniform(-1, 1)))
        
        new_genome = [new_weights, new_biases]
        weights = new_genome[0]; biases = new_genome[1]

        new_organism = Organism(self); self.gridboard = new_organism.game.gridboard
        new_organism.brain.genome = new_genome

        l1_weights = weights[:len(new_organism.brain.inputs) * new_organism.brain.n_w1]
        l1_weights = split(l1_weights, new_organism.brain.n_w1)
        l2_weights = weights[len(l1_weights):len(l1_weights) + new_organism.brain.n_w1 * new_organism.brain.n_w2]
        l2_weights = split(l2_weights, new_organism.brain.n_w2)
        l3_weights = weights[len(l2_weights):len(l2_weights) + new_organism.brain.n_w2 * new_organism.brain.n_w3]
        l3_weights = split(l3_weights, new_organism.brain.n_w3)

        l1_biases = [biases[:new_organism.brain.n_w1]]
        l2_biases = [biases[len(l1_biases):len(l1_biases) + new_organism.brain.n_w2]]
        l3_biases = [biases[len(l2_biases):len(l2_biases) + new_organism.brain.n_w3]]

        new_organism.brain.layer1.weights = l1_weights
        new_organism.brain.layer2.weights = l2_weights
        new_organism.brain.layer3.weights = l3_weights
        new_organism.brain.layer1.biases = l1_biases
        new_organism.brain.layer2.biases = l2_biases
        new_organism.brain.layer3.biases = l3_biases

        return new_organism

    def survive(self, organisms):
        surviving_organisms = []
        for o in organisms:
            if self.distance_to_nearest_corner(o.gridpos) < 20: surviving_organisms.append(o)

        self.survival_rate = len(surviving_organisms) / len(organisms)

        return surviving_organisms
    
    def distance_to_nearest_corner(self, gridpos):
        c1 = math.sqrt(abs(gridpos[0] - self.gridsize)**2 + abs(gridpos[1] - self.gridsize)**2)
        c2 = math.sqrt(gridpos[0]**2 + abs(gridpos[1] - self.gridsize)**2)
        c3 = math.sqrt(gridpos[0]**2 + gridpos[1]**2)
        c4 = math.sqrt(abs(gridpos[0] - self.gridsize)**2 + gridpos[1]**2)
        return min(c1, c2, c3, c4)

    def update(self):
        self.draw()
        self.update_organisms()

    def draw(self):
        self.window.fill(self.background_clr)
        self.draw_grid()
        self.draw_organisms()
        self.draw_diagnostics()
        self.window = self.survival_graph.update(self.window)

    def draw_diagnostics(self):
        self.window.blit(self.test_fimg, (self.dims[0] - self.test_fimg.get_width() - 20, 20))

        diagnoistcs = [
            self.font.render(f"Generation: {self.generations}", True, (0, 0, 0)),
            self.font.render(f"Previous survival rate: {int(self.survival_rate*100)}%", True, (0, 0, 0)),
            self.font.render(f"Mutation constant: {self.mutation_constant * 100}%", True, (0, 0, 0)),
            self.font.render(f"Tickspeed: {self.tickspeed}", True, (0, 0, 0)),
            self.font.render(f"Generation time: {self.generation_time}", True, (0, 0, 0)),
            self.font.render(f"Gridsize: {self.gridsize}", True, (0, 0, 0)),
            self.font.render(f"FPS: {int(self.fps)}", True, (0, 0, 0)),
        ]

        y_start_pos = 30 + self.test_fimg.get_height()
        for i, d in enumerate(diagnoistcs):
            self.window.blit(d, (self.dims[0] - self.test_fimg.get_width() - 18, y_start_pos + (i * diagnoistcs[i - 1].get_height())))

    def draw_organisms(self):
        for o in self.organisms:
            realpos = [
                self.topleft + (o.gridpos[0] * self.cellsize) + self.cellsize/2,
                self.topleft + (o.gridpos[1] * self.cellsize) + self.cellsize/2
            ]
            pygame.draw.circle(self.window, o.clr, realpos, (self.cellsize / 2))

    def update_organisms(self):
        for o in self.organisms:
            self.gridboard = o.update(self)

    def draw_grid(self):
        for i in range(self.gridsize+1):
            const = i * self.cellsize
            pygame.draw.line(self.window, (0, 0, 0), (self.topleft + const, self.topleft), (self.topleft + const, self.topleft + self.griddims[1]), 1)
            
        for i in range(self.gridsize+1):
            const = i * (self.griddims[1] / self.gridsize)
            pygame.draw.line(self.window, (0, 0, 0), (self.topleft, self.topleft + const), (self.topleft + self.griddims[0], self.topleft + const), 1)

class Organism:
    def __init__(self, game: Core) -> None:
        self.game = game
        self.gridpos = [random.randint(0, self.game.gridsize - 1), random.randint(0, self.game.gridsize - 1)]
        while self.game.gridboard[self.gridpos[0]][self.gridpos[1]] == 1:
            self.gridpos = [random.randint(0, self.game.gridsize - 1), random.randint(0, self.game.gridsize - 1)]
        self.game.gridboard[self.gridpos[0]][self.gridpos[1]] = 1
        
        self.update_inputs()
        self.brain = NN(self.given_inputs)

        self.clr = (0, 0, 200)

    def update(self, game) -> list[list]:
        self.game = game

        self.update_inputs()
        self.brain.update_inputs(self.given_inputs)

        self.brain.think()
        if self.brain.str_output != "nothing":
            self.move(self.brain.str_output)

        return self.game.gridboard

    def move(self, movement): # movement could be: for left right up down
        before_gridpos = self.gridpos.copy()
        self.game.gridboard[self.gridpos[0]][self.gridpos[1]] = 0

        if movement == "left" and self.gridpos[0] != 0:
            self.gridpos[0] -= 1
        elif movement == "right" and self.gridpos[0] != (self.game.gridsize - 1):
            self.gridpos[0] += 1
        elif movement == "up" and self.gridpos[1] != 0:
            self.gridpos[1] -= 1
        elif movement == "down" and self.gridpos[1] != (self.game.gridsize - 1):
            self.gridpos[1] += 1

        if not self.game.kill and self.game.gridboard[self.gridpos[0]][self.gridpos[1]] == 1:
            self.gridpos = before_gridpos

        self.game.gridboard[self.gridpos[0]][self.gridpos[1]] = 1

    def update_inputs(self):
        self.proximity1 = -1 # -1 because your own position
        for xj in range(-1, 2):
            for yj in range(-1, 2):
                if xj == -1 and self.gridpos[0] == 0: continue
                if xj == 1 and self.gridpos[0] == (self.game.gridsize - 1): continue
                if yj == -1 and self.gridpos[1] == 0: continue
                if yj == 1 and self.gridpos[1] == (self.game.gridsize - 1): continue

                if self.game.gridboard[self.gridpos[0] + xj][self.gridpos[1] + yj] == 1:
                    self.proximity1 += 1

        self.given_inputs = [
            self.gridpos[0],
            self.gridpos[1],
            self.proximity1,
        ]

        if self.proximity1 > 4: self.clr = (200, 0, 0)
        else: self.clr = (0, 0, 200)
