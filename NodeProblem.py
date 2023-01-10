import pygame
from pygame.locals import *
import random
import math
import sys

#Defines
TOPBAR = 50
XSIZE = 800
YSIZENOTOP = 500
YSIZE = YSIZENOTOP + TOPBAR

DEFAULTNOOFNODES = 30
MINNODES = 5
MAXNODES = 200
DEFAULTNODESPEED = 2
MAXNODESPEED = 20
MINNODESPEED = 0.5
NODESIZE = 2
LINEDISTHRESHOLD = 200

DEFAULTLINEDIFFUSION = 4
MAXLINEDIFFUSION = 10

class Node:
    def __init__(self, speed):
        self.SpawnNewNode(speed)
    
    def SpawnNewNode(self, speed):
        #Chose random spot on the edge of the screen, and a random direction and speed
        self.pos = (random.random() * XSIZE, (random.random() * YSIZENOTOP) + TOPBAR)
        side = random.randint(0, 3)
        self.toDelete = False
        #Clamp position to one of the sides
        if (side == 0):
            self.pos = (0, self.pos[1])
            self.rot = random.randint(0, 180)
        elif (side == 1):
            self.pos = (XSIZE, self.pos[1])
            self.rot = random.randint(180, 360)
        elif (side == 2):
            self.pos = (self.pos[0], TOPBAR)
            self.rot = random.randint(90, 270)
        elif (side == 3):
            self.pos = (self.pos[0], YSIZE)
            self.rot = random.randint(0, 180)
            self.rot -= 90
            if self.rot < 0:
                self.rot += 360
        
        self.speed = (random.random() + 0.01) * speed #Make sure the speed can't be exactly zero

    def Tick(self):
        #Move the nodes, and destroy them if they go out of bounds
        self.pos = (math.sin(self.rot) * self.speed + self.pos[0], math.cos(self.rot) * self.speed + self.pos[1])

        if (self.pos[0] < 0):
            self.toDelete = True
        elif (self.pos[0] > XSIZE):
            self.toDelete = True
        elif (self.pos[1] < TOPBAR):
            self.toDelete = True
        elif (self.pos[1] > YSIZE):
            self.toDelete = True


class NodeProblem:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Node Problem")

        self.screen = pygame.display.set_mode((XSIZE, YSIZE))
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        if pygame.font:
            self.font = pygame.font.Font(None, 40)

        self.red = 255
        self.green = 255
        self.blue = 255
        self.maxNodeSpeed = DEFAULTNODESPEED
        self.noNodes = DEFAULTNOOFNODES
        self.lineDiffusion = DEFAULTLINEDIFFUSION
        self.subLineDiffusion = self.lineDiffusion

        #Hide cursor
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        
        self.nodes = []
        self.finished = False
    
    def Run(self):
        
        while not self.finished:
            #Handle input
            self.HandleInput()

            self.HandleNodes()

            #Draw screen
            self.Draw()

            self.clock.tick(60)

    def HandleInput(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        if pygame.key.get_pressed()[K_UP]:
            if pygame.key.get_pressed()[K_r] and self.red < 255:
                self.red += 1
            elif pygame.key.get_pressed()[K_g] and self.green < 255:
                self.green += 1
            elif pygame.key.get_pressed()[K_b] and self.blue < 255:
                self.blue += 1
            elif pygame.key.get_pressed()[K_s] and self.maxNodeSpeed < MAXNODESPEED:
                self.maxNodeSpeed += 0.1
            elif pygame.key.get_pressed()[K_n] and self.noNodes < MAXNODES:
                self.noNodes += 1
            elif pygame.key.get_pressed()[K_d] and self.subLineDiffusion < MAXLINEDIFFUSION:
                self.subLineDiffusion += 0.1
                self.lineDiffusion = round(self.subLineDiffusion)
        elif pygame.key.get_pressed()[K_DOWN]:
            if pygame.key.get_pressed()[K_r] and self.red > 0:
                self.red -= 1
            elif pygame.key.get_pressed()[K_g] and self.green > 0:
                self.green -= 1
            elif pygame.key.get_pressed()[K_b] and self.blue > 0:
                self.blue -= 1
            elif pygame.key.get_pressed()[K_s] and self.maxNodeSpeed > MINNODESPEED:
                self.maxNodeSpeed -= 0.1
            elif pygame.key.get_pressed()[K_n] and self.noNodes > MINNODES:
                self.noNodes -= 1
            elif pygame.key.get_pressed()[K_d] and self.subLineDiffusion > 1:
                self.subLineDiffusion -= 0.1
                self.lineDiffusion = round(self.subLineDiffusion)
    
    def HandleNodes(self):
        for n in self.nodes:
            n.Tick()
            if (n.toDelete == True):
                self.nodes.remove(n)

        #Make sure we have self.noNodes nodes
        while len(self.nodes) < self.noNodes:
            self.nodes.append(Node(self.maxNodeSpeed))

    def Draw(self):
        self.screen.blit(self.background, (0,0))

        for n in self.nodes:
            #Draw lines between nodes
            for d in self.nodes:
                xdif = abs(n.pos[0] - d.pos[0])
                ydif = abs(n.pos[1] - d.pos[1])
                dist = math.sqrt(xdif ** 2 + ydif ** 2)
                for i in range(self.lineDiffusion - 1, -1, -1):
                    if dist < LINEDISTHRESHOLD / (i + 1):
                        pygame.draw.line(self.screen, (self.red/(self.lineDiffusion/(i+1)), self.green/(self.lineDiffusion/(i+1)), self.blue/(self.lineDiffusion/(i+1))), n.pos, d.pos)
                        break
            #Draw lines to cursor
            if (pygame.mouse.get_pos()[1] > TOPBAR):
                xdif = abs(n.pos[0] - pygame.mouse.get_pos()[0])
                ydif = abs(n.pos[1] - pygame.mouse.get_pos()[1])
                dist = math.sqrt(xdif ** 2 + ydif ** 2)
                for i in range(self.lineDiffusion - 1, -1, -1):
                    if dist < LINEDISTHRESHOLD / (i + 1):
                        pygame.draw.line(self.screen, (self.red/(self.lineDiffusion/(i+1)), self.green/(self.lineDiffusion/(i+1)), self.blue/(self.lineDiffusion/(i+1))), n.pos, pygame.mouse.get_pos())
                        break
        
        #Draw circles second so they appear on top
        for n in self.nodes:
            pygame.draw.circle(self.screen, (self.red, self.green, self.blue), n.pos, NODESIZE)
        pygame.draw.circle(self.screen, (self.red, self.green, self.blue), pygame.mouse.get_pos(), NODESIZE)

        #Draw colours
        red = pygame.Rect(0,0,TOPBAR,TOPBAR)
        pygame.draw.rect(self.screen, (self.red,0,0), red)
        green = pygame.Rect(TOPBAR*2,0,TOPBAR,TOPBAR)
        pygame.draw.rect(self.screen, (0,self.green,0), green)
        blue = pygame.Rect(TOPBAR,0,TOPBAR,TOPBAR)
        pygame.draw.rect(self.screen, (0,0,self.blue), blue)

        #Draw speed
        speedStr = "Speed: " + str(round(self.maxNodeSpeed, 3))
        speedTxt = self.font.render(speedStr, True, (255,255,255))
        self.screen.blit(speedTxt, (TOPBAR*3.1, 0))

        #Draw diffusion
        stepsStr = "Steps: " + str(self.lineDiffusion)
        stepsTxt = self.font.render(stepsStr, True, (255,255,255))
        self.screen.blit(stepsTxt, (TOPBAR*6.5, 0))

        #Draw node count
        nodeStr = "Number of Nodes: " + str(self.noNodes)
        nodeTxt = self.font.render(nodeStr, True, (255,255,255))
        self.screen.blit(nodeTxt, (TOPBAR * 10, 0))

        pygame.display.flip()



nodes = NodeProblem()
nodes.Run()