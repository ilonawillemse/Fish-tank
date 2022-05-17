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
            for i in range(self.y):
                for j in range(self.x):
                        if i == randy and j == randx:
                            self.visgrid[i][j] = 2
        self.visgrid[0][0] = 3
        self.tmp_visgrid = deepcopy(self.visgrid)
        return self.visgrid

    def status(self, x): 
        "this returns the visgrid after adjusting the next situation"   
        # print(self.visgrid) 
        fish_mating = 0
        energy = 0
        for i in range(self.y):
            for j in range(self.x):
                "when the current pixel is a fish"   
                if self.visgrid[i][j] == 2:
                    surrounding = ((-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1))
                    random = np.random.choice([0,1,-1])
                    random2 = np.random.choice([0,1,-1])
                    
                    # for a, b in surrounding:
                    #     if i+a <= self.x and i+a >= 0 and j+b >= 0 and j+b <= self.y:
                    #         if self.visgrid[i+a][j+b] == 1:
                    #             random = b
                    #             random2 = a
                    #             energy += 1
                    #         # elif self.visgrid[i+a][j+b] == 2:
                    #         #     random = a
                    #         #     random2 = b
                    #         #     fish_mating += 1
                    # print(energy)
                    # # print(fish_mating)
                    # # print(random)
                    # # print(random2)
                    # if energy > 3:
                    #     self.tmp_visgrid[i][j] = 3

                    if i+random < self.y and i+random >= 0 and j+random >= 0 and j+random < self.x and i+random2 < self.y and i+random2 >= 0 and j+random2 >= 0 and j+random2 < self.x:
                        if random == 0 and random2 == 0:
                            self.tmp_visgrid[i][j] = 2
                        
                        else:
                            self.tmp_visgrid[i+random][j+random2] = 2
                            self.tmp_visgrid[i][j] = 0    
                            
        self.visgrid = deepcopy(self.tmp_visgrid)
        return self.tmp_visgrid
        

if __name__ == "__main__":
    probability_algea = 0.8
    # probability_algea = float(input('probability of algea: '))
    # y = int(input('fishtank height: '))
    # x = int(input('fishtank width: '))
    y = 20
    x = 40
    # number_fish = int(input('number of fish inside the tank: '))
    number_fish = 10

    # create a forest object
    tank = Fishtank(y, x, probability_algea, number_fish)

    # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange', 'yellow'])
   
    ims = []

    data = tank.add_fish()
    im = ax.imshow(data, cmap=cmap)
    ims.append([im])

    for _ in range(70):
        data = tank.status(data)
        
        im = ax.imshow(data, cmap=cmap)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval = 500, blit = True, repeat_delay= 1000)
    ani.save("fish.gif")