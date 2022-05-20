"""
=================================================
Animated image using a precomputed list of images
=================================================

"""
from shutil import which
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
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    
class Fish(Agent):
    "class Fish makes an agent of the fish"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = 20
    
    def move(self): 
        "decide on neighbour positions"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        

        "make the fish move to nearby algea"

        for i in range(len(possible_steps)):
            the_agents = self.model.grid.get_cell_list_contents([possible_steps[i]])
            if len(the_agents)> 0:
                for option in range(len(the_agents)):
                    if isinstance(the_agents[option], Algea):
                        new_position = possible_steps[i]
                        pass
                    else:
                        new_position = self.random.choice(possible_steps)

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
                    if  self.energy < 150:
                        self.eat(agent_algea)
        

        "make the fish mate with each other"

        if len(agents)> 1:
            # print(agents)
            if isinstance(agents[0], Fish) and isinstance(agents[1], Fish):
                if self.fish_mating_energy():
                    self.mating()

    
    def eat(self, algea): 
        "the fish eats algea"

        self.model.grid.remove_agent(algea)
        self.model.schedule.remove(algea)
        self.energy += 10
    

    def move_up(self):        
        "when the fish dies it moves to the top of the tank"

        new = self.pos[1] - 2
        new_pos = (self.pos[0], new)

        if new >= 0:
            self.model.grid.move_agent(self, new_pos)
        
        else:
            self.die()
        

    def die(self):
        "the fish dies / dissapears"

        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents)> 0:
            for option in range(len(agents)):
                if isinstance(agents[option], Fish):
                    fish = agents[option]
                    self.model.grid.remove_agent(fish)
                    self.model.schedule.remove(fish)
        
        
    def step(self):
        "the fish moves when it still has enegery, otherwise dies"

        if self.fish_energy():
            self.move()

        else:
            self.move_up()


    def fish_energy(self):
        "tells whether the fish still got some energy"

        if self.energy > 0:
            return True


    def fish_mating_energy(self):
        "tells whether the fish has enough mating energy"
        if self.energy > 20:
            return True
        

    def mating(self):
        "fish make a baby but loose some energy"

        fish = Fish(self.model.next_id(), self.model)
        self.model.schedule.add(fish)
        self.model.grid.place_agent(fish, self.pos)
        self.energy -= 10


class Algea(Agent):
    "class Algea makes an agent of the algea"
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def grow(self):
        "makes algea grow with a chance"

        neighbours = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        
        new_algea = self.random.choice(neighbours)
                            
        algea = Algea(self.model.next_id(), self.model)
        self.model.schedule.add(algea)
        self.model.grid.place_agent(algea, new_algea)
        
    def random_grow(self):
        x = self.random.randrange(self.model.width)
        y = self.random.randrange(self.model.height)

        algea = Algea(self.model.next_id(), self.model)
        self.model.schedule.add(algea)
        self.model.grid.place_agent(algea, (x, y))

    def step(self):
        # print(self.model.light_strength)
        growth = random.randint(0, 1000)
        random_growth = random.randint(0, 1000)

        if self.model.light_strength >= 30 and self.model.light_strength <= 60:
            if growth < 5:
                self.grow()
            if random_growth < 4:
                self.random_grow()
        
        if self.model.light_strength < 30:
            if growth < 3:
                self.grow()
            if random_growth < 2:
                self.random_grow()
       
        if self.model.light_strength > 60:
            if growth < 8:
                self.grow()
            if random_growth < 7:
                self.random_grow()

class Fishtank(Model):
    "class Fishtank creates a tank with agents"
    def __init__(self, width, height, probability_algea, number_fish, light_strength):
        super().__init__()

        self.width = width
        self.height = height
        self.number_algea = width * height * probability_algea
        self.number_fish = number_fish
        self.light_strength = light_strength
        
        self.grid = MultiGrid(width, height, False)
        self.visgrid = np.zeros((height,width))
        self.schedule = RandomActivation(self)
        

        # create agents
        for _ in range(self.number_fish):
            a = Fish(self.next_id(), self)
            self.schedule.add(a)

            # add fish to random grid cel
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
        
        for _ in range(int(self.number_algea)):
            b = Algea(self.next_id(), self)
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
        # fish = Image.open("fish.jpeg")

        fish = 2
        algea = 1

        self.fish_counter = 0
        self.algea_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], Algea):
                            self.visgrid[i][j] = algea
                            self.algea_counter += 1
                        if isinstance(self.grid[j][i][something], Fish):
                            self.visgrid[i][j] = fish
                            self.fish_counter += 1
                    
                else:
                    self.visgrid[i][j] = 0

        return self.visgrid 
    
    def fish_counting(self):
        return self.fish_counter
    
    def algea_counting(self):
        return self.algea_counter


    def no_fish(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.visgrid[i][j] == 2:
                    return True
        return False

        

if __name__ == "__main__":
    probability_algea = 0.2
    # probability_algea = float(input('probability of algea: '))
    # y = int(input('fishtank height: '))
    # x = int(input('fishtank width: '))
    height = 50
    width = 100
    # number_fish = int(input('number of fish inside the tank: '))
    number_fish = 50

    # light_strength = int(input('lightstrength 1-100: '))
    light_strength = 50


    # create a forest object
    tank = Fishtank(width, height, probability_algea, number_fish, light_strength)

    # # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange'])
   
    ims = []
    algea = []
    fish = []

    # # data = tank.datacollector.get_model_vars_dataframe()
    # # print(data)
    im = ax.imshow(tank.status(), cmap=cmap)
    ims.append([im])
    algea.append(tank.algea_counting())
    fish.append(tank.fish_counting())
  

    for i in range(200):
        print(i)
    # while tank.no_fish():
        tank.step()
        algea.append(tank.algea_counting())
        fish.append(tank.fish_counting())

        # data = tank.datacollector.get_model_vars_dataframe()
        # print(data)
        im = ax.imshow(tank.status(), cmap=cmap)
        # ims = ax.imshow(data, cmap=cmap)
        ims.append([im])
        # tank.step()
        
    print(algea)
    print(fish)
    ani = animation.ArtistAnimation(fig, ims, interval = 200, blit = True, repeat_delay= 1000)

    plt.xticks(size = 0)
    plt.yticks(size = 0)
    plt.xlabel('width')
    plt.ylabel('height')
    ani.save("fish1.gif")
    