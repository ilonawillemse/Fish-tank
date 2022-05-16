# project-ilona willemse fishtank
This code creates a situation that visualises a fishtank within an animation.

![Fish visualisation](doc/image/prototype.png)

## How to run

```
$ python3 fish.py
```

# General idea

- Fish
    - [] swim in a fishtank.
    - [] swim by boids model
    - [] through swimming energy level goes down
    - [] energy can be obtained by eating algea.
    - [] with energy fish can mate and bare children.
    - [] fish die after a certain time stamp

- algea
    - [] can grow with light.
    - [] number gets reduced by fish that eat algea.

- input
    - [] light strenght
    - [] starting algea density
    - [] starting number of fish

- [] the more fish, the less light, the less algea.
- [] the less algea the less food for the fish, so no mating.

- optional
    - [] different male and female fish for mating.
    - [] different species of fish
    - [] fish grow when they eat.
    - [] different kinds of fish that only mate with the same species.
    - [] adding slides in which the user can change certain values.

- end goal
    - [] visualise how fish populations are influences


## libraries
```
- numpy
- matplotlib.pyplot to plot the data in an image
- matplotlib.animation to visualize the animation
- random to generate a random number to implement some chances
- matplotlib
- copy to copy some grids
- pandas to transform some data for visualisation
```

## limitations that could come up
- not being able to insert an image inside the animation instead of a square
- not being able to let the fish grow
- adding the slides can be tough
- boid model implementation

