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
    

class Fishtank():
    "class forest creates a grid with cel objects"
    def __init__(self, y, x, probability_algea, number_fish):
        self.x = x
        self.y = y
        self.surrounding = ((-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1))
        self.probability_algea = probability_algea
        self.number_fish = number_fish
        
        self.grid = []
        for i in range(self.y):
            row = []
            for j in range(self.x):
                "this gives the cell objects a status"
                status = np.random.choice([0,1], p = [1-probability_algea, probability_algea])
                # status = np.random.choice([0,1,2])
                row.append(Cel(status))
            self.grid.append(row)

        self.visgrid = []
        for i in range(self.y):
            rowvis = []
            for j in range(self.x):
                rowvis.append(self.grid[i][j].status)
            self.visgrid.append(rowvis)
        
                
    def add_fish(self):
        "this returns the visgrid of the first forest with trees or empty spots and places one fire spot"
        for _ in range(self.number_fish):
            randx = np.random.randint(0, self.x)
            randy = np.random.randint(0, self.y)
            for i in range(self.x):
                for j in range(self.y):
                        if i == randy and j == randx:
                            self.visgrid[i][j] = 2

        self.tmp_visgrid = deepcopy(self.visgrid)
        return self.visgrid

    def status(self, x): 
        "this returns the visgrid after adjusting the next situation"   
        # print(self.visgrid) 

        for i in range(self.y):
            for j in range(self.x):
                if self.visgrid[i][j] == 2:
                    number = np.random.randint(0,10)
                    for a, b in self.surrounding:
                        if i+a < self.x and i+a > 0 and j+b > 0 and j+b < self.y:
                            if number < 1:
                                self.tmp_visgrid[i][j+1] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 2:
                                self.tmp_visgrid[i][j-1] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 3:
                                self.tmp_visgrid[i+1][j+1] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 4:
                                self.tmp_visgrid[i-1][j+1] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 5:
                                self.tmp_visgrid[i+1][j] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 6:
                                self.tmp_visgrid[i-1][j-1] = 2
                                self.tmp_visgrid[i][j] = 0
                            elif number < 7:
                                self.tmp_visgrid[i+1][j-1] = 2
                                self.tmp_visgrid[i][j] = 0
                            else:
                                self.tmp_visgrid[i-1][j] = 2
                                self.tmp_visgrid[i][j] = 0

                    # for a, b in self.surrounding:
                    #     if i+a < self.x and i+a > 0 and j+b > 0 and j+b < self.y:
                    #         if self.visgrid[i+a][j+b] == 2:
                    #             self.visgrid[i][j] = np.random.choice([1,2], p = [0.4, 0.6])
                
        self.visgrid = deepcopy(self.tmp_visgrid)
        return self.tmp_visgrid
        

if __name__ == "__main__":
    probability_algea = 0.2
    # probability_algea = float(input('probability of algea: '))
    # y = int(input('fishtank height: '))
    # x = int(input('fishtank width: '))
    y = 50
    x = 100
    # number_fish = int(input('number of fish inside the tank: '))
    number_fish = 20

    # create a forest object
    tank = Fishtank(50, 100, probability_algea, number_fish)

    # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange'])
   
    ims = []

    data = tank.add_fish()
    im = ax.imshow(data, cmap=cmap)
    ims.append([im])

    for _ in range(30):
        data = tank.status(data)
        
        im = ax.imshow(data, cmap=cmap)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval = 500, blit = True, repeat_delay= 1000)
    ani.save("fish.gif")