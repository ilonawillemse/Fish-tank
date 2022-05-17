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
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# class Water():
#     "class cel makes a cell object with agents"
#     def __init__(self):
#         self.status = 0
    
class Fish(Agent):
    "class Fish makes an agent of the fish"
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def move(self): 
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def step(self):
        self.move()
    
    # def move2(self):
    #     "this returns the visgrid after adjusting the next situation"   
    #     # print(self.visgrid) 
    #     self.fish_mating = 0
    #     self.energy = 0

    #     for i in range(self.y):
    #         for j in range(self.x):

    #             "when the current pixel is a fish"   
    #             if self.visgrid[i][j] == 2:
    #                 random = np.random.choice([0,1,-1])
    #                 random2 = np.random.choice([0,1,-1])

    #                 if i+random < self.y and i+random >= 0 and j+random >= 0 and j+random < self.x and i+random2 < self.y and i+random2 >= 0 and j+random2 >= 0 and j+random2 < self.x:
    #                     if random == 0 and random2 == 0:
    #                         self.tmp_visgrid[i][j] = 2
                        
    #                     else:
    #                         if self.tmp_visgrid[i+random][j+random2] == 1:
    #                             self.energy += 1
    #                         self.tmp_visgrid[i+random][j+random2] = 2
    #                         self.tmp_visgrid[i][j] = 0   
                    
    #                         print(self.energy) 
    #                         if self.energy > 4:
    #                             self.tmp_visgrid[i][j] = 3
    #                             self.energy = 0
        
                
        #         elif self.visgrid[i][j] == 3:
        #             random = np.random.choice([0,1,-1])
        #             random2 = np.random.choice([0,1,-1])

        #             if i+random < self.y and i+random >= 0 and j+random >= 0 and j+random < self.x and i+random2 < self.y and i+random2 >= 0 and j+random2 >= 0 and j+random2 < self.x:
        #                 if random == 0 and random2 == 0:
        #                     self.tmp_visgrid[i][j] = 3
                        
        #                 else:
        #                     self.tmp_visgrid[i+random][j+random2] = 3
        #                     self.tmp_visgrid[i][j] = 0   

        # self.visgrid = deepcopy(self.tmp_visgrid)
        # return self.tmp_visgrid


class Algea(Agent):
    "class Fish makes an agent of the fish"
    def __init__(self):
        self.status = 1
    




class Fishtank(Model):
    "class forest creates a grid with cel objects"
    def __init__(self, y, x, probability_algea, number_fish):
        self.x = x
        self.y = y
        self.probability_algea = probability_algea
        self.number_fish = number_fish
        
        self.grid = MultiGrid(x, y, True)
        self.visgrid = np.zeros((y,x))
        self.schedule = RandomActivation(self)

        # create agents
        for i in range(self.number_fish):
            a = Fish(i, self)
            self.schedule.add(a)

            # add fish to random grid cel
            x = self.random.randrange(self.x)
            y = self.random.randrange(self.y)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(model_reporters={"Grid": self.status})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
    
    def status(self):
        for i in range(self.y):
            for j in range(self.x):
                if len(self.grid[j][i]) > 0:
                    if isinstance(self.grid[j][i][0], Fish):
                        self.visgrid[i][j] = 2
                        print('ja')
                else:
                    self.visgrid[i][j] = 0
        return self.visgrid 

    # def make_fishtank(self):
    #     "make fishtank"

        # self.grid = []
        # for i in range(self.y):
        #     row = []
        #     for j in range(self.x):
                # "this gives the cell objects a status"
                # random_number = np.random.choice([0,1], p = [1 - probability_algea, probability_algea])
                # if random_number == 0:
                #     status = 0
                #     row.append(Water())
                # if random_number == 1:
                #     status = 1
                #     row.append(Algea())
        #         row.append(0)
        #     self.grid.append(row)

        # for _ in range(self.number_fish):
        #     randx = np.random.randint(0, self.x)
        #     randy = np.random.randint(0, self.y)
        #     for i in range(self.y):
        #         for j in range(self.x):
        #                 if i == randy and j == randx:
        #                     self.grid[i][j] = Fish()

        # self.visgrid = []
        # for i in range(self.y):
        #     rowvis = []
        #     for j in range(self.x):
        #         rowvis.append(self.grid[i][j].status)
        #     self.visgrid.append(rowvis)
        
        # self.visgrid[0][0] = 3
        # self.tmp_visgrid = deepcopy(self.visgrid)
        

        

if __name__ == "__main__":
    probability_algea = 0.4
    # probability_algea = float(input('probability of algea: '))
    # y = int(input('fishtank height: '))
    # x = int(input('fishtank width: '))
    y = 20
    x = 40
    # number_fish = int(input('number of fish inside the tank: '))
    number_fish = 3

    # create a forest object
    tank = Fishtank(y, x, probability_algea, number_fish)

    # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange', 'yellow'])
   
    ims = []

    data = tank.datacollector.get_model_vars_dataframe()
    # print(data)

    for _ in range(70):
        # data = tank.datacollector.get_model_vars_dataframe()
        tank.step()
        im = ax.imshow(tank.status(), cmap=cmap)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval = 500, blit = True, repeat_delay= 1000)
    plt.axis('off')
    ani.save("fish.gif")
    