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
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pyparsing import counted_array
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.datacollection import DataCollector

class BigFish(Agent):
    "class Fish makes an agent of the fish"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = 200
        self.big_age = 0
        self.type = 'bigfish'
        self.big_mating_counter = 0

    
    def big_move(self): 
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
        self.energy -= 5
        self.big_look()


    def big_look(self):
        "make the fish eat all the other fish at the same location"
        self.current_big_fish_count = 0

        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents)> 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Fish):
                    agent_fish = agents[option]
                    self.big_eat(agent_fish)
        
                "make the fish mate with each other at the same location"
                if isinstance(agents[option], BigFish):
                    self.current_big_fish_count += 1
        
        if self.current_big_fish_count > 1 and len(agents) < 5:
            if self.big_fish_mating_energy() and self.big_age > 15:
                    self.big_mating()
        
        self.big_mating_counter +=1
        self.big_age +=1

    
    def big_eat(self, fish): 
        "the fish eats algea"
        self.model.grid.remove_agent(fish)
        self.model.schedule.remove(fish)
        self.energy += 200
    

    def big_move_up(self):        
        "when the fish dies it moves to the top of the tank"

        new = self.pos[1] + 1
        new_pos = (self.pos[0], new)

        if new < self.model.height:
            self.model.grid.move_agent(self, new_pos)
        
        else:
            self.big_die()
        

    def big_die(self):
        "the big fish dies / dissapears"
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        
        
    def step(self):
        "the fish moves when it still has enegery, otherwise dies"

        if self.big_fish_energy() and self.big_age < 50:
            self.big_move()

        else:
            self.big_move_up()


    def big_fish_energy(self):
        "tells whether the fish still got some energy"

        if self.energy > 0:
            return True


    def big_fish_mating_energy(self):
        "tells whether the fish has enough mating energy"
        if self.energy > 80:
            return True
        

    def big_mating(self):
        "bigfish make 2 babies but loose some energy"
        if self.big_mating_counter > 10:
            for _ in range(2):
                bigfish = BigFish(self.model.next_id(), self.model)
                self.model.schedule.add(bigfish)
                self.model.grid.place_agent(bigfish, self.pos)
            
            self.energy -= 30
            self.big_mating_counter = 0



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
        self.look()


    def look(self):
        "make the fish eat all the algea at the same location"
        self.current_fish_count = 0
        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents)> 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Algea):
                    agent_algea = agents[option]
                    if self.energy < 300:
                        self.eat(agent_algea)

                "make the fish mate with each other at the same location"
                if isinstance(agents[option], Fish):
                    self.current_fish_count += 1
        
        if self.current_fish_count > 1:
            if self.fish_mating_energy() and self.age > 3:
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

        new = self.pos[1] + 1
        new_pos = (self.pos[0], new)

        if new < self.model.height:
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
            self.mating_counter44444444 = 0


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

        if random_growth < 6 * self.model.light_strength:
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

        self.datacollector = DataCollector(
            model_reporters={   "fish": self.fish, 
                                "bigfish": self.bigfish,
                                "algea": self.algea})
        

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


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()  
    
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

    def fish(self):
        fish_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], Fish):
                            fish_counter += 1
        return fish_counter
    
    def bigfish(self):
        big_fish_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], BigFish):
                            big_fish_counter += 1
        return big_fish_counter

    def algea(self):
        algea_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], Algea):
                            algea_counter += 1
        return (algea_counter/ (self.width * self.height))
                

        
def agent_portrayal(agent):
    # add age and color change
    portrayal = {"Filled": "true"}


# For an image:
#                 The image must be placed in the same directory from which the
#                 server is launched. An image has the attributes "x", "y",
#                 "scale", "text" and "text_color".
#         "Color": The color to draw the shape in; needs to be a valid HTML
#                  color, e.g."Red" or "#AA08F8"
#         "Filled": either "true" or "false", and determines whether the shape is
#                   filled or not.
#         "Layer": Layer number of 0 or above; higher-numbered layers are drawn
#                  above lower-numbered layers.
#         "text": The text to be inscribed inside the Shape. Normally useful for
#                 showing the unique_id of the agent.
#         "text_color": The color to draw the inscribed text. Should be given in
#                       conjunction of "text" property.



    if agent.type == 'fish':
        portrayal["Layer"] = 2

        if agent.energy == 0:
            portrayal["Shape"] = "doc/image/deadfish.png"
            portrayal["x"] = 1
            portrayal["y"] = 1
            portrayal["scale"] = 0.8
        else:
            portrayal["Shape"] = "doc/image/fish.png"
            portrayal["x"] = 1
            portrayal["y"] = 1
            portrayal["scale"] = 0.7     

    
    elif agent.type == 'bigfish': 
        portrayal["Layer"] = 2 

        if agent.energy == 0:
            portrayal["Shape"] = "doc/image/deadshark.png"
            portrayal["x"] = 1
            portrayal["y"] = 1
            portrayal["scale"] = 1     
        
        else:
            portrayal["Shape"] = "doc/image/shark.jpg"
            portrayal["x"] = 1
            portrayal["y"] = 1
            portrayal["scale"] = 1



    elif agent.type == 'algea':
        portrayal["Layer"] = 1

        portrayal["Shape"] = "doc/image/algea.jpg"
        portrayal["x"] = 1
        portrayal["y"] = 1
        portrayal["scale"] = 1

    return portrayal
        

if __name__ == "__main__":
    probability_algea = 0.3
    height = 20
    width = 30
    number_fish = 20
    number_big_fish = 4

    # light_strength = int(input('lightstrength in %: '))
    light_strength = 50



    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 300)

    chart = ChartModule([{"Label": "fish", "Color": "Orange"}, 
                        {"Label": "bigfish", "Color": "Red"}], 
                        data_collector_name='datacollector')
    
    chart2 = ChartModule([{"Label": "algea", "Color": "Green"}], 
                        data_collector_name='datacollector')

    server = ModularServer(Fishtank,
                        [grid,chart2,chart],
                        "Fishtank Ilona Willemse",
                        {"width":20, "height": 20, "probability_algea": 0.3, "number_fish": 30, "light_strength": light_strength, "number_big_fish": 6})
    server.port = 8521 # The default


    server.launch()