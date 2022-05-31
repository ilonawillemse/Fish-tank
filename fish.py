"""
=================================================
fish.py

Ilona Willemse

Imitation of a fishtank with growing algea and two populations of fish.
Live visualisation of the fish and algea population growth.
Visualisation of fish population changes when light strength influences.
=================================================
"""
import statistics
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.datacollection import DataCollector


class BigFish(Agent):
    "Creating BigFish agents"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'bigfish'
        self.big_energy = 100
        self.big_age = self.random.randrange(0, 20)
        self.big_mating_counter = 0
        self.current_big_fish_count = 0

    def step(self):
        "the big fish moves when it still has enegery, otherwise dies"

        if self.big_fish_energy() and self.big_age < 200:
            self.big_move()

        else:
            self.big_move_up()

    def big_fish_energy(self):
        "tells whether the big fish still got some energy"

        if self.big_energy > 0:
            return True

    def big_move(self):
        "move to a new spot in the fishtank"

        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.big_energy -= 3
        self.big_look()

    def big_look(self):
        "look at the spot to see whether to eat, mate or do nothing"

        self.current_big_fish_count = 0

        # make the big fish eat smaller fish
        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents) > 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Fish):
                    agent_fish = agents[option]
                    if self.big_energy < 200:
                        self.big_eat(agent_fish)

                # make the big fish mate with each other at the same location
                if isinstance(agents[option], BigFish):
                    self.current_big_fish_count += 1

        if self.current_big_fish_count > 1 and len(agents) < 5:
            if self.big_fish_mating_energy() and self.big_age > 15:
                self.big_mating()

        self.big_mating_counter += 1
        self.big_age += 1

    def big_eat(self, fish):
        "the big fish eats other smaller fish"

        self.model.grid.remove_agent(fish)
        self.model.schedule.remove(fish)
        self.big_energy += 100

    def big_fish_mating_energy(self):
        "tells whether the big fish has enough mating energy"

        if self.big_energy > 200:
            return True

    def big_mating(self):
        "bigfish makes a baby but looses some energy"

        if self.big_mating_counter > 30:
            current = self.model.grid.get_cell_list_contents([self.pos])
            if len(current) < 4:
                bigfish = BigFish(self.model.next_id(), self.model)
                self.model.schedule.add(bigfish)
                self.model.grid.place_agent(bigfish, self.pos)

                self.big_energy -= 150
                self.big_mating_counter = 0

    def big_move_up(self):
        "when the big fish dies it moves to the top of the tank"

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


class Fish(Agent):
    "Creating Fish agents"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'fish'
        self.energy = 40
        self.mating_counter = 0
        self.current_fish_count = 0
        self.age = self.random.randrange(0, 20)

    def step(self):
        "the fish moves when it still has enegery, otherwise dies"

        if self.fish_energy() and self.age < 45:
            speed = self.random.randrange(1, 3)
            for _ in range(speed):
                self.move()
            self.age += 1
            self.energy -= 1

        else:
            self.move_up()

    def fish_energy(self):
        "tells whether the fish still got some energy"

        if self.energy > 0:
            return True

    def move(self):
        "move to a new spot in the fishtank"
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )

        # make the fish move to nearby algea
        for i in range(len(possible_steps)):
            the_agents = self.model.grid.get_cell_list_contents([possible_steps[i]])
            if len(the_agents) > 0:
                for option in range(len(the_agents)):
                    if isinstance(the_agents[option], Algea):
                        new_position = possible_steps[i]
                    else:
                        new_position = self.random.choice(possible_steps)

            else:
                new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.look()

    def look(self):
        "make the fish look at the spot they are at whether to eat, mate or do nothing"

        self.current_fish_count = 0

        # make the fish eat algea
        agents = self.model.grid.get_cell_list_contents([self.pos])
        if len(agents) > 1:
            for option in range(len(agents)):
                if isinstance(agents[option], Algea):
                    agent_algea = agents[option]
                    if self.energy < 200:
                        self.eat(agent_algea)

                # make the fish mate with each other
                if isinstance(agents[option], Fish):
                    self.current_fish_count += 1

        if self.current_fish_count > 1:
            if self.fish_mating_energy() and self.age > 10:
                self.mating()

        self.mating_counter += 1

    def eat(self, algea):
        "the fish eats algea"

        self.model.grid.remove_agent(algea)
        self.model.schedule.remove(algea)
        self.energy += 10

    def fish_mating_energy(self):
        "tells whether the fish has enough mating energy"

        if self.energy > 40:
            return True

    def mating(self):
        "fish make a baby but loose some energy"

        if self.mating_counter > 20:
            current = self.model.grid.get_cell_list_contents([self.pos])
            if len(current) < 3:
                fish = Fish(self.model.next_id(), self.model)
                self.model.schedule.add(fish)
                self.model.grid.place_agent(fish, self.pos)
                self.energy -= 15
                self.mating_counter = 0

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


class Algea(Agent):
    "Create Algea agents"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'algea'

    def step(self):
        "with chance the algea can grow in time"

        random_growth = self.random.randint(0, 100)
        if random_growth < 25 * self.model.light_strength:
            self.random_grow()

    def random_grow(self):
        "makes the algea grow at random locations as long as that gridpoint is empty"

        location_x = self.random.randrange(self.model.width)
        location_y = self.random.randrange(self.model.height)

        if self.model.grid.is_cell_empty((location_x, location_y)):
            algea = Algea(self.model.next_id(), self.model)
            self.model.schedule.add(algea)
            self.model.grid.place_agent(algea, (location_x, location_y))


class Fishtank(Model):
    "A fishtank is created with fish, algea and big fish"

    def __init__(self, width, height, probability_algea, number_fish,
                 light_strength, number_big_fish):
        super().__init__()
        self.width = width
        self.height = height
        self.light_strength = light_strength / 50
        self.fish_counter = 0
        self.big_fish_counter = 0
        self.algea_counter = 0

        self.grid = MultiGrid(width, height, False)
        self.visgrid = np.zeros((height, width))
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"fish": self.fish,
                             "bigfish": self.bigfish,
                             "algea": self.algea})

        # fish are added
        for _ in range(number_fish):
            fish = Fish(self.next_id(), self)
            self.schedule.add(fish)
            location_x = self.random.randrange(self.width)
            location_y = self.random.randrange(self.height)
            self.grid.place_agent(fish, (location_x, location_y))

        # algea are added
        number_algea = width * height * probability_algea
        for _ in range(int(number_algea)):
            algea = Algea(self.next_id(), self)
            self.schedule.add(algea)
            location_x = self.random.randrange(self.width)
            location_y = self.random.randrange(self.height)
            self.grid.place_agent(algea, (location_x, location_y))

        # big fish are added
        for _ in range(number_big_fish):
            bigfish = BigFish(self.next_id(), self)
            self.schedule.add(bigfish)
            location_x = self.random.randrange(self.width)
            location_y = self.random.randrange(self.height)
            self.grid.place_agent(bigfish, (location_x, location_y))

    def step(self):
        self.fishcounting()
        self.datacollector.collect(self)
        self.schedule.step()

    def fishcounting(self):
        "keeps track of the number of fish, big fish and algea in the tank"

        self.fish_counter = 0
        self.big_fish_counter = 0
        self.algea_counter = 0

        for i in range(self.height):
            for j in range(self.width):
                if len(self.grid[j][i]) > 0:
                    for something in range(len(self.grid[j][i])):
                        if isinstance(self.grid[j][i][something], Fish):
                            self.fish_counter += 1
                        if isinstance(self.grid[j][i][something], BigFish):
                            self.big_fish_counter += 1
                        if isinstance(self.grid[j][i][something], Algea):
                            self.algea_counter += 1

    def fish(self):
        "returns the number of fish in the tank"

        return self.fish_counter

    def bigfish(self):
        "returns the number of big fish in the tank"

        return self.big_fish_counter

    def algea(self):
        "returns percentages of algea in comparison to the tank"

        return (self.algea_counter / (self.width * self.height))


def agent_portrayal(agent):
    "give proporties to the agents for visualization"

    portrayal = {"Filled": "true", "x": 1, "y": 1}

    if agent.type == 'fish':
        portrayal["Layer"] = 2

        if agent.energy == 0 or agent.age == 45:
            portrayal["Shape"] = "doc/image/deadfish.png"
            portrayal["scale"] = 0.8

        else:
            portrayal["Shape"] = "doc/image/fish.png"

            if agent.age < 10:
                portrayal["scale"] = 0.3

            elif agent.age < 30:
                portrayal["scale"] = 0.5

            else:
                portrayal["scale"] = 0.8

    elif agent.type == 'bigfish':
        portrayal["Layer"] = 3

        if agent.big_energy == 0 or agent.big_age == 200:
            portrayal["Shape"] = "doc/image/deadshark.png"
            portrayal["scale"] = 1

        else:
            portrayal["Shape"] = "doc/image/shark.jpg"

            if agent.big_age < 10:
                portrayal["scale"] = 0.5

            elif agent.big_age < 50:
                portrayal["scale"] = 0.8

            else:
                portrayal["scale"] = 1

    elif agent.type == 'algea':
        portrayal["Shape"] = "doc/image/algea.jpg"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1

    return portrayal


def visualize_experiment():
    "visualisation of number of Fish depending on light strength"

    fish = {}
    bigfish = {}
    for light in np.arange(0, 110, 10):
        print(light)
        fish_list = []
        bigfish_list = []

        for _ in range(20):
            tank = Fishtank(15, 15, 0.3, 20, light, 6)
            for _ in range(400):
                tank.step()
            fish_list.append(tank.fish_counter)
            bigfish_list.append(tank.big_fish_counter)

        mean_fish = statistics.mean(fish_list)
        mean_bigfish = statistics.mean(bigfish_list)

        fish[light] = mean_fish
        bigfish[light] = mean_bigfish

    print(fish)
    print(bigfish)

    plt.plot(fish.keys(), fish.values())
    plt.plot(bigfish.keys(), bigfish.values())
    plt.legend(['fish', 'bigfish'])
    plt.title('Sensitivity of fish populations depending on light strength')
    plt.xlabel('Light strength')
    plt.ylabel('Fish numbers')
    plt.savefig('fishies.png')


def live_fishtank(light_strength):
    "create an animation and view fish / algea countings"

    grid = CanvasGrid(agent_portrayal, 15, 15, 500, 300)

    chart = ChartModule([{"Label": "fish", "Color": "Red"},
                         {"Label": "bigfish", "Color": "Blue"}],
                        data_collector_name='datacollector')

    chart2 = ChartModule([{"Label": "algea", "Color": "Green"}],
                         data_collector_name='datacollector')

    server = ModularServer(Fishtank, [grid, chart2, chart],
                           "Fishtank Ilona Willemse",
                           {"width": 15, "height": 15, "probability_algea": 0.3,
                            "number_fish": 20, "light_strength": light_strength,
                            "number_big_fish": 6})
    server.port = 8521  # The default

    server.launch()


if __name__ == "__main__":

    # ask whether the user would like to perform the experiment
    ANSWER = input('Would you like to run the experiment?(yes/no): ')
    if ANSWER == "yes":
        # sensitivity analysis of number of fish depending on ligth strength
        visualize_experiment()

    print('A visualisation of a fishtank with different populations will be shown,   \
the size of these populations depend on the light strength')

    # live visualisation of the fishtank with certain light strength
    LIGHT_STRENGTH = int(input('What light strength in % would you like to test: '))

    live_fishtank(LIGHT_STRENGTH)
