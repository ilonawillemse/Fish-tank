"""
=================================================
Animated image using a precomputed list of images
=================================================

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import colors
from copy import deepcopy

class Cel():
    "class cel makes a cell object with a status"
    def __init__(self, status):
        self.status = status
    

class Forest():
    "class forest creates a grid with cel objects"
    def __init__(self, x, y, probability_empty, probability_tree):
        self.x = x
        self.y = y
        self.surrounding = ((-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1))
        self.probability_empty = probability_empty
        self.probability_tree = probability_tree
        
        self.grid = []
        for i in range(self.x):
            row = []
            for j in range(self.y):
                "this gives the cell objects a status"
                status = np.random.choice([0,1,2], p = [self.probability_empty, self.probability_tree, 0])
                row.append(Cel(status))
            self.grid.append(row)

        self.visgrid = []
        for i in range(self.x):
            rowvis = []
            for j in range(self.y):
                rowvis.append(self.grid[i][j].status)
            self.visgrid.append(rowvis)
        
                
    def status_first(self):
        "this returns the visgrid of the first forest with trees or empty spots and places one fire spot"
        randx = np.random.randint(0, self.x)
        randy = np.random.randint(0, self.y)
       
        for i in range(self.x):
            for j in range(self.y):
                if i == randx and j == randy:
                    self.visgrid[i][j] = 2

        self.tmp_visgrid = deepcopy(self.visgrid)
        return self.visgrid

    def status(self, x): 
        "this returns the visgrid after adjusting the next situation"    
        for i in range(self.x):
            for j in range(self.y):
                if self.visgrid[i][j] == 0:
                    self.tmp_visgrid[i][j] = 0
                if self.visgrid[i][j] == 2:
                    self.tmp_visgrid[i][j] = 0
                if self.visgrid[i][j] == 1:
                    self.burning_counter = 0
                    self.tree_counter = 0
                    for a, b in self.surrounding:
                        if i+a < self.x and i+a > 0 and j+b > 0 and j+b < self.y:
                            if self.visgrid[i+a][j+b] == 2:
                                self.burning_counter += 1
                    
                    # print(self.burning_counter)

                    # if self.tree_counter == 0:
                    #     self.burning_chance = 0
                    # else:
                    #     self.burning_chance = self.burning_counter/4
                    
                    # self.tree_chance = 1 - self.burning_chance
                    # print(self.burning_chance)

                    for a, b in self.surrounding:
                        if i+a < self.x and i+a > 0 and j+b > 0 and j+b < self.y:
                            if self.visgrid[i+a][j+b] == 2:
                                self.tmp_visgrid[i][j] = np.random.choice([1,2], p = [0.4, 0.6])
             

        # print(self.visgrid)
        self.visgrid = deepcopy(self.tmp_visgrid)
        return self.tmp_visgrid
        

    def burning(self):
        "this looks whether there is still a fire and if so returns True"

        for i in range(self.x):
            for j in range(self.y):
                if self.tmp_visgrid[i][j] == 2:
                    return True
        return False

if __name__ == "__main__":
    probability_tree = float(input('probability of a tree: '))
    probability_empty = 1 - probability_tree
    y = int(input('how high: '))
    x = int(input('how wide: '))

    # create a forest object
    forest = Forest(x, y, probability_empty, probability_tree)

    # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'red'])
    # cmap = 'RdYIGn
   
    ims = []

    data = forest.status_first()
    im = ax.imshow(data, cmap=cmap)
    ims.append([im])

    while forest.burning():
        data = forest.status(data)
        
        im = ax.imshow(data, cmap=cmap)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval = 500, blit = True, repeat_delay= 1000)
    ani.save("fish.gif")