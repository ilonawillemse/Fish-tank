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
    
class Fish(Agent):
    "class Fish makes an agent of the fish"
    def __init__(self, unique_id, model, width, height):
        super().__init__(unique_id, model)
        self.width = width
        self.height = height
        self.energy = 10
    
    def move(self): 
        "decide on neighbour positions"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        
        "make the fish move to nearby algea"
        for i in range(len(possible_steps)):
            agents = self.model.grid.get_cell_list_contents([possible_steps[i]])
            if len(agents)> 0:
                for option in range(len(agents)):
                    if isinstance(agents[option], Algea):
                        agent = agents[option]
                        new_position = possible_steps[i]
                        pass
            else:
                new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        self.energy -= 1

        "make the fish eat the algea"
        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents)> 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Algea):
                    agent_algea = agents[option]
                    self.eat(agent_algea)
                

    
    def eat(self, agent): 
        self.model.grid.remove_agent(agent)
        self.energy += 2
    
    def move_up(self):        
        "when the fish dies it moves to the top of the tank"
        # self.model.grid.remove_agent()
        pass
        
    def step(self):
        if self.fish_energy():
            self.move()

        # else:
        #     self.move_up()

    def fish_energy(self):
        print(self.energy)
        if self.energy > 0:
            return True
        else:
            self.move_up()
            return False
        


class Algea(Agent):
    "class Fish makes an agent of the fish"
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    

class Fishtank(Model):
    "class forest creates a grid with cel objects"
    def __init__(self, width, height, probability_algea, number_fish):
        self.width = width
        self.height = height
        self.number_algea = width * height * probability_algea
        self.number_fish = number_fish
        
        self.grid = MultiGrid(width, height, False)
        self.visgrid = np.zeros((height,width))
        self.schedule = RandomActivation(self)

        # create agents
        for i in range(self.number_fish):
            a = Fish(i, self, self.width, self.height)
            self.schedule.add(a)

            # add fish to random grid cel
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
        
        for j in range(self.number_fish, int(self.number_algea)):
            b = Algea(j, self)
            self.schedule.add(b)

            # add algea to random grid cel
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(b, (x, y))


        self.datacollector = DataCollector(model_reporters={"Grid": self.status})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
    
    def status(self):
        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for algea in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][algea], Algea):
                            self.visgrid[i][j] = 1

                    for fish in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][fish], Fish):
                            self.visgrid[i][j] = 2
                    
                else:
                    self.visgrid[i][j] = 0

        
        return self.visgrid 

        

if __name__ == "__main__":
    probability_algea = 0.4
    # probability_algea = float(input('probability of algea: '))
    # y = int(input('fishtank height: '))
    # x = int(input('fishtank width: '))
    height = 10
    width = 20
    # number_fish = int(input('number of fish inside the tank: '))
    number_fish = 10

    # create a forest object
    tank = Fishtank(width, height, probability_algea, number_fish)

    # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange'])
   
    ims = []

    # data = tank.datacollector.get_model_vars_dataframe()
    # print(data)
  
    for _ in range(50):
        # data = tank.datacollector.get_model_vars_dataframe()
        # print(data)
        im = ax.imshow(tank.status(), cmap=cmap)
        # ims = ax.imshow(data, cmap=cmap)
        ims.append([im])
        tank.step()

    ani = animation.ArtistAnimation(fig, ims, interval = 500, blit = True, repeat_delay= 1000)
    plt.xlabel('width')
    plt.ylabel('height')
    plt.xticks(size = 0)
    plt.yticks(size = 0)

    ani.save("fish.gif")
    