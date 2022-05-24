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
from pyparsing import counted_array

class BigFish(Agent):
    "class Fish makes an agent of the fish"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = 200
        self.age = 0
        self.type = 'bigfish'
        self.mating_counter = 0

    
    def move(self): 
        "decide on neighbour positions"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        

    
        "make the fish move to nearby fish"

        for i in range(len(possible_steps)):
            the_agents = self.model.grid.get_cell_list_contents([possible_steps[i]])
            if len(the_agents)> 0:
                for option in range(len(the_agents)):
                    if isinstance(the_agents[option], Fish):
                        new_position = possible_steps[i]
                        pass
                    else:
                        new_position = self.random.choice(possible_steps)

            else:
                new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -= 1


        "make the fish eat the other fish"

        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents)> 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Fish):
                    agent_fish = agents[option]
                    self.eat(agent_fish)
        

        "make the fish mate with each other"

        if len(agents)> 1:
            if isinstance(agents[0], BigFish) and isinstance(agents[1], BigFish):
                if self.fish_mating_energy():
                    self.mating()
        
        self.age +=1
        self.mating_counter +=1


    
    def eat(self, fish): 
        "the fish eats algea"
        self.model.grid.remove_agent(fish)
        self.model.schedule.remove(fish)
        self.energy += 200
    

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
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        
        
    def step(self):
        "the fish moves when it still has enegery, otherwise dies"

        if self.fish_energy() and self.age < 50:
            self.move()

        else:
            self.move_up()


    def fish_energy(self):
        "tells whether the fish still got some energy"

        if self.energy > 0:
            return True


    def fish_mating_energy(self):
        "tells whether the fish has enough mating energy"
        if self.energy > 80:
            return True
        

    def mating(self):
        "fish make a baby but loose some energy"
        if self.mating_counter > 6:
            bigfish = BigFish(self.model.next_id(), self.model)
            self.model.schedule.add(bigfish)
            self.model.grid.place_agent(bigfish, self.pos)
            self.energy -= 10
            self.mating_counter = 0



class Fish(Agent):
    "class Fish makes an agent of the fish"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = 30
        self.mating_counter = 0
        self.age = 0
        self.type = 'fish'
    
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
                    # print(agents)
                    if self.energy < 300:
                        self.eat(agent_algea)
                    # print('na', agents)
        

        "make the fish mate with each other"

        if len(agents)> 1:
            # print(agents)
            if isinstance(agents[0], Fish) and isinstance(agents[1], Fish):
                if self.fish_mating_energy():
                    self.mating()
        
        self.mating_counter +=1
        self.age +=1

    
    def eat(self, algea): 
        "the fish eats algea"
        self.model.grid.remove_agent(algea)
        self.model.schedule.remove(algea)
        self.energy += 20
    

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

        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        
        
    def step(self):
        "the fish moves when it still has enegery, otherwise dies"

        if self.fish_energy() and self.age < 50:
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
        if self.mating_counter > 12:
            fish = Fish(self.model.next_id(), self.model)
            self.model.schedule.add(fish)
            self.model.grid.place_agent(fish, self.pos)
            self.energy -= 15
            self.mating_counter = 0


class Algea(Agent):
    "class Algea makes an agent of the algea"
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'algea'
        
    def random_grow(self):        
        x = self.random.randrange(self.model.width)
        y = self.random.randrange(self.model.height)
        
        if self.model.grid.is_cell_empty((x, y)):
            algea = Algea(self.model.next_id(), self.model)
            self.model.schedule.add(algea)
            self.model.grid.place_agent(algea, (x,y))

    def step(self):
        random_growth = self.random.randint(0, 100)

        if random_growth < 4 * self.model.light_strength:
            self.random_grow()


class Fishtank(Model):
    "class Fishtank creates a tank with agents"
    def __init__(self, width, height, probability_algea, number_fish, light_strength, number_big_fish):
        super().__init__()

        self.width = width
        self.height = height
        self.number_algea = width * height * probability_algea
        self.number_fish = number_fish
        self.number_big_fish = number_big_fish
        self.light_strength = light_strength / 50
        
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
        
        for _ in range(self.number_big_fish):
            c = BigFish(self.next_id(), self)
            self.schedule.add(c)

            # add algea to random grid cel
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(c, (x, y))


        # self.datacollector = DataCollector(model_reporters={"Grid": self.status})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
    
    def status(self):
        # fish = Image.open("fish.jpeg")

        self.fish_counter = 0
        self.algea_counter = 0
        self.big_fish_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], Algea):
                            self.visgrid[i][j] = 1
                            self.algea_counter += 1
                        if isinstance(self.grid[j][i][something], Fish):
                            self.visgrid[i][j] = 2
                            self.fish_counter += 1
                        if isinstance(self.grid[j][i][something], BigFish):
                            self.visgrid[i][j] = 3
                            self.big_fish_counter += 1
                    
                else:
                    self.visgrid[i][j] = 0

        return self.visgrid 
    
    def big_fish_counting(self):
        return self.big_fish_counter

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
    

        
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if agent.type == 'fish':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
    if agent.type == 'algea':
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 1
        portrayal["Shape"]= "circle"
    else:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 1

    return portrayal
        

if __name__ == "__main__":
    probability_algea = 0.3
    height = 20
    width = 40
    number_fish = 20
    number_big_fish = 10

    # light_strength = int(input('lightstrength in %: '))
    light_strength = 50



    # grid = CanvasGrid(agent_portrayal, 40, 20, 500, 500)

    # # chart = ChartModule([{"Label": "Fish",
    # #                     "Color": "Black"}],
    # #                     data_collector_name='datacollector')

    # server = ModularServer(Fishtank,
    #                     [grid],
    #                     "Fishtank",
    #                     {"width":40, "height": 20, "probability_algea": 0.3, "number_fish": 10, "light_strength": light_strength, "number_big_fish": 10})
    # server.port = 8521 # The default


    # server.launch()

    

    # create a forest object
    tank = Fishtank(width, height, probability_algea, number_fish, light_strength, number_big_fish)

    # # creating the animation
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['blue', 'green', 'orange', 'red'])
   
    ims = []
    algea = []
    fish = []
    big_fish = []

    # # data = tank.datacollector.get_model_vars_dataframe()
    # # print(data)
    im = ax.imshow(tank.status(), cmap=cmap)
    ims.append([im])


    counter_list = []
    counter = 0

    for i in range(700):
    # while tank.no_fish():
    # #     print(i)
        counter +=1
        print(counter)
        counter_list.append(counter)
        algea.append(tank.algea_counting())
        fish.append(tank.fish_counting())
        big_fish.append(tank.big_fish_counting())

    #     # data = tank.datacollector.get_model_vars_dataframe()
    #     # print(data)

        im = ax.imshow(tank.status(), cmap = cmap)
        ims.append([im])

        
    #     plt.subplot(211)
    #     plt.imshow(tank.status(), cmap = cmap)
    #     plt.subplot(212)
    #     plt.plot(counter_list, fish, label = 'fish')
    #     plt.plot(counter_list, algea, label = 'algea')
    #     plt.xlabel('swims')
    #     plt.ylabel('fish')
        
    #     plt.savefig('fig.png')
    #     im =  Image.open("fig.png")
    #     print(im)
    #     ims.append(im) 
    #     print(ims)   
    
        tank.step()
        
    # # save the animation of the fishtank
    # ani = animation.ArtistAnimation(fig, ims, interval = 200, blit = True, repeat_delay= 1000)

    # plt.xticks(size = 0)
    # plt.yticks(size = 0)
    # plt.xlabel('width')
    # plt.ylabel('height')

    # ani.save("fish.gif")

    print(algea)
    print(fish)
    print(big_fish)


    plt.subplot(211)
    plt.plot(counter_list, np.array(algea)/(width * height), label = 'algea')
    plt.ylabel('algea')

    plt.subplot(212)
    plt.plot(counter_list, fish, label = 'fish')
    plt.xlabel('swims')
    plt.ylabel('fish')

    plt.subplot(212)
    plt.plot(counter_list, big_fish, label = 'big_fish')
    # plt.ylabel('big_fish')
    plt.legend()
    
    plt.savefig('fig.png')
